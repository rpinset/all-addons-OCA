# Copyright 2026 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PruneMailingList(models.Model):
    _name = "mass_mailing_list_prune_blacklisted.wizard"
    _description = "Remove blacklisted contacts from mailng list"

    blacklisted_contact_ids = fields.Many2many(
        comodel_name="mailing.contact",
        readonly=True,
        string="Blacklisted contacts",
    )
    list_ids = fields.Many2many(
        comodel_name="mailing.list",
        default=lambda model: model.env.context.get("active_ids"),
        readonly=True,
        string="Selected Lists",
    )

    @api.model
    def default_get(self, fields_list):
        default_values = super().default_get(fields_list)
        default_list_command = default_values.get("list_ids")
        if default_list_command:
            default_list_ids = self._fields["list_ids"].convert_to_cache(
                default_list_command, self
            )
            blacklisted_contacts_data = self.env["mailing.contact"].search_read(
                domain=[
                    ("is_blacklisted", "=", True),
                    ("list_ids", "in", default_list_ids),
                ],
                fields=["list_ids"],
            )
            default_values["blacklisted_contact_ids"] = [
                fields.Command.set([data["id"] for data in blacklisted_contacts_data])
            ]
        return default_values

    def remove_blacklisted_contacts(self):
        for mailing_list in self.list_ids:
            list_blacklisted_contacts = self.blacklisted_contact_ids.filtered(
                lambda c: mailing_list in c.list_ids
            )
            if list_blacklisted_contacts:
                mailing_list.contact_ids = [
                    fields.Command.unlink(list_blacklisted_contact.id)
                    for list_blacklisted_contact in list_blacklisted_contacts
                ]
