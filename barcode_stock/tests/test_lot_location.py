# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestBarcodeLotLocation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Quant = cls.env["stock.quant"]
        cls.stock = cls.env.ref("stock.stock_location_stock")
        Location = cls.env["stock.location"]
        cls.shelf_1 = Location.create({"name": "Shelf 1", "location_id": cls.stock.id})
        cls.shelf_2 = Location.create({"name": "Shelf 2", "location_id": cls.stock.id})
        cls.category = cls.env["product.category"].create({"name": "Barcode lots"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Duck confit",
                "is_storable": True,
                "tracking": "lot",
                "categ_id": cls.category.id,
            }
        )
        cls.lot = cls.env["stock.lot"].create(
            {"name": "6077102", "product_id": cls.product.id}
        )
        cls.other_lot = cls.env["stock.lot"].create(
            {"name": "6077103", "product_id": cls.product.id}
        )
        # The lot came in on Shelf 1 first, then on Shelf 2.
        now = fields.Datetime.now()
        cls.Quant._update_available_quantity(
            cls.product, cls.shelf_1, 3, lot_id=cls.lot, in_date=now - timedelta(days=9)
        )
        cls.Quant._update_available_quantity(
            cls.product, cls.shelf_2, 3, lot_id=cls.lot, in_date=now
        )

    def _where(self, lot=None, location=None):
        return self.Quant.barcode_lot_location(
            self.product.id, (lot or self.lot).id, (location or self.stock).id
        )

    def test_first_in_first_out(self):
        self.assertEqual(self._where(), [self.shelf_1.id, "WH/Stock/Shelf 1"])

    def test_the_removal_strategy_decides(self):
        self.category.removal_strategy_id = self.env.ref("stock.removal_lifo")
        self.assertEqual(self._where()[0], self.shelf_2.id)

    def test_stock_reserved_for_others_comes_last(self):
        self.Quant._update_reserved_quantity(
            self.product, self.shelf_1, 3, lot_id=self.lot
        )
        self.assertEqual(self._where()[0], self.shelf_2.id)
        # All of it reserved: still where it lies, Odoo frees the reservation.
        self.Quant._update_reserved_quantity(
            self.product, self.shelf_2, 3, lot_id=self.lot
        )
        self.assertEqual(self._where()[0], self.shelf_1.id)

    def test_no_stock_there(self):
        # Only under the location asked.
        self.assertEqual(self._where(location=self.shelf_2)[0], self.shelf_2.id)
        # Neither stock without a lot, nor a lot's negative quant, counts.
        self.Quant._update_available_quantity(self.product, self.shelf_1, 4)
        self.Quant._update_available_quantity(
            self.product, self.shelf_2, -2, lot_id=self.other_lot
        )
        self.assertFalse(self._where(lot=self.other_lot))
