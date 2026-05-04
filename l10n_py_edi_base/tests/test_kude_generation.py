import base64
from datetime import date, timedelta
from unittest.mock import ANY, MagicMock, patch

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestKudeGeneration(TransactionCase):
    """Tests for KUDE PDF generation via pykude."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        cls.country_py = cls.env.ref("base.py")
        cls.company.write(
            {
                "country_id": cls.country_py.id,
                "account_fiscal_country_id": cls.country_py.id,
            }
        )

        cls.doc_type_invoice = cls.env["l10n_latam.document.type"].search(
            [("country_id", "=", cls.country_py.id), ("code", "=", "1")],
            limit=1,
        )
        if not cls.doc_type_invoice:
            cls.doc_type_invoice = cls.env["l10n_latam.document.type"].create(
                {
                    "name": "Factura",
                    "code": "1",
                    "country_id": cls.country_py.id,
                    "internal_type": "invoice",
                }
            )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Cliente KuDE Test",
                "country_id": cls.country_py.id,
            }
        )

        cls.account_income = cls.env["account.account"].search(
            [
                ("company_id", "=", cls.company.id),
                ("account_type", "=", "income"),
            ],
            limit=1,
        )
        if not cls.account_income:
            cls.account_income = cls.env["account.account"].create(
                {
                    "name": "Ingresos",
                    "code": "400098",
                    "account_type": "income",
                    "company_id": cls.company.id,
                }
            )

        cls.account_receivable = cls.env["account.account"].search(
            [
                ("company_id", "=", cls.company.id),
                ("account_type", "=", "asset_receivable"),
            ],
            limit=1,
        )
        if not cls.account_receivable:
            cls.account_receivable = cls.env["account.account"].create(
                {
                    "name": "Cuentas por Cobrar",
                    "code": "110098",
                    "account_type": "asset_receivable",
                    "reconcile": True,
                    "company_id": cls.company.id,
                }
            )

        cls.partner.property_account_receivable_id = cls.account_receivable

        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Ventas KuDE",
                "type": "sale",
                "code": "VKD",
                "company_id": cls.company.id,
                "l10n_latam_use_documents": True,
            }
        )

        today = date.today()
        cls.authorization = cls.env["account.authorization"].create(
            {
                "name": "99887766",
                "date_from": today - timedelta(days=30),
                "date_to": today + timedelta(days=335),
                "invoice_number_from": 1,
                "invoice_number_to": 10000,
                "establishment": "001",
                "expedition_point": "001",
                "l10n_latam_document_type_id": cls.doc_type_invoice.id,
                "company_id": cls.company.id,
            }
        )

        cls.sample_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>' "<rDE><dVerFor>150</dVerFor></rDE>"
        )
        cls.sample_pdf = b"%PDF-1.4 fake pdf content for testing"

    def _create_invoice_with_xml(self, cdc="0" * 43):
        """Helper: create posted invoice with fake XML and CDC."""
        move = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner.id,
                "journal_id": self.journal.id,
                "l10n_py_authorization_id": self.authorization.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Producto Test",
                            "quantity": 1,
                            "price_unit": 100000.0,
                            "account_id": self.account_income.id,
                            "tax_ids": [(6, 0, [])],
                        },
                    )
                ],
            }
        )
        move.action_post()
        move.write(
            {
                "l10n_py_cdc": cdc,
                "l10n_py_edi_xml": base64.b64encode(self.sample_xml.encode("utf-8")),
                "l10n_py_edi_xml_filename": f"{cdc}.xml",
                "l10n_py_edi_status": "accepted",
            }
        )
        return move

    @patch("pykude.auto_kude")
    def test_generate_kude_calls_pykude(self, mock_auto_kude):
        """_generate_kude calls pykude.auto_kude with XML content."""
        mock_kude_obj = MagicMock()
        mock_kude_obj.output.return_value = self.sample_pdf
        mock_auto_kude.return_value = mock_kude_obj

        move = self._create_invoice_with_xml()
        move._generate_kude()

        mock_auto_kude.assert_called_once_with(xml=self.sample_xml, config=ANY)
        mock_kude_obj.output.assert_called_once()

    @patch("pykude.auto_kude")
    def test_generate_kude_stores_pdf(self, mock_auto_kude):
        """_generate_kude stores base64 PDF and filename on the invoice."""
        mock_kude_obj = MagicMock()
        mock_kude_obj.output.return_value = self.sample_pdf
        mock_auto_kude.return_value = mock_kude_obj

        cdc = "1" * 43
        move = self._create_invoice_with_xml(cdc=cdc)
        move._generate_kude()

        self.assertTrue(move.l10n_py_kude_pdf)
        pdf_decoded = base64.b64decode(move.l10n_py_kude_pdf)
        self.assertEqual(pdf_decoded, self.sample_pdf)
        self.assertEqual(move.l10n_py_kude_filename, f"KUDE_{cdc}.pdf")

    def test_generate_kude_no_xml_skips(self):
        """_generate_kude does nothing when no XML is present."""
        move = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": self.partner.id,
                "journal_id": self.journal.id,
                "l10n_py_authorization_id": self.authorization.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Producto Test",
                            "quantity": 1,
                            "price_unit": 100000.0,
                            "account_id": self.account_income.id,
                            "tax_ids": [(6, 0, [])],
                        },
                    )
                ],
            }
        )
        move.action_post()
        move._generate_kude()

        self.assertFalse(move.l10n_py_kude_pdf)
        self.assertFalse(move.l10n_py_kude_filename)

    @patch("pykude.auto_kude")
    def test_generate_kude_decodes_xml_correctly(self, mock_auto_kude):
        """_generate_kude decodes base64 XML before passing to pykude."""
        mock_kude_obj = MagicMock()
        mock_kude_obj.output.return_value = self.sample_pdf
        mock_auto_kude.return_value = mock_kude_obj

        xml_with_accents = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            "<rDE><dNomEmi>Compañía Test SA</dNomEmi></rDE>"
        )
        move = self._create_invoice_with_xml()
        move.l10n_py_edi_xml = base64.b64encode(xml_with_accents.encode("utf-8"))
        move._generate_kude()

        mock_auto_kude.assert_called_once_with(xml=xml_with_accents, config=ANY)

    @patch("pykude.auto_kude")
    def test_generate_kude_error_propagates(self, mock_auto_kude):
        """_generate_kude propagates pykude errors."""
        mock_auto_kude.side_effect = ValueError("Invalid XML structure")

        move = self._create_invoice_with_xml()
        with self.assertRaises(ValueError):
            move._generate_kude()

    @patch("pykude.auto_kude")
    def test_process_edi_response_generates_kude(self, mock_auto_kude):
        """_process_edi_response auto-generates KuDE after accepting."""
        mock_kude_obj = MagicMock()
        mock_kude_obj.output.return_value = self.sample_pdf
        mock_auto_kude.return_value = mock_kude_obj

        cdc = "2" * 43
        xml_str = "<rDE><dVerFor>150</dVerFor></rDE>"

        move = self._create_invoice_with_xml()
        move.l10n_py_edi_xml = False  # Clear so _process_edi_response sets it

        response = {
            "success": True,
            "result": {
                "deList": [{"cdc": cdc, "xml": xml_str}],
            },
        }
        move._process_edi_response(response)

        self.assertEqual(move.l10n_py_cdc, cdc)
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        mock_auto_kude.assert_called_once()

    @patch("pykude.auto_kude")
    def test_process_edi_response_kude_error_non_blocking(self, mock_auto_kude):
        """KuDE generation error should not block EDI acceptance."""
        mock_auto_kude.side_effect = RuntimeError("pykude crash")

        cdc = "3" * 43
        xml_str = "<rDE><dVerFor>150</dVerFor></rDE>"

        move = self._create_invoice_with_xml()
        response = {
            "success": True,
            "result": {
                "deList": [{"cdc": cdc, "xml": xml_str}],
            },
        }
        # Should NOT raise — KuDE error is logged as warning
        move._process_edi_response(response)

        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertFalse(move.l10n_py_kude_pdf)
