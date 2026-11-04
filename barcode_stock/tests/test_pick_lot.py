# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import defaultdict
from datetime import timedelta

from odoo import Command, fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestBarcodePickLot(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Quant = cls.env["stock.quant"]
        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.stock = cls.warehouse.lot_stock_id
        cls.customers = cls.env.ref("stock.stock_location_customers")
        Location = cls.env["stock.location"]
        cls.shelf_1 = Location.create({"name": "Shelf 1", "location_id": cls.stock.id})
        cls.shelf_2 = Location.create({"name": "Shelf 2", "location_id": cls.stock.id})
        cls.product = cls.env["product.product"].create(
            {"name": "Duck confit", "is_storable": True, "tracking": "lot"}
        )
        Lot = cls.env["stock.lot"]
        cls.lot_x = Lot.create({"name": "X", "product_id": cls.product.id})
        cls.lot_b = Lot.create({"name": "B", "product_id": cls.product.id})
        # Lot X is the oldest, so deliveries reserve it first; lot B lies on
        # both shelves.
        now = fields.Datetime.now()
        for location, lot, quantity, days in (
            (cls.shelf_1, cls.lot_x, 5, 10),
            (cls.shelf_1, cls.lot_b, 2, 9),
            (cls.shelf_2, cls.lot_b, 3, 8),
        ):
            cls.Quant._update_available_quantity(
                cls.product,
                location,
                quantity,
                lot_id=lot,
                in_date=now - timedelta(days=days),
            )

    def _delivery(self, quantity):
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.warehouse.out_type_id.id,
                "location_id": self.stock.id,
                "location_dest_id": self.customers.id,
                "move_ids": [
                    Command.create(
                        {
                            "name": self.product.name,
                            "product_id": self.product.id,
                            "product_uom_qty": quantity,
                            "location_id": self.stock.id,
                            "location_dest_id": self.customers.id,
                        }
                    )
                ],
            }
        )
        picking.action_confirm()
        picking.action_assign()
        return picking

    def _stock(self):
        """What is on hand, by shelf, lot, package and owner."""
        stock = defaultdict(float)
        quants = self.Quant.search(
            [
                ("product_id", "=", self.product.id),
                ("location_id.usage", "=", "internal"),
            ]
        )
        for quant in quants:
            key = (
                quant.location_id.name,
                quant.lot_id.name,
                quant.package_id.name or False,
                quant.owner_id.name or False,
            )
            stock[key] += quant.quantity
        return stock

    def _lines(self, picking):
        return [
            (line.lot_id.name, line.location_id.name, line.quantity, line.qty_picked)
            for line in picking.move_line_ids.sorted("id")
        ]

    def test_a_lot_spread_over_its_shelves(self):
        picking = self._delivery(5)
        self.assertEqual(self._lines(picking), [("X", "Shelf 1", 5, 0)])
        picking.move_ids.barcode_pick_lot(self.lot_b.id, 5)
        # Lot X's reservation gives way; lot B is taken from both shelves.
        self.assertEqual(
            self._lines(picking), [("B", "Shelf 1", 2, 2), ("B", "Shelf 2", 3, 3)]
        )
        picking.button_validate()
        stock = self._stock()
        self.assertEqual(stock["Shelf 1", "X", False, False], 5)
        self.assertEqual(stock["Shelf 1", "B", False, False], 0)
        self.assertEqual(stock["Shelf 2", "B", False, False], 0)
        self.assertFalse([key for key, qty in stock.items() if qty < 0])

    def test_only_what_the_lot_replaces_is_released(self):
        picking = self._delivery(4)
        picking.move_ids.barcode_pick_lot(self.lot_b.id, 1)
        self.assertEqual(
            self._lines(picking), [("X", "Shelf 1", 3, 0), ("B", "Shelf 1", 1, 1)]
        )

    def test_released_from_the_last_lines(self):
        lot_c = self.env["stock.lot"].create(
            {"name": "C", "product_id": self.product.id}
        )
        self.Quant._update_available_quantity(
            self.product, self.shelf_2, 1, lot_id=lot_c
        )
        picking = self._delivery(9)
        picking.move_ids.barcode_pick_lot(lot_c.id, 1)
        self.assertEqual(
            self._lines(picking),
            [
                ("X", "Shelf 1", 5, 0),
                ("B", "Shelf 1", 2, 0),
                ("B", "Shelf 2", 1, 0),
                ("C", "Shelf 2", 1, 1),
            ],
        )

    def test_only_what_it_takes_is_picked(self):
        # Lot B already has two lines, Shelf 2's holding 2 of its 3.
        picking = self._delivery(9)
        picking.move_ids.barcode_pick_lot(self.lot_b.id, 1)
        # The third unit gets a line of its own, the only one picked.
        self.assertEqual(
            self._lines(picking),
            [
                ("X", "Shelf 1", 4, 0),
                ("B", "Shelf 1", 2, 0),
                ("B", "Shelf 2", 2, 0),
                ("B", "Shelf 2", 1, 1),
            ],
        )

    def test_what_a_partly_picked_lot_still_holds_is_released(self):
        picking = self._delivery(5)
        picking.move_line_ids.qty_picked = 2
        picking.move_ids.barcode_pick_lot(self.lot_b.id, 3)
        # Lot X keeps the 2 picked, its other 3 make room for lot B.
        self.assertEqual(
            self._lines(picking),
            [("X", "Shelf 1", 2, 2), ("B", "Shelf 1", 2, 2), ("B", "Shelf 2", 1, 1)],
        )
        # A line fully picked gives nothing back.
        picking.move_line_ids[0].qty_picked = 2
        lot_c = self.env["stock.lot"].create(
            {"name": "C", "product_id": self.product.id}
        )
        self.Quant._update_available_quantity(
            self.product, self.shelf_2, 1, lot_id=lot_c
        )
        picking.move_ids.barcode_pick_lot(lot_c.id, 1)
        self.assertEqual(self._lines(picking)[0], ("X", "Shelf 1", 2, 2))

    def test_stock_without_a_lot_is_left_alone(self):
        lot_d = self.env["stock.lot"].create(
            {"name": "D", "product_id": self.product.id}
        )
        self.Quant._update_available_quantity(
            self.product, self.shelf_2, 2, lot_id=lot_d
        )
        self.Quant._update_available_quantity(self.product, self.shelf_2, 3)
        picking = self._delivery(5)
        picking.move_ids.barcode_pick_lot(lot_d.id, 3)
        lines = picking.move_line_ids.filtered("picked")
        self.assertEqual(lines.lot_id, lot_d)
        self.assertEqual(lines.mapped("quantity"), [2])
        self.assertEqual(lines.mapped("qty_picked"), [3])
        lotless = self.Quant.search(
            [("product_id", "=", self.product.id), ("lot_id", "=", False)]
        )
        self.assertEqual(lotless.reserved_quantity, 0)

    def test_packaged_and_consigned_stock(self):
        package = self.env["stock.quant.package"].create({"name": "PK1"})
        owner = self.env["res.partner"].create({"name": "Consignor"})
        lot_p = self.env["stock.lot"].create(
            {"name": "P", "product_id": self.product.id}
        )
        self.Quant._update_available_quantity(
            self.product,
            self.shelf_2,
            3,
            lot_id=lot_p,
            package_id=package,
            owner_id=owner,
        )
        picking = self._delivery(3)
        picking.move_ids.barcode_pick_lot(lot_p.id, 3)
        line = picking.move_line_ids
        self.assertEqual(
            (line.lot_id, line.location_id, line.package_id, line.owner_id),
            (lot_p, self.shelf_2, package, owner),
        )
        picking.button_validate()
        stock = self._stock()
        self.assertEqual(stock["Shelf 2", "P", "PK1", "Consignor"], 0)
        self.assertFalse([key for key, qty in stock.items() if qty < 0])

    def test_more_than_the_lot_holds(self):
        picking = self._delivery(5)
        picking.move_ids.barcode_pick_lot(self.lot_b.id, 6)
        # What is over goes on the last line.
        self.assertEqual(
            self._lines(picking), [("B", "Shelf 1", 2, 2), ("B", "Shelf 2", 3, 4)]
        )
        # As Odoo allows it: validating leaves a negative quant on that shelf,
        # which shows the gap.
        picking.button_validate()
        stock = self._stock()
        self.assertEqual(stock["Shelf 1", "B", False, False], 0)
        self.assertEqual(stock["Shelf 2", "B", False, False], -1)

    def test_a_destination_the_operator_chose(self):
        picking = self._delivery(5)
        picking.move_ids.barcode_pick_lot(self.lot_b.id, 5, False, self.shelf_2.id)
        self.assertEqual(picking.move_line_ids.mapped("location_dest_id"), self.shelf_2)

    def test_stock_another_move_holds(self):
        first = self._delivery(5)
        # The second delivery holds all of lot B.
        second = self._delivery(5)
        self.assertEqual({line[0] for line in self._lines(second)}, {"B"})
        first.move_ids.barcode_pick_lot(self.lot_b.id, 5)
        self.assertEqual(
            self._lines(first), [("B", "Shelf 1", 2, 2), ("B", "Shelf 2", 3, 3)]
        )
        first.button_validate()
        stock = self._stock()
        self.assertEqual(stock["Shelf 1", "B", False, False], 0)
        self.assertEqual(stock["Shelf 2", "B", False, False], 0)
        self.assertFalse([key for key, qty in stock.items() if qty < 0])
        # Its hold on lot B freed, the second delivery takes what is left: the
        # lot X the first one gave up.
        self.assertEqual(self._lines(second), [("X", "Shelf 1", 5, 0)])

    def _lot_in_packages(self, *packages):
        """Lot P in packages on Shelf 2, the first the oldest."""
        lot_p = self.env["stock.lot"].create(
            {"name": "P", "product_id": self.product.id}
        )
        now = fields.Datetime.now()
        for days, (name, quantity) in enumerate(packages):
            self.Quant._update_available_quantity(
                self.product,
                self.shelf_2,
                quantity,
                lot_id=lot_p,
                package_id=self.env["stock.quant.package"].create({"name": name}),
                in_date=now - timedelta(days=7 - days),
            )
        return lot_p

    def _least_packages(self):
        self.product.categ_id = self.env["product.category"].create(
            {
                "name": "Least packages",
                "removal_strategy_id": self.env.ref("stock.removal_least_packages").id,
            }
        )

    def _packages(self, picking):
        return sorted(
            (line.package_id.name, line.qty_picked) for line in picking.move_line_ids
        )

    def test_the_fewest_packages(self):
        lot_p = self._lot_in_packages(("PK1", 3), ("PK2", 2), ("PK3", 5))
        picking = self._delivery(5)
        self._least_packages()
        picking.move_ids.barcode_pick_lot(lot_p.id, 5)
        # The package that holds it all rather than the two oldest.
        self.assertEqual(self._packages(picking), [("PK3", 5)])

    def test_the_fewest_packages_and_stock_another_move_holds(self):
        lot_p = self._lot_in_packages(("PK1", 5), ("PK2", 3))
        first = self._delivery(5)
        self._least_packages()
        # The second delivery holds the package that holds it all.
        second = self._delivery(5)
        self.assertEqual(self._packages(second), [("PK1", 0)])
        first.move_ids.barcode_pick_lot(lot_p.id, 5)
        # The free package first, the rest from the held one.
        self.assertEqual(self._packages(first), [("PK1", 2), ("PK2", 3)])
        first.button_validate()
        stock = self._stock()
        self.assertEqual(stock["Shelf 2", "P", "PK1", False], 3)
        self.assertEqual(stock["Shelf 2", "P", "PK2", False], 0)
        self.assertFalse([key for key, qty in stock.items() if qty < 0])

    def test_a_source_the_operator_chose(self):
        picking = self._delivery(3)
        picking.move_ids.barcode_pick_lot(self.lot_b.id, 3, self.shelf_2.id)
        self.assertEqual(self._lines(picking), [("B", "Shelf 2", 3, 3)])

    def test_a_lot_with_no_stock(self):
        lot_z = self.env["stock.lot"].create(
            {"name": "Z", "product_id": self.product.id}
        )
        picking = self._delivery(2)
        with self.assertRaises(UserError):
            picking.move_ids.barcode_pick_lot(lot_z.id, 2)
        # From a source the operator chose, it is picked there.
        picking.move_ids.barcode_pick_lot(lot_z.id, 2, self.shelf_2.id)
        self.assertEqual(self._lines(picking), [("Z", "Shelf 2", 2, 2)])
