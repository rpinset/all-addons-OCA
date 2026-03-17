# Copyright 2022 Opener B.V.
# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo.tests.common import TransactionCase

from .common import CommonPartnerInvoicingMode


class TestManualInvoiceGrouping(CommonPartnerInvoicingMode, TransactionCase):
    def test_manual_invoice_does_not_mix_partners(self):
        """
        Manual invoice creation must never mix sale orders
        belonging to different partners, even if
        partner_invoicing_mode is installed.
        """
        # Confirm and deliver both sale orders
        self._confirm_and_deliver(self.so1)

        # Create a second sale order for another partner
        so_other_partner = self.SaleOrder.create(
            {
                "partner_id": self.partner2.id,
                "partner_invoice_id": self.partner2.id,
                "partner_shipping_id": self.partner2.id,
                "payment_term_id": self.pt1.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": "Line one",
                            "product_id": self.product.id,
                            "product_uom_qty": 1,
                            "product_uom": self.product.uom_id.id,
                            "price_unit": 100,
                        },
                    )
                ],
                "pricelist_id": self.env.ref("product.list0").id,
            }
        )
        self._confirm_and_deliver(so_other_partner)

        # Manual invoicing (this is where the bug was)
        invoices = (self.so1 | so_other_partner)._create_invoices()

        # Expect one invoice per partner
        self.assertEqual(2, len(invoices))
        self.assertEqual(
            set(invoices.mapped("partner_id").ids),
            {self.partner.id, self.partner2.id},
        )
