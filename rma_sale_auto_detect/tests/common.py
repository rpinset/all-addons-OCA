# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import Command
from odoo.fields import Date
from odoo.tests.common import TransactionCase


class TestRmaSaleAutoDetectBase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Customer"})
        cls.partner2 = cls.env["res.partner"].create({"name": "Customer 2"})
        cls.product = cls.env["product.product"].create(
            {"name": "Test Product", "type": "consu", "is_storable": True}
        )
        cls.product2 = cls.env["product.product"].create(
            {"name": "Test Product 2", "type": "consu", "is_storable": True}
        )
        cls.operation = cls.env["rma.operation"].create(
            {"name": "Warranty Return", "return_eligibility_days": 30}
        )
        cls.loc_stock = cls.env.ref("stock.stock_location_stock")
        cls.env["stock.quant"]._update_available_quantity(
            cls.product, cls.loc_stock, 100
        )
        cls.env["stock.quant"]._update_available_quantity(
            cls.product2, cls.loc_stock, 100
        )

    def _create_and_confirm_sale_order(self, partner, products, timedelta_days):
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "order_line": [
                    Command.create({"product_id": product.id, "product_uom_qty": qty})
                    for product, qty in products
                ],
            }
        )
        sale_order.action_confirm()
        sale_order.date_order = Date.today() - timedelta(days=timedelta_days)
        return sale_order

    def _process_picking(self, picking, product, qty):
        move = picking.move_ids.filtered(
            lambda m: m.product_id == product and m.state == "assigned"
        )
        move.quantity = qty
        move.picked = True
        move._action_done()
        self.assertEqual(move.state, "done")

    def _create_rma(self, partner, product, qty, operation):
        return self.env["rma"].create(
            {
                "partner_id": partner.id,
                "product_id": product.id,
                "operation_id": operation.id,
                "product_uom_qty": qty,
            }
        )
