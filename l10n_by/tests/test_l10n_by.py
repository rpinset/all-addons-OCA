# Copyright 2026 Aliaksandr Zubik <alexzub@tut.by> (https://artcloud.by)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestL10nBy(TransactionCase):
    """Tests for Belarus localization."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a company with Belarus as country
        cls.company = cls.env["res.company"].create(
            {
                "name": "Belarus Test Company",
                "country_id": cls.env.ref("base.by").id,
            }
        )
        cls.env = cls.env(
            context=dict(cls.env.context, allowed_company_ids=[cls.company.id])
        )

        # Apply the Belarus chart template to the company
        chart_template = cls.env["account.chart.template"]
        chart_template._load("by", cls.company, install_demo=False)

    def test_accounts_loaded(self):
        """Test that accounts were loaded from template."""
        # Check that key accounts exist after template load
        AccountAccount = self.env["account.account"].with_company(self.company)
        accounts = AccountAccount.search(
            [("code", "in", ["5010", "5110", "6210", "6010"])]
        )
        self.assertEqual(len(accounts), 4, "Should have 4 key accounts")

        # Check specific account types
        receivable = accounts.filtered(lambda a: a.code == "6210")
        self.assertEqual(receivable.account_type, "asset_receivable")

        payable = accounts.filtered(lambda a: a.code == "6010")
        self.assertEqual(payable.account_type, "liability_payable")

    def test_vat_taxes_loaded(self):
        """Test that VAT taxes were loaded from template."""
        taxes = self.env["account.tax"].with_company(self.company).search([])
        self.assertTrue(len(taxes) >= 8, "Should have at least 8 taxes")

        # Check VAT 20% sale tax
        vat_20_sale = taxes.filtered(
            lambda t: t.amount == 20.0 and t.type_tax_use == "sale"
        )
        self.assertTrue(vat_20_sale, "VAT 20% sale tax should exist")

        # Check VAT 10% sale tax
        vat_10_sale = taxes.filtered(
            lambda t: t.amount == 10.0 and t.type_tax_use == "sale"
        )
        self.assertTrue(vat_10_sale, "VAT 10% sale tax should exist")

    def test_fiscal_positions_loaded(self):
        """Test that fiscal positions were loaded from template."""
        positions = (
            self.env["account.fiscal.position"].with_company(self.company).search([])
        )
        self.assertTrue(len(positions) >= 2, "Should have at least 2 fiscal positions")

        # Check domestic position exists
        domestic = positions.filtered(lambda p: p.auto_apply)
        self.assertTrue(domestic, "Auto-apply domestic position should exist")

    def test_tax_report_exists(self):
        """Test that Belarus VAT report was created."""
        report = self.env.ref("l10n_by.tax_report_by", raise_if_not_found=False)
        self.assertTrue(report, "Belarus VAT Report should exist")
        self.assertEqual(report.country_id, self.env.ref("base.by"))
