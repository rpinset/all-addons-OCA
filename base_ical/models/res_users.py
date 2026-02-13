# Copyright 2023 Hunki Enterprises BV
# Copyright 2024 initOS GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    ical_ids = fields.One2many("base.ical", compute="_compute_ical_ids")

    def _compute_ical_ids(self):
        for this in self:
            domain = [("allowed_users_ids", "=", this.id)]
            this.ical_ids = self.env["base.ical"].search(domain)

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + ["ical_ids"]

    @api.model_create_multi
    def create(self, vals_list):
        result = super().create(vals_list)
        auto_calendars = (
            self.env["base.ical"]
            .sudo()
            .search(
                [
                    ("auto", "=", True),
                    "|",
                    ("auto_group_ids", "=", False),
                    ("auto_group_ids", "in", result.groups_id.ids),
                ]
            )
        )
        if not auto_calendars:
            return result
        for this in result:
            auto_calendars.filtered(
                lambda x, this=this: not x.auto_group_ids
                or this.groups_id & x.auto_group_ids
            ).write({"allowed_users_ids": [fields.Command.link(this.id)]})
        return result
