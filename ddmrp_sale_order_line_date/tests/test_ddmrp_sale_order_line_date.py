# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from datetime import datetime as dt, timedelta as td

from odoo.addons.ddmrp_sale.tests.test_ddmrp_sale import TestDDMRPSale


class TestDDMRPSaleOrderLineDate(TestDDMRPSale):
    """
    Inherits all base ddmrp_sale tests, which now run with line-level
    commitment_date active. Tests 02-04 set commitment_date only on the order,
    so the line inherits it — verifying backwards-compatible behaviour.

    Tests below specifically exercise cases where order-level and line-level
    dates diverge.
    """

    def test_05_line_date_outside_horizon_not_qualified(self):
        """Order date within horizon but line date outside -> not qualified."""
        self._refresh_involved_buffers()
        so_date_order = dt.today() + td(days=2)
        so_date_line = dt.today() + td(days=15)  # beyond the 10-day horizon
        so = self.so_model.create(
            {
                "partner_id": self.customer.id,
                "partner_invoice_id": self.customer.id,
                "partner_shipping_id": self.customer.id,
                "commitment_date": so_date_order,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.productA.id,
                            "name": "cool product",
                            "price_unit": 100.0,
                            "product_uom_qty": 17,
                            "commitment_date": so_date_line,
                        },
                    )
                ],
            }
        )
        self.assertEqual(so.state, "draft")
        self._refresh_involved_buffers()
        self.assertEqual(
            self.buffer_a.qualified_demand, self.buffer_internal.qualified_demand
        )

    def test_06_line_date_within_horizon_qualified(self):
        """Order date outside horizon but line date within horizon -> qualified."""
        self._refresh_involved_buffers()
        so_date_order = dt.today() + td(days=15)  # beyond the 10-day horizon
        so_date_line = dt.today() + td(days=2)
        so = self.so_model.create(
            {
                "partner_id": self.customer.id,
                "partner_invoice_id": self.customer.id,
                "partner_shipping_id": self.customer.id,
                "commitment_date": so_date_order,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.productA.id,
                            "name": "cool product",
                            "price_unit": 100.0,
                            "product_uom_qty": 17,  # it is a spike.
                            "commitment_date": so_date_line,
                        },
                    )
                ],
            }
        )
        self.assertEqual(so.state, "draft")
        self._refresh_involved_buffers()
        diff = self.buffer_a.qualified_demand - self.buffer_internal.qualified_demand
        self.assertEqual(diff, 17)

    def test_07_sol_uom_line_date(self):
        """UOM conversion works correctly when using line-level commitment_date."""
        self._refresh_involved_buffers()
        so_date_order = dt.today() + td(days=15)  # beyond the 10-day horizon
        so_date_line = dt.today() + td(days=2)
        so = self.so_model.create(
            {
                "partner_id": self.customer.id,
                "partner_invoice_id": self.customer.id,
                "partner_shipping_id": self.customer.id,
                "commitment_date": so_date_order,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.productA.id,
                            "name": "cool product",
                            "price_unit": 100.0,
                            "product_uom_qty": 2,  # 2 dozens, it is a spike.
                            "product_uom": self.uom_dozen.id,
                            "commitment_date": so_date_line,
                        },
                    )
                ],
            }
        )
        self.assertEqual(so.state, "draft")
        self._refresh_involved_buffers()
        diff = self.buffer_a.qualified_demand - self.buffer_internal.qualified_demand
        self.assertEqual(diff, 24)
