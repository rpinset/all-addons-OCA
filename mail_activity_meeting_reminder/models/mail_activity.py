# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class MailActivity(models.Model):

    _inherit = "mail.activity"

    def action_create_calendar_event(self):
        action = super().action_create_calendar_event()
        action["context"].setdefault(
            "default_alarm_ids",
            self.activity_type_id.default_alarm_ids.ids,
        )
        return action
