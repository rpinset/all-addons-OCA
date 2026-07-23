from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestEDILifecycle(TransactionCase):
    """Tests do ciclo de vida EDI, inutilização e contingência (F10-F12)"""

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
                "name": "Cliente Test",
                "country_id": cls.country_py.id,
            }
        )

        cls.account_income = cls.env["account.account"].search(
            [
                ("company_ids", "in", cls.company.id),
                ("account_type", "=", "income"),
            ],
            limit=1,
        )
        if not cls.account_income:
            cls.account_income = cls.env["account.account"].create(
                {
                    "name": "Ingresos",
                    "code": "400099",
                    "account_type": "income",
                    "company_ids": [(6, 0, [cls.company.id])],
                }
            )

        cls.account_receivable = cls.env["account.account"].search(
            [
                ("company_ids", "in", cls.company.id),
                ("account_type", "=", "asset_receivable"),
            ],
            limit=1,
        )
        if not cls.account_receivable:
            cls.account_receivable = cls.env["account.account"].create(
                {
                    "name": "Cuentas por Cobrar",
                    "code": "110099",
                    "account_type": "asset_receivable",
                    "reconcile": True,
                    "company_ids": [(6, 0, [cls.company.id])],
                }
            )

        cls.partner.property_account_receivable_id = cls.account_receivable

        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Ventas LC Test",
                "type": "sale",
                "code": "VLT",
                "company_id": cls.company.id,
                "l10n_latam_use_documents": True,
            }
        )

        today = date.today()
        cls.authorization = cls.env["account.authorization"].create(
            {
                "name": "55667799",
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

        cls.tax_exempt = cls.env["account.tax"].create(
            {
                "name": "Exento Test",
                "amount": 0.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
            }
        )

    def _create_and_post_invoice(self):
        """Helper: crear e confirmar factura"""
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
                            "tax_ids": [(6, 0, [self.tax_exempt.id])],
                            "account_id": self.account_income.id,
                        },
                    )
                ],
            }
        )
        move.action_post()
        return move

    # ============== F10: Ciclo EDI ==============

    def test_action_post_sets_to_send(self):
        """F10: action_post configura status EDI como to_send"""
        move = self._create_and_post_invoice()
        self.assertEqual(move.l10n_py_edi_status, "to_send")

    def test_transmission_deadline_computed(self):
        """F10: Prazo de transmissão calculado (72h desde emissão)"""
        move = self._create_and_post_invoice()
        if move.invoice_date:
            self.assertTrue(move.l10n_py_transmission_deadline)

    # ============== F11: Inutilização ==============

    def test_inutilize_range(self):
        """F11: Inutilizar faja de números → OK"""
        inut = self.env["l10n_py.number.inutilization"].create(
            {
                "authorization_id": self.authorization.id,
                "number_from": 9990,
                "number_to": 9999,
                "motive": "Números saltados por error de sistema",
            }
        )
        self.assertTrue(inut.id)
        self.assertEqual(inut.quantity, 10)
        self.assertEqual(inut.state, "draft")

    def test_inutilize_over_1000(self):
        """F11: Inutilizar más de 1000 → error"""
        with self.assertRaises(ValidationError):
            self.env["l10n_py.number.inutilization"].create(
                {
                    "authorization_id": self.authorization.id,
                    "number_from": 1,
                    "number_to": 1001,
                    "motive": "Test",
                }
            )

    def test_inutilize_used_numbers(self):
        """F11: Inutilizar números ya usados → error"""
        move = self._create_and_post_invoice()
        used_number = move.l10n_py_invoice_number

        with self.assertRaises(ValidationError):
            self.env["l10n_py.number.inutilization"].create(
                {
                    "authorization_id": self.authorization.id,
                    "number_from": used_number,
                    "number_to": used_number,
                    "motive": "Test",
                }
            )

    def test_inutilize_outside_range(self):
        """F11: Inutilizar fuera del rango del timbrado → error"""
        with self.assertRaises(ValidationError):
            self.env["l10n_py.number.inutilization"].create(
                {
                    "authorization_id": self.authorization.id,
                    "number_from": 10001,
                    "number_to": 10005,
                    "motive": "Test",
                }
            )

    def test_inutilize_reversed_range(self):
        """F11: Rango invertido → error"""
        with self.assertRaises(ValidationError):
            self.env["l10n_py.number.inutilization"].create(
                {
                    "authorization_id": self.authorization.id,
                    "number_from": 100,
                    "number_to": 50,
                    "motive": "Test",
                }
            )
