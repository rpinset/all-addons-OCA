# Copyright 2025 CamptoCamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from unittest.mock import MagicMock, patch

from odoo.tests import TransactionCase
from odoo.tests.common import tagged

from odoo.addons.queue_job.tests.common import trap_jobs


@tagged("post_install", "-at_install")
class TestAccountInvoiceMassSendingDirectPrint(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                queue_job__no_delay=True,
            )
        )

    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create(
            {"name": "Test Partner", "email": "test@example.com"}
        )
        self.invoice = self.env["account.move"].create(
            {
                "partner_id": self.partner.id,
                "move_type": "out_invoice",
                "invoice_date": "2023-01-01",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Test Product",
                            "quantity": 1,
                            "price_unit": 100,
                        },
                    )
                ],
            }
        )
        self.action_report = self.env.ref("account.account_invoices")
        self.report = self.env.ref(self.action_report.report_file)
        self.server = self.env["printing.server"].create({})

    def new_printer(self):
        return self.env["printing.printer"].create(
            {
                "name": "Printer",
                "server_id": self.server.id,
                "system_name": "Sys Name",
                "default": True,
                "status": "unknown",
                "status_message": "Msg",
                "model": "res.users",
                "location": "Location",
                "uri": "URI",
            }
        )

    def test_mass_sending_with_direct_print(self):
        """Test mass sending with direct print."""
        self.env = self.env(
            context=dict(
                self.env.context,
                queue_job__no_delay=False,
            )
        )
        self.invoice.write({"sending_in_progress": False})
        with trap_jobs() as trap:
            wizard = (
                self.env["account.invoice.send"]
                .with_context(active_ids=self.invoice.ids)
                .create(
                    {
                        "is_print": True,
                        "is_email": False,
                        "is_direct_print": True,
                    }
                )
            )
            result = wizard.enqueue_invoices()
            self.assertTrue(result)
            trap.assert_jobs_count(1)

    def test_mass_sending_with_direct_print_no_printer(self):
        """Test mass sending with direct print and no printer available."""
        with self.assertRaises(ValueError) as error:
            self.invoice.with_context(
                account_invoice_mass_sending=False
            )._send_invoice_individually(is_direct_print=True, is_print=True)
        self.assertEqual(error.exception.args[0], "No printer found for the report.")

    def test_mass_sending_with_printer_mock(self):
        """Test mass sending with direct print and mock printer interaction."""
        self.invoice.write({"sending_in_progress": False})
        with patch(
            "odoo.addons.base_report_to_printer.models."
            "ir_actions_report.IrActionsReport._render_qweb_pdf"
        ) as mock_render_pdf:
            wizard = (
                self.env["account.invoice.send"]
                .with_context(active_ids=self.invoice.ids)
                .create(
                    {
                        "is_print": True,
                        "is_email": False,
                        "is_direct_print": True,
                    }
                )
            )
            result = wizard.enqueue_invoices()
            self.assertTrue(result)
            self.assertFalse(self.invoice.sending_in_progress)
            mock_render_pdf.assert_called_once_with(
                self.action_report.report_name, res_ids=[self.invoice.id], data=None
            )

    @patch("cups.Connection")
    def test_render_qweb_pdf_with_direct_print(self, mock_cups_connection):
        """Test print pdf report using `is_direct_print` option"""
        mock_conn = MagicMock()
        mock_cups_connection.return_value = mock_conn
        with patch(
            "odoo.addons.base_report_to_printer.models."
            "printing_printer.PrintingPrinter."
            "print_document"
        ) as print_document:
            # Modify the action type of the printing action to client to bypass `print_document`
            self.action_report.property_printing_action_id.action_type = "client"
            self.action_report.printing_printer_id = self.new_printer()

            # Create the wizard and call the method to print directly
            wizard = (
                self.env["account.invoice.send"]
                .with_context(active_ids=self.invoice.ids)
                .create(
                    {
                        "is_print": True,
                        "is_email": False,
                        "is_direct_print": True,
                    }
                )
            )
            result = wizard.enqueue_invoices()
            self.assertTrue(result)

            # Use _render_qweb_pdf to create a document for inspection
            # This action will not access `print_document`.
            # Because self.action_report.property_printing_action_id.action_type = "client"
            document = self.action_report._render_qweb_pdf(
                self.action_report.report_name, self.invoice.ids
            )

            # Check that the print_document method was called with the correct parameters
            print_document.assert_called_once_with(
                self.action_report,
                document[0],
                action="server",
                doc_format="qweb-pdf",
                tray=False,
            )
