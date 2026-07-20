# Copyright 2026 Nexusai Solutions (OPC) Private Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CrowdfundingChallenge(models.Model):
    _inherit = "crowdfunding.challenge"

    start_datetime = fields.Datetime(help="Date and time when pledge become available")

    end_datetime = fields.Datetime(
        help="Date and time when pledges are no longer accepted"
    )

    @api.constrains("start_datetime", "end_datetime")
    def _check_schedule_dates(self):
        for challenge in self:
            if challenge.start_datetime and challenge.end_datetime:
                if challenge.start_datetime > challenge.end_datetime:
                    raise ValidationError(
                        self.env._("Start date cannot be after end date.")
                    )

    def _is_scheduled_active(self):
        self.ensure_one()

        now = fields.Datetime.now()

        if self.start_datetime and now < self.start_datetime:
            return False

        if self.end_datetime and now > self.end_datetime:
            return False

        return True

    def _can_pay(self, partner=None):
        self.ensure_one()

        if not super()._can_pay(partner=partner):
            return False

        return self._is_scheduled_active()
