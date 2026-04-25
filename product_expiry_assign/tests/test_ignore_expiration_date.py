# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields
from odoo.tests.common import TransactionCase


class TestIgnoreExpirationDate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.picking_type_out = cls.warehouse.out_type_id
        cls.stock_location = cls.warehouse.lot_stock_id
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        # put product in stock in an expired lot
        cls.product = cls.env["product.product"].create(
            {
                "name": "TEST",
                "type": "consu",
                "is_storable": True,
                "use_expiration_date": True,
            }
        )

        cls.lot = cls.env["stock.lot"].create(
            {
                "name": "EXPIRED_LOT",
                "product_id": cls.product.id,
                "expiration_date": fields.Datetime.subtract(
                    fields.Datetime.now(), days=10
                ),
            }
        )
        cls.env["stock.quant"]._update_available_quantity(
            cls.product, cls.stock_location, quantity=10.0, lot_id=cls.lot
        )

    @classmethod
    def _create_move_out(cls, product, qty=1):
        """Create a delivery move with pick/pack/ship delivery steps."""
        return cls.env["stock.move"].create(
            {
                "name": product.name,
                "product_id": product.id,
                "product_uom_qty": qty,
                "product_uom": product.uom_id.id,
                "location_id": cls.stock_location.id,
                "location_dest_id": cls.customer_location.id,
                "picking_type_id": cls.picking_type_out.id,
                "warehouse_id": cls.warehouse.id,
                "procure_method": "make_to_stock",
            }
        )

    def test_company_ignore_expiration_date(self):
        """Force reservation of expired lots with the company parameter."""
        self.move_out = self._create_move_out(self.product, qty=10)
        self.move_out._action_confirm()
        self.move_out._action_assign()
        self.assertEqual(self.move_out.state, "confirmed")
        self.move_out.company_id.product_ignore_expiration_date = True
        self.move_out._action_assign()
        self.assertEqual(self.move_out.state, "assigned")

    def test_context_key_ignore_expiration_date(self):
        """Force reservation of expired lots with the context key."""
        self.move_out = self._create_move_out(self.product, qty=10)
        self.move_out._action_confirm()
        self.move_out._action_assign()
        self.assertEqual(self.move_out.state, "confirmed")
        self.move_out.with_context(ignore_expiration_date=True)._action_assign()
        self.assertEqual(self.move_out.state, "assigned")
