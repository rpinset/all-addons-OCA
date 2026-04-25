# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo import api, models
from odoo.osv.expression import OR


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("picking_ids.exchange_record_ids")
    def _compute_exchange_record_count(self):
        res = super()._compute_exchange_record_count()
        for rec in self:
            rec.exchange_record_count += sum(
                rec.picking_ids.mapped("exchange_record_count")
            )
        return res

    def action_view_edi_records(self):
        res = super().action_view_edi_records()
        for picking in self.picking_ids:
            picking_domain = picking.action_view_edi_records()["domain"]
            res["domain"] = OR([res["domain"], picking_domain])
        return res
