# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestBarcodeInventory(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Inventory = cls.env["stock.inventory"]
        cls.location = cls.env["stock.location"].create(
            {
                "name": "Barcode Count Shelf",
                "usage": "internal",
                "location_id": cls.env.ref("stock.stock_location_stock").id,
            }
        )
        cls.storable = cls.env["product.product"].create(
            {"name": "Count Storable", "is_storable": True}
        )
        cls.consumable = cls.env["product.product"].create(
            {"name": "Count Consumable", "type": "consu", "is_storable": False}
        )
        cls.service = cls.env["product.product"].create(
            {"name": "Count Service", "type": "service"}
        )

    def test_apply_count_storable(self):
        result = self.Inventory.action_barcode_apply_count(
            self.location.id,
            [{"product_id": self.storable.id, "counted_qty": 5}],
        )
        self.assertEqual(result["adjusted"], 1)
        self.assertEqual(
            self.env["stock.quant"]._get_available_quantity(
                self.storable, self.location
            ),
            5,
        )

    def test_apply_count_refuses_non_storable(self):
        for product in (self.consumable, self.service):
            with (
                self.subTest(product=product.name),
                self.assertRaisesRegex(UserError, "not a storable product"),
            ):
                self.Inventory.action_barcode_apply_count(
                    self.location.id,
                    [{"product_id": product.id, "counted_qty": 1}],
                )
