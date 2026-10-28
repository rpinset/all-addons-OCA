# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command
from odoo.tests.common import TransactionCase, new_test_user


class TestDeliveryZoneChange(TransactionCase):
    """The scanner changes an operation's zone with a plain write on the
    picking, as the operator: `partner_delivery_zone` then carries it on to the
    sale order. A warehouse user without any sales right must be able to."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Zone = cls.env["partner.delivery.zone"]
        cls.north = Zone.create({"name": "North"})
        cls.south = Zone.create({"name": "South"})
        partner = cls.env["res.partner"].create(
            {"name": "Zone Customer", "delivery_zone_id": cls.north.id}
        )
        product = cls.env["product.product"].create(
            {"name": "Zone Product", "is_storable": True}
        )
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "order_line": [
                    Command.create({"product_id": product.id, "product_uom_qty": 1})
                ],
            }
        )
        cls.order.action_confirm()
        cls.picking = cls.order.picking_ids
        cls.clerk = new_test_user(
            cls.env, login="zone_clerk", groups="stock.group_stock_user"
        )

    def test_warehouse_user_changes_the_zone(self):
        self.assertFalse(self.clerk.has_group("sales_team.group_sale_salesman"))
        self.assertEqual(self.picking.delivery_zone_id, self.north)
        picking = self.picking.with_user(self.clerk)
        picking.write({"delivery_zone_id": self.south.id})
        self.assertEqual(self.picking.delivery_zone_id, self.south)
        self.assertEqual(self.order.delivery_zone_id, self.south)
        picking.write({"delivery_zone_id": False})
        self.assertFalse(self.picking.delivery_zone_id)
        self.assertFalse(self.order.delivery_zone_id)
