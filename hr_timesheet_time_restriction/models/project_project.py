# Copyright 2022 Dinar Gabbasov
# Copyright 2022 Ooops404
# Copyright 2022 Cetmix
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = "project.project"

    timesheet_restriction_days = fields.Integer(
        default=0,
        help="Maximum number of days before today allowed for a timesheet. "
        "Set to 0 to disable project‑level restriction.",
    )
    use_timesheet_restriction = fields.Boolean(
        default=lambda self: self._default_use_timesheet_restriction(),
        help="Whether to enforce date restriction for this project "
        "based on the global setting.",
    )

    @api.model
    def _default_use_timesheet_restriction(self):
        """
        This method provides a default value for the 'use_timesheet_restriction' field by
        fetching the configuration parameter
        'hr_timesheet_time_restriction.use_timesheet_restriction'.
        It ensures that the returned value is a boolean.

        Returns:
            bool: The default value of the 'use_timesheet_restriction' field based on the
            system configuration parameter.
        """
        return bool(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("hr_timesheet_time_restriction.use_timesheet_restriction", False)
        )

    @api.constrains("timesheet_restriction_days")
    def _check_timesheet_restriction_days(self):
        """
        Checks and validates the timesheet restriction days for projects

        Raises:
            ValidationError:
                If the `timesheet_restriction_days` field contains a negative value
                in a project record.
        """
        # Skip validation if global restriction is disabled
        global_flag = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("hr_timesheet_time_restriction.use_timesheet_restriction", False)
        )
        if not bool(global_flag):
            return

        for project in self:
            if project.timesheet_restriction_days < 0:
                raise ValidationError(
                    _(
                        "The number of days for timesheet restriction must not be negative."
                    )
                )
