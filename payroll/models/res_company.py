# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    payroll_structure_id = fields.Many2one(
        "hr.payroll.structure",
        string="Default Salary Structure",
    )
