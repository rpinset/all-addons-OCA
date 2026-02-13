# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import tagged

from odoo.addons.contract.tests.test_contract import TestContractBase


@tagged("post_install", "-at_install")
class TestContractAutoValidate(TestContractBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.write({"enable_contract_invoice_manually": True})
        contracts = cls.contract
        for _i in range(10):
            contracts |= cls.contract.copy()
        cls.manual_invoice_contracts = contracts[:5]
        cls.manual_invoice_contracts.write({"is_manually_invoiced": True})
        cls.auto_invoice_contracts = contracts - cls.manual_invoice_contracts

    def test_contract_manually_create_invoice(self):
        """
        Test only contracts-to-invoice-manually are proposed
        """
        wizard = self.env["contract.manually.create.invoice"].create(
            {"invoice_date": self.today}
        )
        contract_to_invoice_count = wizard.contract_to_invoice_count
        self.assertEqual(len(self.manual_invoice_contracts), contract_to_invoice_count)
        action = wizard.create_invoice()
        invoice_lines = self.env["account.move.line"].search(
            [
                (
                    "contract_line_id",
                    "in",
                    self.manual_invoice_contracts.mapped("contract_line_ids").ids,
                )
            ]
        )
        self.assertEqual(
            len(self.manual_invoice_contracts.mapped("contract_line_ids")),
            len(invoice_lines),
        )
        invoices = self.env["account.move"].search(action["domain"])
        self.assertEqual(len(invoices), contract_to_invoice_count)

    def test_contract_manually_create_invoice_custom_domain(self):
        """
        Overwrite domain to manually invoice auto-contracts
        """
        wizard = self.env["contract.manually.create.invoice"].create(
            {"invoice_date": self.today}
        )
        wizard.filter_domain = str([("id", "in", self.auto_invoice_contracts.ids)])
        action = wizard.create_invoice()
        invoices = self.env["account.move"].search(action["domain"])

        self.assertEqual(
            invoices.mapped("line_ids.contract_line_id.contract_id"),
            self.auto_invoice_contracts,
        )

    def test_cron_recurring_create_invoice(self):
        self.acct_line.date_start = "2018-01-01"
        self.acct_line.recurring_invoicing_type = "post-paid"
        self.acct_line.date_end = "2018-03-15"
        contracts = self.contract2
        for _i in range(10):
            contracts |= self.contract.copy()
        manual_invoice_contracts = contracts[:5]
        manual_invoice_contracts.write({"is_manually_invoiced": True})

        self.env["contract.contract"].cron_recurring_create_invoice()
        invoice_lines = self.env["account.move.line"].search(
            [("contract_line_id", "in", contracts.mapped("contract_line_ids").ids)]
        )
        invoiced_contracts = invoice_lines.mapped("contract_line_id.contract_id")
        for manual_contract in manual_invoice_contracts:
            self.assertNotIn(manual_contract, invoiced_contracts)
