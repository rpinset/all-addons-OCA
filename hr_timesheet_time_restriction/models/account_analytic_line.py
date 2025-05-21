# Copyright 2022 Dinar Gabbasov
# Copyright 2022 Ooops404
# Copyright 2022 Cetmix
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from datetime import date, timedelta

from odoo import _, api, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.constrains("date")
    def _check_project_date(self):
        """
        Checks and validates the project timesheet date based on defined restrictions

        Attributes:
            date (fields.Date): The timesheet entry date.
            project_id (fields.Many2one): The project associated with the timesheet entry.

        Raises:
            ValidationError: Raised if the timesheet date does not adhere to the allowed days
            of entry. The restrictions can be defined either globally or at the project level.
        """
        if not self._is_time_manager():
            use_global, global_days = self._read_global_restriction()
            for record in self:
                if (
                    record.date
                    and record.project_id
                    and (use_global or record.project_id.use_timesheet_restriction)
                ):
                    allowed_days = (
                        record.project_id.timesheet_restriction_days or global_days
                    )
                    self._validate_timesheet_date(record, allowed_days)

    def _is_time_manager(self):
        """Return True if the current user is in the timesheet time manager group."""
        is_manager = self.user_has_groups(
            "hr_timesheet_time_restriction.group_timesheet_time_manager"
        )

        if not is_manager:
            _logger.warning(
                "Unauthorized attempt to bypass timesheet restriction by user %s (ID=%s)",
                self.env.user.login or self.env.user.name,
                self.env.uid,
            )

        return is_manager

    def _read_global_restriction(self):
        """
        Reads global restriction settings for timesheets.

        Returns:
            tuple: A tuple where the first element is a boolean indicating whether
            timesheet restrictions are enabled and the second element is an integer
            representing the number of restriction days configured.
        """
        params = self.env["ir.config_parameter"].sudo()
        use_flag = bool(
            params.get_param(
                "hr_timesheet_time_restriction.use_timesheet_restriction", False
            )
        )
        days = int(
            params.get_param(
                "hr_timesheet_time_restriction.timesheet_restriction_days", 0
            )
        )
        return use_flag, days

    def _validate_timesheet_date(self, record, allowed_days):
        """
        Validates the date of the timesheet record against the allowed policy settings,
        ensuring entries comply with the set boundaries.

        Args:
            record (Record): The timesheet record containing the date to be validated.
            allowed_days (int): The number of days allowed for backdating timesheets. If set
                to 0, only today's date is permissible.

        Raises:
            ValidationError: If the record date is older than allowed_days or does not match
                today's date when allowed_days is set to 0.
        """
        if not record.date or not isinstance(record.date, date):
            raise ValidationError(_("Invalid date value for timesheet record."))

        if allowed_days < 0:
            raise ValidationError(_("Allowed days must be a non-negative integer."))

        today = date.today()
        delta = today - record.date

        if allowed_days > 0:
            # Disallow entries older than allowed_days
            if delta > timedelta(days=allowed_days):
                raise ValidationError(
                    _(
                        "You cannot set a timesheet more than %(days)s days from current date.",
                        days=allowed_days,
                    )
                )
        else:
            if record.date != today:
                raise ValidationError(
                    _(
                        "You cannot set a timesheet for a date different from current date."
                    )
                )
