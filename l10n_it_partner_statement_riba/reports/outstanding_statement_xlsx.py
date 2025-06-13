# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models

from odoo.addons.report_xlsx_helper.report.report_xlsx_format import FORMATS


class OutstandingStatementXslx(models.AbstractModel):
    _inherit = "report.p_s.report_outstanding_statement_xlsx"

    def _get_currency_header_row_data(self, partner, currency, data):
        row_data = super()._get_currency_header_row_data(partner, currency, data)
        if data["l10n_it_show_riba"]:
            last_col_pos = row_data[-1]["col_pos"]
            row_data.insert(
                -1,
                {
                    "col_pos": last_col_pos,
                    "sheet_func": "write",
                    "args": (_("RiBa"), FORMATS["format_theader_yellow_center"]),
                },
            )
            row_data[-1]["col_pos"] = last_col_pos + 1
        return row_data

    def _get_currency_line_row_data(self, partner, currency, data, line):
        row_data = super()._get_currency_line_row_data(partner, currency, data, line)
        if data["l10n_it_show_riba"]:
            if line.get("blocked"):
                format_distributed = FORMATS["format_distributed_blocked"]
            else:
                format_distributed = FORMATS["format_distributed"]

            move_line = self.env["account.move.line"].browse(line["id"])
            move = move_line.move_id
            # account.move.is_riba_payment cannot be included
            # because is not stored
            is_riba_open = move.is_riba_payment
            last_col_pos = row_data[-1]["col_pos"]
            row_data.insert(
                -1,
                {
                    "col_pos": last_col_pos,
                    "sheet_func": "write",
                    "args": ("X" if is_riba_open else "", format_distributed),
                },
            )
            row_data[-1]["col_pos"] = last_col_pos + 1
        return row_data

    def _get_currency_footer_row_data(self, partner, currency, data):
        row_data = super()._get_currency_footer_row_data(partner, currency, data)
        if data["l10n_it_show_riba"]:
            row_data[-1]["col_pos"] += 1
        return row_data
