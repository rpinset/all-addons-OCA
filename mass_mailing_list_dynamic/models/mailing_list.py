# Copyright 2017 Tecnativa - Jairo Llopis
# Copyright 2020 Hibou Corp. - Jared Kipe
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class MassMailingList(models.Model):
    _inherit = "mailing.list"

    dynamic = fields.Boolean(
        help="Set this list as dynamic, to make it autosynchronized with "
        "partners from a given criteria."
    )
    sync_method = fields.Selection(
        selection=[
            ("add", "Only add new records"),
            ("full", "Add and remove records as needed"),
        ],
        default="add",
        required=True,
        help="Choose the synchronization method for this list if you want to "
        "make it dynamic",
    )
    sync_domain = fields.Char(
        string="Synchronization criteria",
        default="[('is_blacklisted', '=', False), ('email', '!=', False)]",
        required=True,
        help="Filter partners to sync in this list",
    )
    is_synced = fields.Boolean(
        help="Helper field to make the user aware of unsynced changes", default=True
    )

    def action_sync(self):
        """Sync contacts in dynamic lists."""
        Contact = self.env["mailing.contact"].with_context(syncing=True)
        Partner = self.env["res.partner"]
        detached = Contact
        # Skip non-dynamic lists
        dynamic = self.filtered("dynamic").with_context(syncing=True)
        for one in dynamic:
            sync_domain = [("email", "!=", False)] + safe_eval(one.sync_domain)
            desired_partners = Partner.search(sync_domain)
            final_contacts = one.contact_ids
            # Detach or remove undesired contacts when synchronization is full
            if one.sync_method == "full":
                final_contacts -= final_contacts.filtered(
                    lambda r, dp=desired_partners: r.partner_id not in dp
                )
            # Add new contacts
            current_partners = final_contacts.mapped("partner_id")
            for partner in desired_partners - current_partners:
                final_contacts |= partner.mass_mailing_contact_ids[:1] or self.env[
                    "mailing.contact"
                ].new({"partner_id": partner.id})
            detached |= one.contact_ids - final_contacts
            one.contact_ids = final_contacts
            one.is_synced = True
        # Clean up empty detached contacts
        detached.filtered(lambda rec: not rec.list_ids).unlink()
        # Invalidate cached contact count
        dynamic.invalidate_recordset(["contact_count"])

    @api.onchange("dynamic", "sync_method", "sync_domain")
    def _onchange_dynamic(self):
        for rec in self:
            if rec.dynamic:
                rec.is_synced = False
