import freezegun

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests.common import tagged

from odoo.addons.sale_order_blanket_order.tests.common import (
    SaleOrderBlanketOrderCase,
)


@tagged("post_install", "-at_install")
class TestCallOffDelivery(SaleOrderBlanketOrderCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.delivery_product = cls.env["product.product"].create(
            {
                "name": "Delivery fees",
                "type": "service",
                "invoice_policy": "order",
            }
        )
        cls.carrier = cls.env["delivery.carrier"].create(
            {
                "name": "Test Carrier",
                "delivery_type": "fixed",
                "product_id": cls.delivery_product.id,
                # Keep it zero because of `_check_call_off_order_line_price`
                # Otherwise, error will raise before the test
                "fixed_price": 0.0,
            }
        )
        # Configure partner's carrier
        cls.partner.property_delivery_carrier_id = cls.carrier
        # Configure company settings
        company = cls.env.company
        company.carrier_on_create = True
        company.carrier_auto_assign = True
        company.create_call_off_from_so_if_possible = True
        # Confirm to trigger delivery fee (`_is_auto_set_carrier_on_confirm`)
        cls.blanket_so.action_confirm()
        # Two regular SOs reused by the tests: each test confirms them with
        # whatever context it needs. The transaction is rolled back between
        # tests, so they stay in draft for the next one.
        cls.so1 = cls._make_regular_so()
        cls.so2 = cls._make_regular_so()

    @classmethod
    def _make_blanket_so(cls, product):
        return cls.env["sale.order"].create(
            {
                "order_type": "blanket",
                "partner_id": cls.partner.id,
                "blanket_validity_start_date": "2025-01-01",
                "blanket_validity_end_date": "2025-12-31",
                "blanket_reservation_strategy": "at_call_off",
                "order_line": [
                    Command.create(
                        {
                            "product_id": product.id,
                            "product_uom_qty": 10.0,
                            "price_unit": 100.0,
                        }
                    ),
                ],
            }
        )

    @classmethod
    def _make_regular_so(cls):
        return cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": cls.product_1.id,
                            "product_uom_qty": 5,
                            "price_unit": 100.0,
                        }
                    ),
                ],
            }
        )

    def _has_delivery_line(self, order):
        return any(order.order_line.mapped("is_delivery"))

    @freezegun.freeze_time("2025-06-01")
    def test_two_sales_with_calloff_without_fix(self):
        """Confirm the presence of the bug by deactivating both fixes"""
        self.assertTrue(self._has_delivery_line(self.blanket_so))
        ctx = {
            "skip_blanket_carrier_filter": True,
            "skip_blanket_carrier_auto_assign": True,
        }
        self.so1.with_context(**ctx).action_confirm()
        with self.assertRaisesRegex(
            ValidationError, "not part of linked blanket order"
        ):
            self.so2.with_context(**ctx).action_confirm()

    @freezegun.freeze_time("2025-06-01")
    def test_two_sales_with_calloff_only_line_filter_fix(self):
        """Delivery line created but ignored should work"""
        self.so1.with_context(skip_blanket_carrier_auto_assign=True).action_confirm()
        self.so2.with_context(skip_blanket_carrier_auto_assign=True).action_confirm()

        self.assertEqual(len(self.blanket_so.call_off_order_ids), 2)
        for co in self.blanket_so.call_off_order_ids:
            self.assertEqual(co.state, "sale")
            self.assertTrue(self._has_delivery_line(co))

    @freezegun.freeze_time("2025-06-01")
    def test_two_sales_with_calloff_with_fixes(self):
        """With the 2 fixes, ther should be no line created"""
        self.so1.action_confirm()
        self.so2.action_confirm()

        self.assertEqual(len(self.blanket_so.call_off_order_ids), 2)
        for co in self.blanket_so.call_off_order_ids:
            self.assertEqual(co.state, "sale")

    @freezegun.freeze_time("2025-06-01")
    def test_blanket_delivery_line_no_false_overlap(self):
        """A second blanket order with a distinct product must confirm even
        though both blanket orders carry the same auto-assigned carrier
        (delivery) line over overlapping validity periods."""
        self.assertTrue(self._has_delivery_line(self.blanket_so))
        blanket_so2 = self._make_blanket_so(self.product_3)
        blanket_so2.action_confirm()
        self.assertEqual(blanket_so2.state, "sale")
        self.assertTrue(self._has_delivery_line(blanket_so2))

    @freezegun.freeze_time("2025-06-01")
    def test_blanket_delivery_line_overlap_without_fix(self):
        """Without the filter, the shared carrier line triggers a false
        overlap error between the two blanket orders."""
        blanket_so2 = self._make_blanket_so(self.product_3)
        with self.assertRaisesRegex(
            ValidationError, "already part of another blanket order"
        ):
            blanket_so2.with_context(skip_blanket_carrier_filter=True).action_confirm()

    @freezegun.freeze_time("2025-06-01")
    def test_call_off_has_no_delivery_line(self):
        """Call-off orders must never receive an auto-assigned delivery line."""
        self.so1.action_confirm()
        call_off = self.blanket_so.call_off_order_ids
        self.assertEqual(len(call_off), 1)
        # We must NOT have any delivery line
        self.assertFalse(self._has_delivery_line(call_off))

    @freezegun.freeze_time("2025-06-01")
    def test_call_off_has_delivery_line_when_skip_context(self):
        """``skip_blanket_carrier_auto_assign`` re-enables the auto-assign
        on call-offs; the delivery line is back on the call-off."""
        self.so1.with_context(skip_blanket_carrier_auto_assign=True).action_confirm()
        call_off = self.blanket_so.call_off_order_ids
        self.assertEqual(len(call_off), 1)
        # We must have a delivery line
        self.assertTrue(self._has_delivery_line(call_off))
