# l10n_py_edi_base/tests/test_edi_validation.py

from datetime import date, timedelta

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestEDIValidation(TransactionCase):
    """Tests para validación de datos EDI"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country_py = cls.env.ref("base.py")

        # Tipo de documento
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

        # Empresa
        cls.company = cls.env["res.company"].create(
            {
                "name": "Test Company EDI",
                "country_id": cls.country_py.id,
                "l10n_py_ruc": "80009401",
            }
        )

        # Partner
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "is_company": True,
                "country_id": cls.country_py.id,
                "l10n_py_ruc": "80009401",
                "l10n_py_taxpayer_type": "1",
                "street": "Test Street 123",
            }
        )

        # Timbrado
        today = date.today()
        cls.authorization = cls.env["account.authorization"].create(
            {
                "name": "12345678",
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

        # Journal
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Test Journal EDI",
                "type": "sale",
                "code": "TEDI",
                "company_id": cls.company.id,
                "l10n_py_establishment": "001",
                "l10n_py_point": "001",
                "l10n_py_authorization_id": cls.authorization.id,
            }
        )

        # Producto
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
                "default_code": "TEST001",
                "l10n_py_ncm_code": "01012100",
            }
        )

    def test_security_code_generation(self):
        """Código de seguridad de 9 dígitos"""
        invoice = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "out_invoice",
                    "partner_id": self.partner.id,
                    "journal_id": self.journal.id,
                    "company_id": self.company.id,
                }
            )
        )

        security_code = invoice._generate_security_code()
        self.assertEqual(len(security_code), 9)
        self.assertTrue(security_code.isdigit())

    def test_edi_status_default(self):
        """Estado EDI por defecto es 'draft'"""
        invoice = (
            self.env["account.move"]
            .with_company(self.company)
            .create(
                {
                    "move_type": "out_invoice",
                    "partner_id": self.partner.id,
                    "journal_id": self.journal.id,
                    "company_id": self.company.id,
                }
            )
        )
        self.assertEqual(invoice.l10n_py_edi_status, "draft")
