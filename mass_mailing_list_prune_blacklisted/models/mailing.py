# Copyright 2026 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class Mailing(models.Model):
    _inherit = "mailing.mailing"

    has_list_blacklisted_contacts = fields.Boolean(
        help="One of the mailing lists has blacklisted contacts.",
        compute="_compute_has_list_blacklisted_contacts",
    )

    @api.depends(
        "contact_list_ids",
    )
    def _compute_has_list_blacklisted_contacts(self):
        for mailing in self:
            for mailing_list in mailing.contact_list_ids:
                if mailing_list._origin:
                    # The mailing is being created/edited
                    mailing_list = mailing_list._origin

                if mailing_list.contact_count_blacklisted:
                    has_list_blacklisted_contacts = True
                    break
            else:
                has_list_blacklisted_contacts = False

            mailing.has_list_blacklisted_contacts = has_list_blacklisted_contacts

    def show_prune_lists_wizard(self):
        wizard_action = self.env["ir.actions.act_window"]._for_xml_id(
            "mass_mailing_list_prune_blacklisted.prune_wizard_action"
        )
        action_context = wizard_action.get("context", "{}")
        action_context_dict = safe_eval(action_context)
        action_context_dict["default_list_ids"] = self.contact_list_ids.ids
        wizard_action["context"] = str(action_context_dict)
        return wizard_action
