# Part of the Paraguayan localization. See LICENSE file for full copyright
# and licensing details.
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestChartTemplatePy(AccountTestInvoicingCommon):
    @classmethod
    @AccountTestInvoicingCommon.setup_country("py")
    @AccountTestInvoicingCommon.setup_chart_template("py")
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.template = cls.env["account.chart.template"].with_company(cls.company)

    def test_chart_template_loads(self):
        self.assertEqual(self.company.chart_template, "py")
        self.assertEqual(self.company.account_fiscal_country_id.code, "PY")
        self.assertEqual(
            self.company.account_sale_tax_id.amount, 10, "Default sale tax is IVA 10%"
        )
        self.assertEqual(self.company.account_purchase_tax_id.type_tax_use, "purchase")
        self.assertTrue(self.company.account_journal_suspense_account_id)

    def test_taxes(self):
        for kind, use in (("ventas", "sale"), ("compras", "purchase")):
            for rate, amount in (("10", 10.0), ("5", 5.0), ("exento", 0.0)):
                tax = self.template.ref(f"py_tax_vat_{rate}_{kind}")
                self.assertEqual(tax.amount, amount)
                self.assertEqual(tax.type_tax_use, use)
                self.assertTrue(tax.tax_group_id)

    def test_outstanding_accounts(self):
        journal = self.env["account.journal"].search(
            [("company_id", "=", self.company.id), ("type", "=", "bank")], limit=1
        )
        self.assertTrue(journal)
        lines = journal.inbound_payment_method_line_ids
        self.assertTrue(lines)
        self.assertTrue(
            all(lines.mapped("payment_account_id")),
            "The outstanding accounts are created by the chart template",
        )

    def test_fiscal_position_tax_mapping(self):
        for kind in ("ventas", "compras"):
            position = self.template.ref(f"py_fiscal_position_{kind}_exentas")
            exempt = self.template.ref(f"py_tax_vat_exento_{kind}")
            for rate in ("5", "10"):
                tax = self.template.ref(f"py_tax_vat_{rate}_{kind}")
                self.assertEqual(
                    position.map_tax(tax),
                    exempt,
                    f"IVA {rate}% ({kind}) maps to Exento",
                )

    def test_default_accounts(self):
        """Company defaults for partners and product categories come from the chart"""
        self.assertEqual(
            self.company.income_account_id, self.template.ref("account_py_40101_income")
        )
        self.assertEqual(
            self.company.expense_account_id,
            self.template.ref("account_py_50101_expense"),
        )
        partner = self.env["res.partner"].create({"name": "Test PY partner"})
        self.assertEqual(
            partner.property_account_receivable_id, self.template.ref("account_py_301")
        )
        self.assertEqual(
            partner.property_account_payable_id, self.template.ref("account_py_2001")
        )
        categ = self.env["product.category"].create({"name": "Test PY category"})
        self.assertEqual(
            categ.property_account_income_categ_id, self.company.income_account_id
        )
        self.assertEqual(
            categ.property_account_expense_categ_id, self.company.expense_account_id
        )
