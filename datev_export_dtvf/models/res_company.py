# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    datev_account_code_length = fields.Integer(
        "DATEV account code length",
        default=5,
    )

    datev_partner_numbering = fields.Selection(
        string="DATEV Partner numbering",
        selection="_selection_datev_partner_numbering",
        default="none",
    )

    datev_customer_sequence_id = fields.Many2one(
        "ir.sequence", "DATEV sequence for customers"
    )

    datev_supplier_sequence_id = fields.Many2one(
        "ir.sequence", "DATEV sequence for suppliers"
    )

    def _selection_datev_partner_numbering(self):
        reports_installed = (
            "l10n_de_datev_reports" in self.env["ir.module.module"]._installed()
        )
        return (
            [("none", "None")]
            + ([("ee", "Enterprises Edition")] if reports_installed else [])
            + [("sequence", "Sequence")]
        )
