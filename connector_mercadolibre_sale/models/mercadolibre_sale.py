# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.exceptions import AccessError


class MercadoLibreSaleOrder(models.Model):
    _name = "mercadolibre.sale.order"
    _inherit = "mercadolibre.binding"
    _description = "Mercado Libre Order"
    _order = "id desc"

    odoo_id = fields.Many2one(
        comodel_name="sale.order",
        required=True,
        ondelete="cascade",
        index=True,
    )
    backend_id = fields.Many2one(
        comodel_name="mercadolibre.backend",
        required=True,
        ondelete="restrict",
        index=True,
    )
    external_id = fields.Char(required=True, index=True)
    pack_id = fields.Char(index=True)
    order_status = fields.Char()
    payment_status = fields.Char()
    sale_fee = fields.Monetary()
    currency_id = fields.Many2one(comodel_name="res.currency")
    shipment_external_id = fields.Char()
    shipment_id = fields.Many2one(
        comodel_name="mercadolibre.shipment",
        ondelete="set null",
    )
    date_order = fields.Datetime()
    date_updated = fields.Datetime()

    _sale_external_unique = models.Constraint(
        "UNIQUE(backend_id, external_id)",
        "This Mercado Libre order is already imported.",
    )

    def _check_sales_manager(self):
        if not self.env.user.has_group(
            "connector_mercadolibre.group_mercadolibre_manager"
        ):
            raise AccessError(
                self.env._("Only Mercado Libre managers can import orders.")
            )

    def button_import(self):
        self._check_sales_manager()
        for binding in self:
            binding.backend_id._enqueue_order_import(binding.external_id)

    def action_view_pack(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id("sale.action_orders")
        action["domain"] = [
            ("mercadolibre_pack_id", "=", self.pack_id),
            ("id", "!=", self.odoo_id.id),
        ]
        return action

    def _job_import(self):
        self.ensure_one()
        self.backend_id._job_import_order(self.external_id)
