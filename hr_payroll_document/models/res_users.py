# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

from odoo.addons.hr.models.res_users import HR_WRITABLE_FIELDS

HR_WRITABLE_FIELDS.append("no_payroll_encryption")


class ResUsers(models.Model):
    _inherit = "res.users"

    no_payroll_encryption = fields.Boolean(
        related="employee_id.no_payroll_encryption",
        readonly=False,
        related_sudo=False,
    )
