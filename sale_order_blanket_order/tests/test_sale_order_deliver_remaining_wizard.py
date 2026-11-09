import freezegun

from odoo import Command
from odoo.exceptions import UserError

from .common import SaleOrderBlanketOrderCase


class TestSaleOrderDeliverRemainingWizard(SaleOrderBlanketOrderCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.blanket_so.action_confirm()

    @classmethod
    def _get_wizard(self, sale_order):
        wizard_action = sale_order.action_deliver_remaining()
        wizard = self.env["sale.order.deliver.remaining.wizard"].browse(
            wizard_action["res_id"]
        )
        return wizard

    @freezegun.freeze_time("2025-02-01")
    def test_wizard_shows_only_products_remaining(self):
        call_off_so = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "blanket_order_id": self.blanket_so.id,
                "partner_id": self.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_1.id,
                            "product_uom_qty": 5.0,
                            "price_unit": 0,
                        }
                    ),
                    Command.create(
                        {
                            "product_id": self.product_2.id,
                            "product_uom_qty": 5.0,
                            "price_unit": 0,
                        }
                    ),
                ],
            }
        )
        call_off_so.action_confirm()
        wizard = self._get_wizard(self.blanket_so)
        self.assertEqual(wizard.order_id, self.blanket_so)
        self.assertEqual(len(wizard.wizard_line_ids), 3)
        self.assertListEqual(
            [line.call_off_remaining_qty for line in wizard.wizard_line_ids],
            [line.qty_to_deliver for line in wizard.wizard_line_ids],
            "The 'qty_to_deliver' field should be set to the 'call_off_remaining_qty'"
            "by default at wizard creation",
        )
        self.assertEqual(wizard.wizard_line_ids[0].call_off_remaining_qty, 5)
        self.assertEqual(wizard.wizard_line_ids[1].call_off_remaining_qty, 10)
        self.assertEqual(wizard.wizard_line_ids[2].call_off_remaining_qty, 5)

    def test_action_create_call_off_no_lines(self):
        wizard = self._get_wizard(self.blanket_so)
        wizard.wizard_line_ids = [Command.clear()]
        with self.assertRaises(UserError):
            wizard.action_create_call_off()

    def test_wizard_invalid_quantity(self):
        wizard = self._get_wizard(self.blanket_so)
        with self.assertRaises(UserError), self.env.cr.savepoint():
            wizard.wizard_line_ids[0].qty_to_deliver = -1
        with self.assertRaises(UserError):
            wizard.wizard_line_ids[0].qty_to_deliver = 1000

    def test_action_create_call_off(self):
        wizard = self._get_wizard(self.blanket_so)
        wizard.wizard_line_ids = wizard.wizard_line_ids[0]
        wizard.wizard_line_ids[0].qty_to_deliver = 5
        wizard_action = wizard.action_create_call_off()
        call_off_order = self.env["sale.order"].browse(wizard_action["res_id"])

        self.assertEqual(call_off_order.order_type, "call_off")
        self.assertEqual(call_off_order.blanket_order_id, self.blanket_so)
        self.assertEqual(len(call_off_order.order_line), 1)
        self.assertEqual(call_off_order.order_line[0].product_uom_qty, 5)
        self.assertEqual(call_off_order.order_line[0].price_unit, 0.0)
        self.assertEqual(call_off_order.partner_id, self.blanket_so.partner_id)
        self.assertEqual(
            call_off_order.partner_invoice_id, self.blanket_so.partner_invoice_id
        )
        self.assertEqual(
            call_off_order.partner_shipping_id, self.blanket_so.partner_shipping_id
        )
        self.assertEqual(call_off_order.pricelist_id, self.blanket_so.pricelist_id)
        self.assertEqual(call_off_order.origin, self.blanket_so.name)
