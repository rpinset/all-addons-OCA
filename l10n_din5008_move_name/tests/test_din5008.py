# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestDatevExport(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.JournalObj = cls.env["account.journal"]
        cls.sale_journal = cls.JournalObj.search(
            [
                ("type", "=", "sale"),
                ("company_id", "=", cls.company.id),
            ],
            limit=1,
        )
        if not cls.sale_journal:
            cls.sale_journal = cls.JournalObj.create(
                {
                    "name": "Test sale journal",
                    "code": "sale",
                    "type": "sale",
                    "company_id": cls.company.id,
                }
            )
        cls.AccountObj = cls.env["account.account"]
        cls.PartnerObj = cls.env["res.partner"]
        cls.ProductObj = cls.env["product.product"]
        cls.InvoiceObj = cls.env["account.move"]

        cls.customer_de = cls.env["res.partner"].create(
            {
                "name": "Test customer",
            }
        )

        cls.consulting = cls.env["product.product"].create(
            {
                "name": "Test consulting",
                "list_price": 100.0,
                "standard_price": 50.0,
            }
        )

    def test_name(self):
        """Test the name of the invoice"""
        # Create a test invoice
        invoice = self.InvoiceObj.create(
            {
                "move_type": "out_invoice",
                "partner_id": self.customer_de.id,
                "journal_id": self.sale_journal.id,
                "invoice_line_ids": [
                    (0, 0, {"product_id": self.consulting.id, "quantity": 1})
                ],
            }
        )
        invoice.action_post()
        # Check the name of the invoice
        self.assertIn(invoice.name, invoice.l10n_din5008_document_title)
