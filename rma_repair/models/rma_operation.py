# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RmaOperation(models.Model):

    _inherit = "rma.operation"

    action_create_repair = fields.Selection(
        [
            ("manual_on_confirm", "Manually on Confirm"),
            ("automatic_on_confirm", "Automatically on Confirm"),
            ("manual_after_receipt", "Manually After Receipt"),
            ("automatic_after_receipt", "Automatically After Receipt"),
        ],
        string="Repair Action",
        help="Define how the repair action should be handled.",
    )
