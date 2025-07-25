# Copyright (C) 2022 Trevi Software (https://trevi.et)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrEmployeePublic(models.Model):

    _inherit = "hr.employee.public"

    ethiopic_name = fields.Char(readonly=True)
