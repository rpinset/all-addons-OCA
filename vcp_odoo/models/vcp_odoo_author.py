# Copyright 2026 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, tools


class VcpOdooAuthor(models.Model):
    _name = "vcp.odoo.author"
    _description = "Vcp Odoo Author"

    name = fields.Char()
    partner_id = fields.Many2one("res.partner", "Partner")

    _sql_constraints = [("name_unique", "unique(name)", "Name must be uniq")]

    def _get_partner(self, name):
        # Simple way to match the partner
        partner = self.env["res.partner"].search(
            [("name", "ilike", name), ("parent_id", "=", False)]
        )
        if len(partner) > 1:
            partner = partner.filtered(lambda s: s.name == name)
        if len(partner) == 1:
            return partner.id
        else:
            return None

    def _prepare_author(self, name):
        return {"name": name, "partner_id": self._get_partner(name)}

    @tools.ormcache("name")
    def _get_author(self, name):
        author = self.search([("name", "=", name)], limit=1)
        if not author:
            vals = self._prepare_author(name)
            author = self.create(vals)
        return author.id
