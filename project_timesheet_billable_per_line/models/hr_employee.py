# Copyright 2026 Tecnativa - Eduardo Ezerouali
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrEmployee(models.AbstractModel):
    _inherit = "hr.employee.base"

    timesheet_billable_product_id = fields.Many2one(
        comodel_name="product.product", string="Timesheet Billable Product"
    )
