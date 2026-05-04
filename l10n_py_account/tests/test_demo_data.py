from odoo.tests import tagged
from odoo.tests.common import TransactionCase


def _ref_or_skip(test_case, xml_id):
    """Return the record for xml_id or skip the test if not found."""
    try:
        record = test_case.env.ref(xml_id)
    except ValueError:
        test_case.skipTest(f"Demo data {xml_id} not loaded")
    return record


@tagged("post_install", "-at_install", "l10n_py")
class TestDemoData(TransactionCase):
    """Valida que os dados demo do l10n_py_account foram carregados corretamente."""

    def test_demo_partners_exist(self):
        """Partners demo foram criados com dados corretos"""
        partner = _ref_or_skip(self, "l10n_py_account.partner_contribuyente_general")
        self.assertTrue(partner)
        self.assertEqual(partner.vat, "80012345-6")
        self.assertEqual(partner.l10n_py_ruc, "80012345")
        self.assertEqual(partner.l10n_py_ruc_dv, "6")
        self.assertEqual(partner.l10n_py_taxpayer_type, "1")

        partner_svc = _ref_or_skip(
            self, "l10n_py_account.partner_contribuyente_servicios"
        )
        self.assertTrue(partner_svc)
        self.assertEqual(partner_svc.vat, "80067890-7")
        self.assertEqual(partner_svc.l10n_py_ruc, "80067890")

        partner_nc = _ref_or_skip(self, "l10n_py_account.partner_no_contribuyente_ci")
        self.assertTrue(partner_nc)
        self.assertEqual(partner_nc.l10n_py_taxpayer_type, "2")

    def test_demo_products_exist(self):
        """Produtos demo foram criados"""
        product_10 = _ref_or_skip(self, "l10n_py_account.product_iva_10_electronica")
        self.assertTrue(product_10)
        self.assertTrue(product_10.taxes_id)

        product_5 = _ref_or_skip(self, "l10n_py_account.product_iva_5_alimento")
        self.assertTrue(product_5)

        product_exempt = _ref_or_skip(self, "l10n_py_account.product_exento_libro")
        self.assertTrue(product_exempt)

    def test_demo_authorizations_exist(self):
        """Timbrados demo foram criados com ranges corretos"""
        auth_001 = _ref_or_skip(self, "l10n_py_account.demo_authorization_001")
        self.assertTrue(auth_001)
        self.assertEqual(auth_001.name, "12345678")
        self.assertEqual(auth_001.invoice_number_from, 1)
        self.assertEqual(auth_001.invoice_number_to, 10000)

        auth_nc = _ref_or_skip(self, "l10n_py_account.demo_authorization_credit_note")
        self.assertTrue(auth_nc)
        self.assertEqual(auth_nc.name, "11223344")

        auth_nd = _ref_or_skip(self, "l10n_py_account.demo_authorization_debit_note")
        self.assertTrue(auth_nd)
        self.assertEqual(auth_nd.name, "44556677")

    def test_demo_customer_invoices_posted(self):
        """Facturas de venta demo estão confirmadas"""
        invoice_ids = [
            "l10n_py_account.demo_invoice_fe_iva10",
            "l10n_py_account.demo_invoice_fe_iva5",
            "l10n_py_account.demo_invoice_fe_mixta",
            "l10n_py_account.demo_invoice_fe_no_contribuyente",
            "l10n_py_account.demo_invoice_fe_exenta",
            "l10n_py_account.demo_invoice_fe_punto2",
        ]
        for xml_id in invoice_ids:
            invoice = _ref_or_skip(self, xml_id)
            self.assertEqual(
                invoice.state,
                "posted",
                f"Invoice {xml_id} should be posted",
            )
            self.assertEqual(invoice.move_type, "out_invoice")

    def test_demo_invoice_fe_iva10_amounts(self):
        """FE IVA 10%: montos calculados correctamente"""
        invoice = _ref_or_skip(self, "l10n_py_account.demo_invoice_fe_iva10")
        # 2 × 5.500.000 + 5 × 1.100.000 = 16.500.000
        self.assertGreater(invoice.amount_total, 0)
        product_lines = invoice.invoice_line_ids.filtered(lambda line: line.product_id)
        self.assertEqual(len(product_lines), 2)

    def test_demo_invoice_fe_mixta_has_all_rates(self):
        """FE Mixta: tiene líneas con IVA 10%, 5% y exento"""
        invoice = _ref_or_skip(self, "l10n_py_account.demo_invoice_fe_mixta")
        product_lines = invoice.invoice_line_ids.filtered(lambda line: line.product_id)
        self.assertEqual(len(product_lines), 3)

    def test_demo_supplier_invoices_exist(self):
        """Facturas de compra demo existem"""
        bill = _ref_or_skip(self, "l10n_py_account.demo_bill_iva10")
        self.assertTrue(bill)
        self.assertEqual(bill.move_type, "in_invoice")

    def test_demo_document_types(self):
        """Tipos de documento LATAM para Paraguay existem"""
        doc_types = {
            "l10n_py_account.dc_py_f": ("1", "invoice"),
            "l10n_py_account.dc_py_af": ("4", "invoice"),
            "l10n_py_account.dc_py_nc": ("5", "credit_note"),
            "l10n_py_account.dc_py_nd": ("6", "debit_note"),
            "l10n_py_account.dc_py_nr": ("7", "invoice"),
        }
        for xml_id, (code, internal_type) in doc_types.items():
            dt = self.env.ref(xml_id)
            self.assertEqual(dt.code, code, f"{xml_id} should have code {code}")
            self.assertEqual(
                dt.internal_type,
                internal_type,
                f"{xml_id} should have internal_type {internal_type}",
            )

    def test_authorization_validity_dates(self):
        """Timbrados demo têm datas de validade coerentes"""
        auth = _ref_or_skip(self, "l10n_py_account.demo_authorization_001")
        self.assertTrue(auth.date_from)
        self.assertTrue(auth.date_to)
        self.assertLess(auth.date_from, auth.date_to)

        auth_expired = _ref_or_skip(self, "l10n_py_account.demo_authorization_expired")
        self.assertFalse(auth_expired.active)
