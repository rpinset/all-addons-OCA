# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    mercadolibre_bind_ids = fields.One2many(
        comodel_name="mercadolibre.res.partner",
        inverse_name="odoo_id",
    )
    mercadolibre_bind_count = fields.Integer(compute="_compute_mercadolibre_bind_count")

    @api.depends("mercadolibre_bind_ids")
    def _compute_mercadolibre_bind_count(self):
        counts = {
            partner.id: count
            for partner, count in self.env["mercadolibre.res.partner"]._read_group(
                domain=[("odoo_id", "in", self.ids)],
                groupby=["odoo_id"],
                aggregates=["__count"],
            )
        }
        for partner in self:
            partner.mercadolibre_bind_count = counts.get(partner.id, 0)

    def action_view_mercadolibre_bindings(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "connector_mercadolibre_sale.action_mercadolibre_partner"
        )
        action["domain"] = [("odoo_id", "in", self.ids)]
        return action
