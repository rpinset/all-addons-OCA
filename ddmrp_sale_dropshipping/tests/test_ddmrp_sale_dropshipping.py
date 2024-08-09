# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from datetime import datetime as dt, timedelta as td

from odoo.addons.ddmrp_sale.tests.test_ddmrp_sale import TestDDMRPSale


class TestDDMRPSaleDropshipping(TestDDMRPSale):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_01_dropship_quotation_not_included_as_demand(self):
        self._refresh_involved_buffers()
        self.assertEqual(
            self.buffer_a.qualified_demand, self.buffer_internal.qualified_demand
        )
        so_date = dt.today() + td(days=2)
        so = self.so_model.create(
            {
                "partner_id": self.customer.id,
                "partner_invoice_id": self.customer.id,
                "partner_shipping_id": self.customer.id,
                "commitment_date": so_date,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.productA.id,
                            "name": "cool product",
                            "price_unit": 100.0,
                            "product_uom_qty": 17,  # it is a spike.
                            "commitment_date": so_date,
                            "route_id": self.env.ref(
                                "stock_dropshipping.route_drop_shipping"
                            ).id,
                        },
                    )
                ],
            }
        )
        self.assertEqual(so.state, "draft")
        self._refresh_involved_buffers()
        # Qualified demand ignored as the line route does not affect the buffer
        # location
        self.assertEqual(self.buffer_a.qualified_demand, 0)
        self.assertEqual(self.buffer_internal.qualified_demand, 0)
