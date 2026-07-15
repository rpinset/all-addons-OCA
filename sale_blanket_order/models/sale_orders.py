# Copyright 2018 ACSONE SA/NV
# Copyright 2019 Eficent and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import date, timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    blanket_order_id = fields.Many2one(
        "sale.blanket.order",
        string="Origin blanket order",
        related="order_line.blanket_order_line.order_id",
    )
    disable_adding_lines = fields.Boolean(
        compute="_compute_disable_adding_lines",
    )

    @api.model
    def _check_exchausted_blanket_order_line(self):
        return any(
            line.blanket_order_line.remaining_qty < 0.0 for line in self.order_line
        )

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order._check_exchausted_blanket_order_line():
                raise ValidationError(
                    self.env._(
                        "Cannot confirm order %(name)s as one of the lines refers "
                        "to a blanket order that has no remaining quantity.",
                        name=order.name,
                    )
                )
            order.check_partner_id()
            order.order_line.check_product_id()
            order.order_line.check_currency()
        return res

    @api.constrains("partner_id")
    def check_partner_id(self):
        if self.order_line.filtered(
            lambda r: r.blanket_order_line
            and r.blanket_order_line.partner_id != self.partner_id
        ):
            raise ValidationError(
                self.env._(
                    "The customer must be equal to the blanket order lines customer"
                )
            )

    @api.depends("blanket_order_id")
    @api.depends_context("uid")
    def _compute_disable_adding_lines(self):
        self.disable_adding_lines = False
        if self.env.user.has_group(
            "sale_blanket_order.blanket_orders_disable_adding_lines"
        ):
            for order in self:
                order.disable_adding_lines = order.blanket_order_id


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    blanket_order_line = fields.Many2one(
        "sale.blanket.order.line",
        string="Blanket Order line",
        copy=False,
        compute="_compute_blanket_order_line",
        store=True,
        precompute=True,
    )

    def _get_assigned_bo_line(self, bo_lines):
        # We get the blanket order line with enough quantity and closest
        # scheduled date
        assigned_bo_line = False
        date_planned = date.today()
        date_delta = timedelta(days=365)
        for line in bo_lines.filtered(lambda bo_line: bo_line.date_schedule):
            date_schedule = line.date_schedule
            if date_schedule and abs(date_schedule - date_planned) < date_delta:
                assigned_bo_line = line
                date_delta = abs(date_schedule - date_planned)
        if assigned_bo_line:
            return assigned_bo_line
        non_date_bo_lines = bo_lines.filtered(lambda bo_line: not bo_line.date_schedule)
        if non_date_bo_lines:
            return non_date_bo_lines[0]

    def _get_eligible_bo_lines_domain(self, base_qty):
        today = fields.Date.today()
        # Keep only blanket order lines that can actually satisfy this sale line:
        # same product and currency, enough remaining quantity, open contract,
        # and a validity period that has already started.
        filters = [
            ("product_id", "=", self.product_id.id),
            ("remaining_qty", ">=", base_qty),
            ("currency_id", "=", self.order_id.currency_id.id),
            ("order_id.state", "=", "open"),
            "|",
            ("order_id.validity_start_date", "=", False),
            ("order_id.validity_start_date", "<=", today),
        ]
        if self.order_id.partner_id:
            filters.append(("partner_id", "=", self.order_id.partner_id.id))
        return filters

    def _get_eligible_bo_lines(self):
        base_qty = self.product_uom_id._compute_quantity(
            self.product_uom_qty, self.product_id.uom_id
        )
        filters = self._get_eligible_bo_lines_domain(base_qty)
        return self.env["sale.blanket.order.line"].search(filters)

    def get_assigned_bo_line(self):
        self.ensure_one()
        eligible_bo_lines = self._get_eligible_bo_lines()
        if eligible_bo_lines:
            if (
                not self.blanket_order_line
                or self.blanket_order_line not in eligible_bo_lines
            ):
                self.blanket_order_line = self._get_assigned_bo_line(eligible_bo_lines)
        else:
            self.blanket_order_line = False

    @api.depends("product_id", "order_partner_id", "currency_id")
    def _compute_blanket_order_line(self):
        for line in self:
            if line.product_id:
                line.get_assigned_bo_line()
            else:
                line.blanket_order_line = False

    @api.depends("blanket_order_line")
    def _compute_tax_ids(self):
        so_line_linked_bol = self.filtered("blanket_order_line.taxes_id")
        for line in so_line_linked_bol:
            line.tax_ids = line.blanket_order_line.taxes_id
        return super(SaleOrderLine, (self - so_line_linked_bol))._compute_price_unit()

    def _get_blanket_order_line_price_unit(self):
        """Return the blanket order line price in the sale line UoM."""
        self.ensure_one()
        if self.blanket_order_line.product_uom != self.product_uom_id:
            return self.blanket_order_line.product_uom._compute_price(
                self.blanket_order_line.price_unit, self.product_uom_id
            )
        return self.blanket_order_line.price_unit

    @api.depends(
        "blanket_order_line",
        "product_id",
        "product_uom_id",
        "product_uom_qty",
    )
    def _compute_price_unit(self):
        so_line_linked_bol = self.filtered("blanket_order_line")
        for line in so_line_linked_bol:
            price_unit = line._get_blanket_order_line_price_unit()
            line.update(
                {
                    "price_unit": price_unit,
                    "technical_price_unit": price_unit,
                }
            )
        return super(SaleOrderLine, (self - so_line_linked_bol))._compute_price_unit()

    @api.constrains("product_id")
    def check_product_id(self):
        if self.filtered(
            lambda r: r.blanket_order_line
            and r.product_id != r.blanket_order_line.product_id
        ):
            raise ValidationError(
                self.env._(
                    "The product in the blanket order and in the sales order must match"
                )
            )

    @api.constrains("currency_id")
    def check_currency(self):
        if self.filtered(
            lambda r: r.blanket_order_line
            and r.currency_id != r.blanket_order_line.order_id.currency_id
        ):
            raise ValidationError(
                self.env._(
                    "The currency of the blanket order must match with "
                    "that of the sale order."
                )
            )
