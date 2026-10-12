from datetime import date, timedelta

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestExportValidation(TransactionCase):
    """Task 9: validações de exportação (moeda/câmbio/endereço do receptor)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        cls.country_py = cls.env.ref("base.py")
        cls.country_br = cls.env.ref("base.br")
        cls.usd = cls.env.ref("base.USD")
        cls.usd.active = True
        cls.company.write(
            {
                "country_id": cls.country_py.id,
                "account_fiscal_country_id": cls.country_py.id,
            }
        )
        cls.company.l10n_py_ruc = "80009401"

        cls.doc_type_fe = cls.env["l10n_latam.document.type"].search(
            [("country_id", "=", cls.country_py.id), ("code", "=", "1")],
            limit=1,
        )
        if not cls.doc_type_fe:
            cls.doc_type_fe = cls.env["l10n_latam.document.type"].create(
                {
                    "name": "Factura electrónica",
                    "code": "1",
                    "country_id": cls.country_py.id,
                    "internal_type": "invoice",
                }
            )

        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Ventas Export Test",
                "type": "sale",
                "code": "VEX",
                "company_id": cls.company.id,
                "l10n_latam_use_documents": True,
            }
        )

        today = date.today()
        cls.env["account.authorization"].create(
            {
                "name": "44556699",
                "date_from": today - timedelta(days=30),
                "date_to": today + timedelta(days=335),
                "invoice_number_from": 1,
                "invoice_number_to": 10000,
                "establishment": "001",
                "expedition_point": "001",
                "l10n_latam_document_type_id": cls.doc_type_fe.id,
                "company_id": cls.company.id,
            }
        )

    def _export_partner(self, street="Av. Exterior 123"):
        return self.env["res.partner"].create(
            {
                "name": "Cliente Exterior",
                "country_id": self.country_br.id,
                "street": street,
            }
        )

    def _export_invoice(
        self,
        currency="USD",
        exchange_rate=1.0,
        partner_street="Av. Exterior 123",
    ):
        partner = self._export_partner(street=partner_street)
        vals = {
            "move_type": "out_invoice",
            "partner_id": partner.id,
            "journal_id": self.journal.id,
            "l10n_latam_document_type_id": self.doc_type_fe.id,
            "l10n_py_exchange_rate": exchange_rate,
        }
        if currency == "USD":
            vals["currency_id"] = self.usd.id
        return self.env["account.move"].create(vals)

    def test_export_requires_exchange_rate_for_foreign_currency(self):
        """Exportación en USD sin tipo de cambio → UserError."""
        inv = self._export_invoice(currency="USD", exchange_rate=0)
        with self.assertRaises(UserError):
            inv._validate_edi_data()

    def test_export_requires_receptor_address(self):
        """Exportación sin dirección del receptor → UserError."""
        inv = self._export_invoice(partner_street=False)
        with self.assertRaises(UserError):
            inv._validate_edi_data()

    def test_export_document_type_errors_mention_export_causes(self):
        """Sin moneda extranjera+cambio, el error específico de exportación aparece."""
        inv = self._export_invoice(currency="USD", exchange_rate=0)
        errors = inv._validate_edi_document_type()
        self.assertTrue(
            any("tipo de cambio" in e for e in errors),
            errors,
        )

    def test_export_with_currency_rate_and_address_no_export_specific_error(self):
        """Con moneda extranjera+cambio válido y dirección, no hay error específico
        de exportación (aunque otras validaciones de _validate_edi_data puedan
        fallar por datos incompletos no relacionados)."""
        inv = self._export_invoice(currency="USD", exchange_rate=7300.0)
        errors = inv._validate_edi_document_type()
        self.assertFalse(errors, errors)

    def test_alpha3_for_uncovered_country(self):
        """Task 10: país fora da tabela hardcoded original (Vietnã) deve resolver
        corretamente, não cair no fallback (que devolveria o próprio code alpha-2)."""
        code = self.env["account.move"]._get_country_alpha3(self.env.ref("base.vn"))
        self.assertEqual(code, "VNM")

    def test_alpha3_for_uncovered_country_china(self):
        code = self.env["account.move"]._get_country_alpha3(self.env.ref("base.cn"))
        self.assertEqual(code, "CHN")

    def test_alpha3_for_uncovered_country_germany(self):
        code = self.env["account.move"]._get_country_alpha3(self.env.ref("base.de"))
        self.assertEqual(code, "DEU")

    def test_alpha3_for_already_covered_country_brazil(self):
        code = self.env["account.move"]._get_country_alpha3(self.env.ref("base.br"))
        self.assertEqual(code, "BRA")

    def test_alpha3_fallback_no_country(self):
        code = self.env["account.move"]._get_country_alpha3(self.env["res.country"])
        self.assertEqual(code, "PRY")
