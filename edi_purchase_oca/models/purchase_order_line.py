# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _name = "purchase.order.line"
    _inherit = [
        "purchase.order.line",
        "edi.exchange.consumer.mixin",
        "edi.id.mixin",
    ]

    edi_disable_auto = fields.Boolean(related="order_id.edi_disable_auto")
    edi_exchange_ready = fields.Boolean(compute="_compute_edi_exchange_ready")

    @api.depends()
    def _compute_edi_exchange_ready(self):
        for rec in self:
            rec.edi_exchange_ready = rec._edi_exchange_ready()

    def _edi_exchange_ready(self):
        # Only product lines are eligible for EDI processing
        # sections/notes and downpayment lines should be ignored
        return not self.display_type and not self.is_downpayment

    @api.model_create_multi
    def create(self, vals_list):
        # Set default origin if not passed
        for vals in vals_list:
            orig_id = vals.get("origin_exchange_record_id")
            if not orig_id and "order_id" in vals:
                order = self.env["purchase.order"].browse(vals["order_id"])
                vals["origin_exchange_record_id"] = order.origin_exchange_record_id.id
        return super().create(vals_list)
