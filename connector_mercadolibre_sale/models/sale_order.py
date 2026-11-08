# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    mercadolibre_bind_ids = fields.One2many(
        comodel_name="mercadolibre.sale.order",
        inverse_name="odoo_id",
    )
    mercadolibre_order_id = fields.Char(
        compute="_compute_mercadolibre_binding_values",
        store=True,
        index=True,
    )
    mercadolibre_pack_id = fields.Char(
        compute="_compute_mercadolibre_binding_values",
        store=True,
        index=True,
    )
    mercadolibre_unmapped_logistic = fields.Boolean(copy=False)
    mercadolibre_pack_count = fields.Integer(compute="_compute_mercadolibre_pack_count")
    mercadolibre_payment_status = fields.Char(
        compute="_compute_mercadolibre_page",
        string="Payment Status",
    )
    mercadolibre_sale_fee = fields.Float(
        compute="_compute_mercadolibre_page",
        string="Sale Fee",
    )
    mercadolibre_shipment_status = fields.Char(
        compute="_compute_mercadolibre_page",
        string="Shipment Status",
    )
    mercadolibre_logistic_type = fields.Char(
        compute="_compute_mercadolibre_page",
        string="Logistic Type",
    )

    @api.depends(
        "mercadolibre_bind_ids.external_id",
        "mercadolibre_bind_ids.pack_id",
    )
    def _compute_mercadolibre_binding_values(self):
        for order in self:
            binding = order.mercadolibre_bind_ids[:1]
            order.mercadolibre_order_id = binding.external_id
            order.mercadolibre_pack_id = binding.pack_id

    @api.depends("mercadolibre_pack_id")
    def _compute_mercadolibre_pack_count(self):
        for order in self:
            if not order.mercadolibre_pack_id:
                order.mercadolibre_pack_count = 0
                continue
            order.mercadolibre_pack_count = self.search_count(
                [
                    ("mercadolibre_pack_id", "=", order.mercadolibre_pack_id),
                    ("id", "!=", order.id),
                ]
            )

    @api.depends(
        "mercadolibre_bind_ids.payment_status",
        "mercadolibre_bind_ids.sale_fee",
        "mercadolibre_bind_ids.shipment_id.status",
        "mercadolibre_bind_ids.shipment_id.logistic_type",
    )
    def _compute_mercadolibre_page(self):
        for order in self:
            binding = order.mercadolibre_bind_ids[:1]
            shipment = binding.shipment_id
            order.mercadolibre_payment_status = binding.payment_status
            order.mercadolibre_sale_fee = binding.sale_fee
            order.mercadolibre_shipment_status = shipment.status
            order.mercadolibre_logistic_type = shipment.logistic_type

    def action_view_mercadolibre_pack(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id("sale.action_orders")
        action["domain"] = [
            ("mercadolibre_pack_id", "=", self.mercadolibre_pack_id),
            ("id", "!=", self.id),
        ]
        return action

    def action_open_mercadolibre_binding(self):
        self.ensure_one()
        binding = self.mercadolibre_bind_ids[:1]
        return {
            "type": "ir.actions.act_window",
            "res_model": "mercadolibre.sale.order",
            "view_mode": "form",
            "res_id": binding.id,
        }


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    mercadolibre_unmatched = fields.Boolean(copy=False)
