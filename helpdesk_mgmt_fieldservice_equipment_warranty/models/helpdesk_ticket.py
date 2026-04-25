# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HelpDeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    equipment_warranty_start_date = fields.Date(
        related="equipment_id.warranty_start_date",
        string="Equipment Warranty Start Date",
    )
    equipment_warranty_end_date = fields.Date(
        related="equipment_id.warranty_end_date",
        string="Equipment Warranty End Date",
    )
