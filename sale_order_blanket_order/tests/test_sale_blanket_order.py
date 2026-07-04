# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import freezegun
from odoo_test_helper import FakeModelLoader

from odoo import Command
from odoo.exceptions import ValidationError
from odoo.tests import Form
from odoo.tests.common import RecordCapturer

from .common import SaleOrderBlanketOrderCase


class TestFakeSaleBlanketOrder(SaleOrderBlanketOrderCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create a fake model to declare another reservation strategy
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .fake_models import FakeSaleOrder

        cls.loader.update_registry(
            [
                FakeSaleOrder,
            ]
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super().tearDownClass()

    # Remove tests that are incompatible with FakeModuleLoader
    def check_attrs(self):
        pass

    # ======================================================================
    def test_reservation_strategy_editable(self):
        # change is allowed in draft state
        self.blanket_so.blanket_reservation_strategy = "fake"
        self.blanket_so.blanket_reservation_strategy = "at_call_off"
        self.blanket_so.action_confirm()
        # change is allowed after confirmation while the blanket order
        # is not finalized
        self.blanket_so.blanket_reservation_strategy = "fake"
        self.blanket_so._action_cancel()
        with (
            self.assertRaisesRegex(
                ValidationError, "The reservation strategy cannot be modified"
            ),
            self.env.cr.savepoint(),
        ):
            # change is not allowed on canceled order
            self.blanket_so.blanket_reservation_strategy = "at_call_off"
        self.blanket_so.action_draft()
        # change is allowed in draft state
        self.blanket_so.blanket_reservation_strategy = "at_call_off"
        self.blanket_so.action_confirm()
        with freezegun.freeze_time("2026-12-31"):
            self.so_model._cron_manage_blanket_order_eol()

        self.assertFalse(self.blanket_so.blanket_need_to_be_finalized)
        with (
            self.assertRaisesRegex(
                ValidationError, "The reservation strategy cannot be modified"
            ),
            self.env.cr.savepoint(),
        ):
            # change is not allowed on finalized order
            self.blanket_so.blanket_reservation_strategy = "fake"


class TestSaleBlanketOrder(SaleOrderBlanketOrderCase):
    def test_action_view_call_off_orders_addresses(self):
        partner_invoice = self.env["res.partner"].create(
            {
                "name": "Alternative Invoice Address",
                "type": "invoice",
                "parent_id": self.partner.id,
            }
        )
        partner_shipping = self.env["res.partner"].create(
            {
                "name": "Alternative Shipping Address",
                "type": "delivery",
                "parent_id": self.partner.id,
            }
        )
        self.blanket_so.write(
            {
                "partner_invoice_id": partner_invoice.id,
                "partner_shipping_id": partner_shipping.id,
            }
        )

        action = self.blanket_so.action_view_call_off_orders()
        action_context = action.get("context", {})
        with Form(self.env["sale.order"].with_context(**action_context)) as so_form:
            with so_form.order_line.new() as line:
                line.product_id = self.product_1
                line.product_uom_qty = 1.0
            call_off_order = so_form.save()

        self.assertEqual(
            call_off_order.partner_invoice_id,
            partner_invoice,
        )
        self.assertEqual(
            call_off_order.partner_shipping_id,
            partner_shipping,
        )

    def test_confirm_start_date_required(self):
        order = self.env["sale.order"].create(
            {
                "order_type": "blanket",
                "partner_id": self.partner.id,
            }
        )
        # Create a call-off order
        with self.assertRaisesRegex(
            ValidationError, "The validity start date is required"
        ):
            order.action_confirm()

    def test_confirm_end_date_required(self):
        order = self.env["sale.order"].create(
            {
                "order_type": "blanket",
                "partner_id": self.partner.id,
                "blanket_validity_start_date": "2024-01-01",
            }
        )
        with self.assertRaisesRegex(
            ValidationError, "The validity end date is required"
        ):
            order.action_confirm()

    def test_confrim_end_date_greater_than_start_date(self):
        order = self.env["sale.order"].create(
            {
                "order_type": "blanket",
                "partner_id": self.partner.id,
                "blanket_validity_start_date": "2024-01-02",
                "blanket_validity_end_date": "2024-01-01",
            }
        )
        with self.assertRaisesRegex(
            ValidationError, "The validity end date must be greater than"
        ):
            order.action_confirm()

    def test_confirm_no_blanket_order(self):
        order = self.env["sale.order"].create(
            {
                "order_type": "blanket",
                "partner_id": self.partner.id,
                "blanket_validity_start_date": "2024-01-01",
                "blanket_validity_end_date": "2024-12-31",
                "blanket_order_id": self.so.id,
            }
        )
        with self.assertRaisesRegex(
            ValidationError, "A blanket order cannot have a blanket order."
        ):
            order.action_confirm()

    def test_no_product_overlap(self):
        self.blanket_so.action_confirm()
        order = self.env["sale.order"].create(
            {
                "order_type": "blanket",
                "partner_id": self.partner.id,
                "blanket_validity_start_date": "2024-02-01",
                "blanket_validity_end_date": "2025-01-31",
                "order_line": [
                    Command.create(
                        {"product_id": self.product_1.id, "product_uom_qty": 10.0}
                    ),
                ],
            }
        )
        # Validate a blanket order with a product that is already in the blanket order
        with (
            self.assertRaisesRegex(
                ValidationError,
                (
                    "The product 'Product 1' is already part of another blanket order "
                    f"{self.blanket_so.name}."
                ),
            ),
            self.env.cr.savepoint(),
        ):
            order.action_confirm()
        self.product_1.allow_blanket_order_overlap = True
        order.action_confirm()

    def test_reservation(self):
        # Confirm the blanket order with reservation at call off
        self.blanket_so.action_confirm()
        self.assertTrue(self.blanket_so.manual_delivery)
        self.assertEqual(self.blanket_so.state, "sale")
        self.assertEqual(
            self.blanket_so.commitment_date.date(),
            self.blanket_so.blanket_validity_start_date,
        )
        self.assertFalse(self.blanket_so.order_line.move_ids)

    def test_reset_reservation_at_cancel(self):
        self.blanket_so.action_confirm()
        self.assertTrue(self.blanket_so.manual_delivery)
        self.blanket_so._action_cancel()
        self.assertFalse(self.blanket_so.manual_delivery)

    def test_eol(self):
        # Confirm the blanket order with reservation at call off
        self.assertFalse(self.blanket_so.blanket_need_to_be_finalized)
        self.blanket_so.blanket_eol_strategy = "deliver"
        self.blanket_so.action_confirm()
        self.assertTrue(self.blanket_so.blanket_need_to_be_finalized)
        self.blanket_so.flush_recordset()
        with (
            RecordCapturer(self.so_model, self.call_off_domain) as captured,
            freezegun.freeze_time("2026-12-31"),
        ):
            self.so_model._cron_manage_blanket_order_eol()
        self.assertFalse(self.blanket_so.blanket_need_to_be_finalized)
        self.assertEqual(len(captured.records), 1)
        for line in self.blanket_so.order_line:
            self.assertEqual(line.call_off_remaining_qty, 0.0)
            call_off = line.call_off_line_ids
            self.assertEqual(len(call_off), 1)
            self.assertEqual(call_off.product_uom_qty, line.product_uom_qty)
            self.assertTrue(line.move_ids)

    @freezegun.freeze_time("2025-02-01")
    def test_prevent_call_off_with_only_delivery_products(self):
        """
        At the EOL of a blanket order, if the only remaining product to deliver is a
        delivery product and the user hasn't included it in any of the call-off orders,
        it makes no sense to create a call-off order containing only a delivery product
        without tangible items.
        Such orders would serve no practical purpose and could lead to confusion.
        Ensuring that call-off orders include at least one actual product maintains
        meaningful and logical orders.

        This test cheks that call-off orders generated by the EOL cron don't contain
        only delivery products.
        """
        delivery_method = self.env.ref("delivery.delivery_local_delivery")
        delivery_product = delivery_method.product_id
        self.blanket_so.blanket_eol_strategy = "deliver"
        self.blanket_so.action_confirm()
        # Add shipping costs
        delivery_wizard = Form(
            self.env["choose.delivery.carrier"].with_context(
                default_order_id=self.blanket_so.id,
                default_carrier_id=delivery_method.id,
            )
        )
        choose_delivery_carrier = delivery_wizard.save()
        choose_delivery_carrier.button_confirm()
        self.assertIn(delivery_product, self.blanket_so.order_line.product_id)
        # Create a call-off order without reservation
        order = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "partner_id": self.partner.id,
                "blanket_order_id": self.blanket_so.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_1.id,
                            "product_uom_qty": 20.0,
                        }
                    ),
                    Command.create(
                        {
                            "product_id": self.product_2.id,
                            "product_uom_qty": 10.0,
                        }
                    ),
                ],
            }
        )
        order.action_confirm()
        # process the picking
        picking = order.order_line.blanket_move_ids.picking_id
        picking.action_assign()
        for move_line in picking.move_line_ids:
            move_line.picked = True
        picking._action_done()

        delivery_line = self.blanket_so.order_line.filtered(
            lambda ol: ol.product_id == delivery_product
        )
        self.assertEqual(delivery_line.call_off_remaining_qty, 1)
        self.assertEqual(
            sum(
                (self.blanket_so.order_line - delivery_line).mapped(
                    "call_off_remaining_qty"
                )
            ),
            0,
        )
        with (
            RecordCapturer(self.so_model, self.call_off_domain) as captured,
            freezegun.freeze_time("2026-12-31"),
        ):
            self.so_model._cron_manage_blanket_order_eol()
        self.assertEqual(len(captured.records), 0)

    def test_eol_with_call_off_in_progress(self):
        self.assertFalse(self.blanket_so.blanket_need_to_be_finalized)
        self.blanket_so.blanket_eol_strategy = "deliver"
        self.blanket_so.action_confirm()
        self.assertTrue(self.blanket_so.blanket_need_to_be_finalized)
        self.blanket_so.flush_recordset()
        # we create a call-of order for part of the quantity of
        # the product 1
        order = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "date_order": "2025-02-01",
                "partner_id": self.partner.id,
                "blanket_order_id": self.blanket_so.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_2.id,
                            "product_uom_qty": 5.0,
                        }
                    ),
                ],
            }
        )
        with freezegun.freeze_time("2025-11-12"):
            order.action_confirm()

        self.assertEqual(self.blanket_so.blanket_need_to_be_finalized, True)
        with (
            RecordCapturer(self.so_model, self.call_off_domain) as captured,
            freezegun.freeze_time("2026-12-31"),
        ):
            self.so_model._cron_manage_blanket_order_eol()
        self.assertFalse(self.blanket_so.blanket_need_to_be_finalized)
        self.assertEqual(len(captured.records), 1)
        new_call_off = captured.records[0]
        for line in self.blanket_so.order_line:
            self.assertEqual(line.call_off_remaining_qty, 0.0)
            call_off = line.call_off_line_ids
            if line.product_id == self.product_2:
                # 2 call-off lines should exist
                # one for the call-off order created in the past
                # and one for the new call-off order created by the cron
                self.assertEqual(len(call_off), 2)
                self.assertEqual(call_off.order_id, order | new_call_off)
                self.assertEqual(
                    set(call_off.mapped("product_uom_qty")),
                    {5, line.product_uom_qty - 5},
                )
            else:
                self.assertEqual(len(call_off), 1)
                self.assertEqual(call_off.product_uom_qty, line.product_uom_qty)
            self.assertTrue(line.move_ids)

    def test_eol_strategy_editable(self):
        # change is allowed in draft state
        self.blanket_so.blanket_eol_strategy = "deliver"
        self.blanket_so.blanket_eol_strategy = False
        self.blanket_so.action_confirm()
        # change is allowed after confirmation while the blanket order
        # is not finalized
        self.blanket_so.blanket_eol_strategy = "deliver"
        self.blanket_so._action_cancel()
        with (
            self.assertRaisesRegex(
                ValidationError, "The end-of-life strategy cannot be modified"
            ),
            self.env.cr.savepoint(),
        ):
            # change is not allowed on canceled order
            self.blanket_so.blanket_eol_strategy = False
        self.blanket_so.action_draft()
        # change is allowed in draft state
        self.blanket_so.blanket_eol_strategy = False
        self.blanket_so.action_confirm()
        with freezegun.freeze_time("2026-12-31"):
            self.so_model._cron_manage_blanket_order_eol()

        self.assertFalse(self.blanket_so.blanket_need_to_be_finalized)
        with (
            self.assertRaisesRegex(
                ValidationError, "The end-of-life strategy cannot be modified"
            ),
            self.env.cr.savepoint(),
        ):
            # change is not allowed on finalized order
            self.blanket_so.blanket_eol_strategy = "deliver"

    def test_update_qty(self):
        self.blanket_so.action_confirm()
        so_line_product_2 = self.blanket_so.order_line.filtered(
            lambda line: line.product_id == self.product_2
        )
        self.assertEqual(so_line_product_2.product_uom_qty, 10)
        so_line_product_2.product_uom_qty = 5
        self.assertEqual(so_line_product_2.product_uom_qty, 5)
        self.assertEqual(so_line_product_2.call_off_remaining_qty, 5)
        # if we deliver 3, we should not update the qty under the remaining qty
        order = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "date_order": "2025-02-01",
                "partner_id": self.partner.id,
                "blanket_order_id": self.blanket_so.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_2.id,
                            "product_uom_qty": 3.0,
                        }
                    ),
                ],
            }
        )
        with freezegun.freeze_time("2025-02-01"):
            order.action_confirm()
        self.assertEqual(so_line_product_2.call_off_remaining_qty, 2)
        with self.assertRaisesRegex(
            ValidationError, "The forecasted quantity cannot be less than the quantity"
        ):
            so_line_product_2.product_uom_qty = 1

    def test_price_unit_not_recomputed_on_confirmed_blanket_order_lines(self):
        self.blanket_so.action_confirm()
        so_line_product_2 = self.blanket_so.order_line.filtered(
            lambda line: line.product_id == self.product_2
        )
        original_price_unit = so_line_product_2.price_unit
        new_price = original_price_unit + 10
        self.product_2.list_price = new_price
        self.assertEqual(so_line_product_2.product_uom_qty, 10)
        so_line_product_2.product_uom_qty = 5
        self.assertEqual(so_line_product_2.price_unit, original_price_unit)
        # if we reset to draft and change the qty the price unit should be recomputed
        self.blanket_so._action_cancel()
        self.blanket_so.action_draft()
        so_line_product_2.product_uom_qty = 10
        self.assertEqual(so_line_product_2.price_unit, new_price)
