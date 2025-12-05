# Copyright 2022 Giuseppe Borruso
# Copyright 2025 Simone Rubino - PyTech
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64
import io
from datetime import datetime

from dateutil.rrule import MONTHLY

from odoo.tests.common import Form, tagged
from odoo.tools import pdf

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestCentralJournalReportlab(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.today = datetime.now()
        cls.range_type = cls.env["date.range.type"].create({"name": "Fiscal year"})
        cls.env["date.range.generator"].create(
            {
                "date_start": "%s-01-01" % cls.today.year,
                "name_prefix": "%s-" % cls.today.year,
                "type_id": cls.range_type.id,
                "duration_count": 1,
                "unit_of_time": str(MONTHLY),
                "count": 12,
            }
        ).action_apply()
        cls.current_period = cls.env["date.range"].search(
            [
                ("date_start", "<=", cls.today.date()),
                ("date_end", ">=", cls.today.date()),
            ]
        )
        cls.wizard_model = cls.env["wizard.giornale.reportlab"]
        cls.report_model = cls.env["ir.actions.report"]
        cls.report_name = "l10n_it_central_journal_reportlab.report_giornale_reportlab"
        cls.journals = cls.env["account.journal"].search([])
        cls.invoice = cls.init_invoice(
            "out_invoice", amounts=[100], invoice_date=cls.today, post=True
        )

    def test_wizard_reportlab(self):
        wizard_form = Form(self.wizard_model)
        wizard_form.daterange_id = self.current_period
        wizard = wizard_form.save()
        self.assertEqual(
            len(wizard.journal_ids),
            len(self.journals.filtered(lambda j: not j.central_journal_exclude)),
        )
        self.assertEqual(wizard.date_move_line_from, self.current_period.date_start)
        self.assertEqual(wizard.date_move_line_to, self.current_period.date_end)
        self.assertEqual(wizard.year_footer, str(self.today.year))
        next_year = self.today.year + 1

        wizard.year_footer = next_year
        wizard.fiscal_page_base = 99

        wizard.print_giornale_reportlab()
        decode_giornale = base64.b64decode(wizard.report_giornale)
        self.minimal_reader_buffer = io.BytesIO(decode_giornale)
        self.minimal_pdf_reader = pdf.OdooPdfFileReader(self.minimal_reader_buffer)
        self.assertTrue(self.minimal_reader_buffer)

    def _get_report_content(self, wizard):
        pdf_content = base64.b64decode(wizard.report_giornale)
        pdf_reader = pdf.OdooPdfFileReader(io.BytesIO(pdf_content))
        content = ""
        for page in pdf_reader.pages:
            content += page.extractText()
        return content

    def test_grouped_report(self):
        # Arrange
        wizard_form = Form(self.wizard_model)
        wizard_form.daterange_id = self.current_period
        wizard_form.group_by_account = True
        wizard = wizard_form.save()
        wizard.year_footer = self.today.year + 1
        wizard.fiscal_page_base = 99
        invoice = self.invoice
        line_ref = "Test Reference"
        invoice.invoice_line_ids.ref = line_ref

        # Act
        wizard.print_giornale_reportlab()

        # Assert
        content = self._get_report_content(wizard)
        self.assertIn(line_ref, content)
        self.assertIn(invoice.partner_id.name, content)

    def _init_move(self, account, amounts, move_vals):
        default_move_vals = {
            "move_type": "entry",
            "date": self.today,
            "journal_id": self.company_data["default_journal_misc"].id,
            "line_ids": [],
        }
        for amount in amounts:
            default_move_vals["line_ids"].append(
                (
                    0,
                    0,
                    {
                        "account_id": account.id,
                        "credit": amount,
                    },
                )
            )
            default_move_vals["line_ids"].append(
                (
                    0,
                    0,
                    {
                        "account_id": account.id,
                        "debit": amount,
                    },
                )
            )

        default_move_vals.update(move_vals)
        move = self.env["account.move"].create(default_move_vals)
        move.action_post()
        return move

    def test_show_ref_grouped_report(self):
        """In the grouped report
        that has "Only show description for purchase and sale move lines" enabled,
        the description of a move is shown accordingly."""
        # Arrange
        wizard_form = Form(self.wizard_model)
        wizard_form.daterange_id = self.current_period
        wizard_form.group_by_account = True
        wizard_form.only_show_purchase_sale_ref = True
        wizard = wizard_form.save()
        invoice = self.invoice
        invoice.ref = "Test invoice ref"
        move = self._init_move(
            self.company_data["default_account_expense"],
            [100],
            {
                "ref": "Test move ref",
            },
        )
        # pre-condition
        self.assertIn(invoice.journal_id.type, ("purchase", "sale"))
        self.assertNotIn(move.journal_id.type, ("purchase", "sale"))

        # Act
        wizard.print_giornale_reportlab()

        # Assert
        content = self._get_report_content(wizard)
        self.assertNotIn(move.ref, content)
        self.assertIn(invoice.ref, content)

    def test_hide_ref_grouped_report(self):
        """In the grouped report
        that has "Only show description for purchase and sale move lines" disabled (default),
        the description of a move is shown accordingly."""
        # Arrange
        wizard_form = Form(self.wizard_model)
        wizard_form.daterange_id = self.current_period
        wizard_form.group_by_account = True
        wizard = wizard_form.save()
        invoice = self.invoice
        invoice.ref = "Test invoice ref"
        move = self._init_move(
            self.company_data["default_account_expense"],
            [100],
            {
                "ref": "Test move ref",
            },
        )
        # pre-condition
        self.assertFalse(wizard_form.only_show_purchase_sale_ref)
        self.assertIn(invoice.journal_id.type, ("purchase", "sale"))
        self.assertNotIn(move.journal_id.type, ("purchase", "sale"))

        # Act
        wizard.print_giornale_reportlab()

        # Assert
        content = self._get_report_content(wizard)
        self.assertIn(move.ref, content)
        self.assertIn(invoice.ref, content)

    def test_show_ref_report(self):
        """In the report
        that has "Only show description for purchase and sale move lines" enabled,
        the description of a move is shown accordingly."""
        # Arrange
        wizard_form = Form(self.wizard_model)
        wizard_form.daterange_id = self.current_period
        wizard_form.only_show_purchase_sale_ref = True
        wizard = wizard_form.save()
        invoice = self.invoice
        invoice.ref = "Test invoice ref"
        move = self._init_move(
            self.company_data["default_account_expense"],
            [100],
            {
                "ref": "Test move ref",
            },
        )
        # pre-condition
        self.assertFalse(wizard.group_by_account)
        self.assertIn(invoice.journal_id.type, ("purchase", "sale"))
        self.assertNotIn(move.journal_id.type, ("purchase", "sale"))

        # Act
        wizard.print_giornale_reportlab()

        # Assert
        content = self._get_report_content(wizard)
        self.assertNotIn(move.ref, content)
        self.assertIn(invoice.ref, content)

    def test_hide_ref_report(self):
        """In the report
        that has "Only show description for purchase and sale move lines" disabled (default),
        the description of a move is shown accordingly."""
        # Arrange
        wizard_form = Form(self.wizard_model)
        wizard_form.daterange_id = self.current_period
        wizard = wizard_form.save()
        invoice = self.invoice
        invoice.ref = "Test invoice ref"
        move = self._init_move(
            self.company_data["default_account_expense"],
            [100],
            {
                "ref": "Test move ref",
            },
        )
        # pre-condition
        self.assertFalse(wizard.group_by_account)
        self.assertFalse(wizard_form.only_show_purchase_sale_ref)
        self.assertIn(invoice.journal_id.type, ("purchase", "sale"))
        self.assertNotIn(move.journal_id.type, ("purchase", "sale"))

        # Act
        wizard.print_giornale_reportlab()

        # Assert
        content = self._get_report_content(wizard)
        self.assertIn(move.ref, content)
        self.assertIn(invoice.ref, content)
