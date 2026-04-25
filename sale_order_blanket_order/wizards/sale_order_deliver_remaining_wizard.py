# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleOrderDelierRemainingWizardLine(models.TransientModel):
    _name = "sale.order.deliver.remaining.wizard.line"
    _description = "Remaining product to deliver"

    wizard_id = fields.Many2one(
        "sale.order.deliver.remaining.wizard",
        string="Wizard",
        required=True,
        ondelete="cascade",
    )
    sale_order_line_id = fields.Many2one(
        "sale.order.line", string="Sale Order Line", required=True, readonly=True
    )
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        related="sale_order_line_id.product_id",
        readonly=True,
    )
    product_packaging_id = fields.Many2one(
        "product.packaging",
        string="Packaging",
        related="sale_order_line_id.product_packaging_id",
        readonly=True,
    )
    call_off_remaining_qty = fields.Float(
        string="Remaining Quantity",
        related="sale_order_line_id.call_off_remaining_qty",
        readonly=True,
    )
    qty_to_deliver = fields.Float(string="Quantity to Deliver", required=True)

    @api.constrains("qty_to_deliver")
    def _check_qty_to_deliver(self):
        for line in self:
            if line.qty_to_deliver > line.call_off_remaining_qty:
                raise UserError(
                    _(
                        "The 'Quantity to Deliver' cannot be greater than the "
                        "'Remaining Quantity'."
                    )
                )
            if line.qty_to_deliver < 0:
                raise UserError(_("The 'Quantity to Deliver' cannot be negative."))


class SaleOrderDelierRemainingWizard(models.TransientModel):
    _name = "sale.order.deliver.remaining.wizard"
    _description = "Create Call-off Sale Order for remaining products"

    order_id = fields.Many2one(
        "sale.order", string="Order", required=True, readonly=True
    )
    wizard_line_ids = fields.One2many(
        "sale.order.deliver.remaining.wizard.line",
        "wizard_id",
        string="Products to Deliver",
    )

    def action_create_call_off(self):
        self.ensure_one()
        call_off_lines = []
        for wizard_line in self.wizard_line_ids:
            if wizard_line.qty_to_deliver > 0:
                line_vals = {
                    "product_id": wizard_line.product_id.id,
                    "product_uom_qty": wizard_line.qty_to_deliver,
                    "product_uom": wizard_line.sale_order_line_id.product_uom.id,
                    "name": wizard_line.sale_order_line_id.name,
                    "price_unit": 0.0,
                    "tax_id": [(6, 0, wizard_line.sale_order_line_id.tax_id.ids)],
                    "order_id": self.order_id.id,
                }
                call_off_lines.append((0, 0, line_vals))
        if not call_off_lines:
            raise UserError(_("A call off order should have at least one product."))

        call_off_order = self.env["sale.order"].create(
            {
                "partner_id": self.order_id.partner_id.id,
                "partner_invoice_id": self.order_id.partner_invoice_id.id,
                "partner_shipping_id": self.order_id.partner_shipping_id.id,
                "pricelist_id": self.order_id.pricelist_id.id,
                "origin": self.order_id.name,
                "user_id": self.order_id.user_id.id,
                "team_id": self.order_id.team_id.id,
                "order_line": call_off_lines,
                "order_type": "call_off",
                "blanket_order_id": self.order_id.id,
            }
        )
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "res_id": call_off_order.id,
            "view_mode": "form",
            "target": "current",
        }
