from datetime import date, timedelta

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestAccountMove(TransactionCase):
    """Tests para account.move (extensión paraguaya) — Cenários BDD"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.AccountMove = cls.env["account.move"]
        cls.Authorization = cls.env["account.authorization"]
        cls.Partner = cls.env["res.partner"]
        cls.Product = cls.env["product.product"]
        cls.Tax = cls.env["account.tax"]
        cls.Journal = cls.env["account.journal"]

        cls.company = cls.env.ref("base.main_company")
        cls.country_py = cls.env.ref("base.py")

        # Configurar empresa como paraguaya
        cls.company.write(
            {
                "country_id": cls.country_py.id,
                "account_fiscal_country_id": cls.country_py.id,
            }
        )

        # Tipo de documento factura
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

        # Cuentas contables
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
                    "name": "Ingresos por Ventas",
                    "code": "400001",
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
                    "code": "110001",
                    "account_type": "asset_receivable",
                    "reconcile": True,
                    "company_id": cls.company.id,
                }
            )

        # Journal de ventas (con LATAM documents habilitado)
        # Crear journal propio para evitar conflictos con journals que ya
        # tienen facturas confirmadas (no se puede cambiar use_documents)
        cls.journal = cls.Journal.create(
            {
                "name": "Ventas PY Test",
                "type": "sale",
                "code": "VPT",
                "company_id": cls.company.id,
                "l10n_latam_use_documents": True,
            }
        )

        # Timbrado válido
        today = date.today()
        cls.authorization = cls.Authorization.create(
            {
                "name": "33445566",
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

        # Cliente
        cls.partner = cls.Partner.create(
            {
                "name": "Cliente Test PY",
                "country_id": cls.country_py.id,
                "property_account_receivable_id": cls.account_receivable.id,
                "property_account_payable_id": cls.account_receivable.id,
            }
        )

        # Impuestos (incluidos en el precio para SIFEN)
        cls.tax_10 = cls.Tax.create(
            {
                "name": "IVA 10%",
                "amount": 10.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "price_include": True,
            }
        )
        cls.tax_5 = cls.Tax.create(
            {
                "name": "IVA 5%",
                "amount": 5.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "price_include": True,
            }
        )
        cls.tax_exempt = cls.Tax.create(
            {
                "name": "Exento",
                "amount": 0.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
            }
        )

        # Productos
        cls.product_10 = cls.Product.create(
            {
                "name": "Producto IVA 10%",
                "list_price": 1100.0,
                "taxes_id": [(6, 0, [cls.tax_10.id])],
            }
        )
        cls.product_5 = cls.Product.create(
            {
                "name": "Producto IVA 5%",
                "list_price": 525.0,
                "taxes_id": [(6, 0, [cls.tax_5.id])],
            }
        )
        cls.product_exempt = cls.Product.create(
            {
                "name": "Producto Exento",
                "list_price": 100.0,
                "taxes_id": [(6, 0, [cls.tax_exempt.id])],
            }
        )

    def _create_invoice(self, products_prices=None, **kwargs):
        """Helper para crear factura de prueba.

        products_prices: lista de tuplas (product, tax, price_unit)
        """
        if products_prices is None:
            products_prices = [
                (self.product_10, self.tax_10, 1100.0),
            ]

        lines = []
        for product, tax, price in products_prices:
            lines.append(
                (
                    0,
                    0,
                    {
                        "product_id": product.id,
                        "quantity": 1,
                        "price_unit": price,
                        "tax_ids": [(6, 0, [tax.id])],
                        "account_id": self.account_income.id,
                    },
                )
            )

        vals = {
            "move_type": "out_invoice",
            "partner_id": self.partner.id,
            "journal_id": self.journal.id,
            "l10n_py_authorization_id": self.authorization.id,
            "invoice_line_ids": lines,
        }
        vals.update(kwargs)
        return self.AccountMove.create(vals)

    # ============== F02: Número ao confirmar ==============

    def test_action_post_assigns_first_number(self):
        """F02: Confirmar factura asigna número = 1 (primer uso del timbrado)"""
        invoice = self._create_invoice()
        self.assertFalse(invoice.l10n_py_invoice_number)
        invoice.action_post()
        self.assertEqual(invoice.l10n_py_invoice_number, 1)
        self.assertEqual(invoice.l10n_py_full_invoice_number, "001-001-0000001")

    def test_action_post_sequential(self):
        """F02: 3 facturas confirmadas → números 1, 2, 3"""
        invoices = []
        for _i in range(3):
            inv = self._create_invoice()
            inv.action_post()
            invoices.append(inv)

        self.assertEqual(invoices[0].l10n_py_invoice_number, 1)
        self.assertEqual(invoices[1].l10n_py_invoice_number, 2)
        self.assertEqual(invoices[2].l10n_py_invoice_number, 3)

    def test_action_post_exhausted_range(self):
        """F02: Faja agotada → UserError"""
        # Crear timbrado con rango mínimo
        today = date.today()
        auth_small = self.Authorization.create(
            {
                "name": "99999999",
                "date_from": today - timedelta(days=30),
                "date_to": today + timedelta(days=335),
                "invoice_number_from": 1,
                "invoice_number_to": 2,
                "establishment": "001",
                "expedition_point": "001",
                "l10n_latam_document_type_id": self.doc_type_invoice.id,
                "company_id": self.company.id,
            }
        )

        # Usar los 2 números disponibles
        inv1 = self._create_invoice(l10n_py_authorization_id=auth_small.id)
        inv1.action_post()
        inv2 = self._create_invoice(l10n_py_authorization_id=auth_small.id)
        inv2.action_post()

        # Tercera factura debe fallar
        inv3 = self._create_invoice(l10n_py_authorization_id=auth_small.id)
        with self.assertRaises(UserError):
            inv3.action_post()

    def test_sale_requires_timbrado(self):
        """F02: Factura de venta sin timbrado → UserError al confirmar"""
        invoice = self._create_invoice(l10n_py_authorization_id=False)
        with self.assertRaises(UserError):
            invoice.action_post()

    def test_purchase_no_timbrado_required(self):
        """F02: Factura de compra sin timbrado → OK (no requiere timbrado propio)"""
        account_payable = self.env["account.account"].search(
            [
                ("company_id", "=", self.company.id),
                ("account_type", "=", "liability_payable"),
            ],
            limit=1,
        )
        if not account_payable:
            account_payable = self.env["account.account"].create(
                {
                    "name": "Cuentas por Pagar",
                    "code": "210001",
                    "account_type": "liability_payable",
                    "reconcile": True,
                    "company_id": self.company.id,
                }
            )

        expense_account = self.env["account.account"].search(
            [
                ("company_id", "=", self.company.id),
                ("account_type", "=", "expense"),
            ],
            limit=1,
        )
        if not expense_account:
            expense_account = self.env["account.account"].create(
                {
                    "name": "Gastos",
                    "code": "500001",
                    "account_type": "expense",
                    "company_id": self.company.id,
                }
            )

        # Create a purchase journal without LATAM documents for this test
        journal_purchase = self.Journal.create(
            {
                "name": "Compras Test",
                "type": "purchase",
                "code": "CMT",
                "company_id": self.company.id,
                "l10n_latam_use_documents": False,
            }
        )

        vendor = self.Partner.create(
            {
                "name": "Proveedor Test",
                "property_account_payable_id": account_payable.id,
                "property_account_receivable_id": self.account_receivable.id,
            }
        )

        purchase_invoice = self.AccountMove.create(
            {
                "move_type": "in_invoice",
                "partner_id": vendor.id,
                "journal_id": journal_purchase.id,
                "invoice_date": date.today(),
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_exempt.id,
                            "quantity": 1,
                            "price_unit": 100.0,
                            "account_id": expense_account.id,
                            "tax_ids": [(6, 0, [])],
                        },
                    )
                ],
            }
        )
        # No debe lanzar error — compra no requiere timbrado
        purchase_invoice.action_post()
        self.assertEqual(purchase_invoice.state, "posted")

    # ============== F09 / F03: IVA SIFEN ==============

    def test_iva_10_sifen_formula(self):
        """F09: Item Gs 1.100.000 con 10% → base=1.000.000, IVA=100.000"""
        invoice = self._create_invoice(
            products_prices=[
                (self.product_10, self.tax_10, 1100000.0),
            ]
        )
        self.assertAlmostEqual(invoice.l10n_py_amount_subtotal_10, 1100000.0, places=0)
        self.assertAlmostEqual(invoice.l10n_py_base_10, 1000000.0, places=0)
        self.assertAlmostEqual(invoice.l10n_py_amount_iva_10, 100000.0, places=0)

    def test_iva_5_sifen_formula(self):
        """F09: Item Gs 525.000 con 5% → base=500.000, IVA=25.000"""
        invoice = self._create_invoice(
            products_prices=[
                (self.product_5, self.tax_5, 525000.0),
            ]
        )
        self.assertAlmostEqual(invoice.l10n_py_amount_subtotal_5, 525000.0, places=0)
        self.assertAlmostEqual(invoice.l10n_py_base_5, 500000.0, places=0)
        self.assertAlmostEqual(invoice.l10n_py_amount_iva_5, 25000.0, places=0)

    def test_iva_exempt(self):
        """F09: Valor exento calculado"""
        invoice = self._create_invoice(
            products_prices=[
                (self.product_exempt, self.tax_exempt, 100000.0),
            ]
        )
        self.assertAlmostEqual(invoice.l10n_py_amount_exempt, 100000.0, places=0)
        self.assertEqual(invoice.l10n_py_amount_iva_total, 0.0)

    def test_iva_mixed_rates(self):
        """F09: Cenário com 4 itens — verificar F003 até F020"""
        invoice = self._create_invoice(
            products_prices=[
                (self.product_10, self.tax_10, 1100000.0),  # IVA 10%
                (self.product_10, self.tax_10, 550000.0),  # IVA 10%
                (self.product_5, self.tax_5, 525000.0),  # IVA 5%
                (self.product_exempt, self.tax_exempt, 200000.0),  # Exento
            ]
        )
        # F003: Exento
        self.assertAlmostEqual(invoice.l10n_py_amount_exempt, 200000.0, places=0)
        # F004: Total gravado 5% (tax-inclusive)
        self.assertAlmostEqual(invoice.l10n_py_amount_subtotal_5, 525000.0, places=0)
        # F005: Total gravado 10% (tax-inclusive)
        self.assertAlmostEqual(invoice.l10n_py_amount_subtotal_10, 1650000.0, places=0)
        # F014: Total IVA
        expected_iva_10 = 1650000.0 - (1650000.0 / 1.1)  # = 150000
        expected_iva_5 = 525000.0 - (525000.0 / 1.05)  # = 25000
        self.assertAlmostEqual(
            invoice.l10n_py_amount_iva_total,
            expected_iva_10 + expected_iva_5,
            places=0,
        )
        # F018: Base gravada 5%
        self.assertAlmostEqual(invoice.l10n_py_base_5, 500000.0, places=0)
        # F019: Base gravada 10%
        self.assertAlmostEqual(invoice.l10n_py_base_10, 1500000.0, places=0)
        # F020: Total base gravada
        self.assertAlmostEqual(invoice.l10n_py_base_total, 2000000.0, places=0)
        # F008: Total operación
        self.assertAlmostEqual(
            invoice.l10n_py_total_operation,
            200000.0 + 525000.0 + 1650000.0,
            places=0,
        )

    def test_total_in_words(self):
        """F03: Total en letras en español"""
        invoice = self._create_invoice(
            products_prices=[
                (self.product_exempt, self.tax_exempt, 100.0),
            ]
        )
        self.assertTrue(invoice.l10n_py_amount_total_words)

    def test_pyg_conversion(self):
        """F03/F023: Factura USD con tipo de cambio → total en PYG"""
        invoice = self._create_invoice(
            products_prices=[
                (self.product_exempt, self.tax_exempt, 500.0),
            ],
            l10n_py_exchange_rate=7300.0,
        )
        self.assertAlmostEqual(invoice.l10n_py_amount_total_pyg, 3650000.0, places=0)

    # ============== Formato número completo ==============

    def test_full_invoice_number_format(self):
        """F02: Formato 001-001-0000001"""
        invoice = self._create_invoice()
        invoice.action_post()
        self.assertEqual(invoice.l10n_py_full_invoice_number, "001-001-0000001")

    def test_authorization_field_exists(self):
        """Campo l10n_py_authorization_id en el move"""
        invoice = self._create_invoice()
        self.assertEqual(invoice.l10n_py_authorization_id, self.authorization)
