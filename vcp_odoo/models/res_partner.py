# Copyright 2026 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    modules_maintained_count = fields.Integer(
        compute="_compute_modules_maintained_count"
    )

    modules_author_count = fields.Integer(compute="_compute_modules_author_count")

    def _compute_modules_maintained_count(self):
        for record in self:
            record.modules_maintained_count = self.env["vcp.odoo.module"].search_count(
                [("version_ids.maintainer_ids.partner_id", "=", record.id)],
            )

    def action_view_maintained_modules(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "vcp_odoo.vcp_odoo_module_act_window"
        )
        action["domain"] = [("version_ids.maintainer_ids.partner_id", "=", self.id)]
        return action

    def _compute_modules_author_count(self):
        for record in self:
            record.modules_author_count = self.env["vcp.odoo.module"].search_count(
                [("version_ids.author_ids.partner_id", "=", record.id)],
            )

    def action_view_author_modules(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "vcp_odoo.vcp_odoo_module_act_window"
        )
        action["domain"] = [("version_ids.author_ids.partner_id", "=", self.id)]
        return action
