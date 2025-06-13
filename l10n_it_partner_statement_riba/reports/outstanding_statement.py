# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class OutstandingStatementReport(models.AbstractModel):
    _inherit = "report.partner_statement.outstanding_statement"

    @api.model
    def _l10n_it_riba_inject_report_values(self, report_values):
        """Include in `report_values` values for RiBa."""
        for _partner_id, partner_data in report_values["data"].items():
            currencies = partner_data.get("currencies", {})
            for _currency_id, currency_data in currencies.items():
                for line in currency_data.get("lines", []):
                    move_line = self.env["account.move.line"].browse(line["id"])
                    move = move_line.move_id
                    # account.move.is_riba_payment cannot be included
                    # because is not stored
                    line["l10n_it_riba_payment"] = move.is_riba_payment
        return report_values

    @api.model
    def _get_report_values(self, docids, data=None):
        report_values = super()._get_report_values(docids, data=data)
        report_values["l10n_it_show_riba"] = data["l10n_it_show_riba"]
        if report_values["l10n_it_show_riba"]:
            report_values = self._l10n_it_riba_inject_report_values(
                report_values,
            )
        return report_values
