# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from xlrd import open_workbook

from odoo import _

from odoo.addons.l10n_it_ricevute_bancarie.tests.riba_common import TestRibaCommon


class TestOutstandingStatement(TestRibaCommon):
    def setUp(self):
        super().setUp()
        self.statement_model = self.env[
            "report.partner_statement.outstanding_statement"
        ]
        self.wiz = self.env["outstanding.statement.wizard"]
        self.xlsx_report = self.env["ir.actions.report"]._get_report_from_name(
            "p_s.report_outstanding_statement_xlsx"
        )

    def test_show_unsolved_in_report(self):
        """If an invoice is linked to an unsolved RiBa,
        it is shown in the report."""
        # Arrange
        invoice, riba_list = self.riba_sbf_common(self.riba_config_sbf_immediate.id)
        partner = invoice.partner_id
        riba_line = riba_list.line_ids
        unsolved_wizard = (
            self.env["riba.unsolved"]
            .with_context(
                active_model=riba_line._name,
                active_ids=riba_line.ids,
                active_id=riba_line.id,
            )
            .create(
                {
                    "bank_amount": 455,
                    "past_due_fee_amount": 5,
                }
            )
        )
        unsolved_wizard.create_move()
        # pre-condition
        self.assertTrue(invoice.is_unsolved)
        self.assertTrue(invoice.unsolved_move_line_ids)

        # Act
        wizard = self.wiz.with_context(active_ids=partner.ids,).create(
            {
                "l10n_it_show_riba": True,
            }
        )
        data = wizard._prepare_statement()
        report = self.statement_model._get_report_values(partner.ids, data)

        # Assert
        move_lines = report["data"][partner.id]["currencies"][invoice.currency_id.id][
            "lines"
        ]
        move_line = next(filter(lambda ml: ml["move_id"] == invoice.name, move_lines))
        self.assertTrue(move_line["l10n_it_riba_payment"])

    def test_show_unsolved_in_xlsx_report(self):
        """If an invoice is linked to an unsolved RiBa,
        it is shown in the XLSX report."""
        # Arrange
        invoice, riba_list = self.riba_sbf_common(self.riba_config_sbf_immediate.id)
        partner = invoice.partner_id
        riba_line = riba_list.line_ids
        unsolved_wizard = (
            self.env["riba.unsolved"]
            .with_context(
                active_model=riba_line._name,
                active_ids=riba_line.ids,
                active_id=riba_line.id,
            )
            .create(
                {
                    "bank_amount": 455,
                    "past_due_fee_amount": 5,
                }
            )
        )
        unsolved_wizard.create_move()
        # pre-condition
        self.assertTrue(invoice.is_unsolved)
        self.assertTrue(invoice.unsolved_move_line_ids)

        # Act
        wizard = self.wiz.with_context(active_ids=partner.ids,).create(
            {
                "l10n_it_show_riba": True,
            }
        )
        data = wizard._prepare_statement()
        report = self.xlsx_report._render(partner.ids, data=data)

        # Assert
        sheet = open_workbook(file_contents=report[0]).sheet_by_index(0)
        # Look for the Riba column in the row of `invoice`
        riba_col = invoice_row = 0
        for row_pos in range(sheet.nrows):
            for col_pos in range(sheet.ncols):
                value = sheet.cell_value(row_pos, col_pos)
                if value == _("RiBa"):
                    riba_col = col_pos
                    break
                elif riba_col and value == invoice.name:
                    invoice_row = row_pos
                    break

            if riba_col and invoice_row:
                break
        else:
            self.fail("Riba column or invoice row not found")
        value = sheet.cell_value(invoice_row, riba_col)
        self.assertEqual(value, "X")
