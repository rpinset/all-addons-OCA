# Copyright 2025 Tenativa - Eduardo Ezerouali
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailingSearchExcludeMixin(models.AbstractModel):
    _name = "mailing.search.exclude.mixin"
    _description = "Mailing search count exclude"

    @api.model
    def search_count(self, domain, limit=None):
        res = super().search_count(domain, limit=limit)
        mass_mailing_id = self.env.context.get("exclude_mass_mailing", False)
        if mass_mailing_id:
            res_ids = (
                self.env["mailing.mailing"]
                .browse(mass_mailing_id)
                .event_filtered_ids(self, domain, field="email")
            )
            res = len(res_ids) if res_ids else 0
        return res
