# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Employee(models.Model):
    _inherit = "hr.employee"

    no_payroll_encryption = fields.Boolean(
        string="Disable payrolls encryption",
        help="If this is disabled (default), "
        "the PDF payrolls are encrypted using the Identification No.\n"
        "Only future payrolls are affected by this change, "
        "existing payrolls will not change their encryption status.",
        groups="hr.group_hr_user",
    )

    def _validate_payroll_identification(self, code=None):
        # Override if the identification should be validated in another way
        if code is None and len(self) == 1:
            code = self.identification_id
        if country_code := self.env.company.country_id.code:
            is_valid = self.env["res.partner"].simple_vat_check(country_code, code)
        else:
            is_valid = True
        return is_valid

    @api.constrains("identification_id")
    def _constrain_payroll_identification(self):
        # Only check the employees that have an `identification_id`
        for employee in self.filtered("identification_id"):
            if not employee._validate_payroll_identification():
                raise ValidationError(_("The field identification ID is not valid"))
