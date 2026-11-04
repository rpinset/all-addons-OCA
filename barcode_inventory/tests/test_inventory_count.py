# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo import Command
from odoo.exceptions import AccessError, UserError
from odoo.tests.common import TransactionCase, new_test_user


class TestBarcodeInventoryCount(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Inventory = cls.env["stock.inventory"]
        cls.Quant = cls.env["stock.quant"]
        cls.company = cls.env.company
        cls.location = cls.env["stock.location"].create(
            {
                "name": "Barcode Count Shelf",
                "usage": "internal",
                "location_id": cls.env.ref("stock.stock_location_stock").id,
                "company_id": cls.company.id,
            }
        )
        cls.sublocation = cls.env["stock.location"].create(
            {
                "name": "Barcode Count Bin",
                "usage": "internal",
                "location_id": cls.location.id,
                "company_id": cls.company.id,
            }
        )
        Product = cls.env["product.product"]
        cls.product = Product.create({"name": "Count Untracked", "is_storable": True})
        cls.lot_product = Product.create(
            {"name": "Count Lot", "is_storable": True, "tracking": "lot"}
        )
        cls.serial_product = Product.create(
            {"name": "Count Serial", "is_storable": True, "tracking": "serial"}
        )
        cls.new_product = Product.create({"name": "Count New", "is_storable": True})
        cls.consumable = Product.create({"name": "Count Consumable", "type": "consu"})
        cls.lot = cls.env["stock.lot"].create(
            {
                "name": "LOT-COUNT-1",
                "product_id": cls.lot_product.id,
                "company_id": cls.company.id,
            }
        )
        cls.serial = cls.env["stock.lot"].create(
            {
                "name": "SN-COUNT-1",
                "product_id": cls.serial_product.id,
                "company_id": cls.company.id,
            }
        )
        cls.package = cls.env["stock.quant.package"].create({"name": "COUNT-PACK"})
        cls.owner = cls.env["res.partner"].create({"name": "Count Owner"})
        Quant = cls.Quant
        Quant._update_available_quantity(cls.product, cls.location, 10)
        Quant._update_available_quantity(cls.product, cls.sublocation, 3)
        Quant._update_available_quantity(
            cls.product, cls.location, 4, package_id=cls.package
        )
        Quant._update_available_quantity(
            cls.product, cls.location, 2, owner_id=cls.owner
        )
        Quant._update_available_quantity(
            cls.lot_product, cls.location, 5, lot_id=cls.lot
        )
        Quant._update_available_quantity(
            cls.serial_product, cls.location, 1, lot_id=cls.serial
        )

    def _qty(self, product, lot=None, location=None, package=None, owner=None):
        """What a location holds of a product and lot, loose and unowned unless
        a package or owner is given."""
        quants = self.Quant.search(
            [
                ("product_id", "=", product.id),
                ("location_id", "=", (location or self.location).id),
                ("lot_id", "=", lot.id if lot else False),
                ("package_id", "=", package.id if package else False),
                ("owner_id", "=", owner.id if owner else False),
            ]
        )
        return sum(quants.mapped("quantity"))

    # --- the lines shown before counting --------------------------------------

    def test_location_lines(self):
        data = self.Inventory.action_barcode_location_lines(self.location.id)
        self.assertEqual(data["location_id"], self.location.id)
        self.assertEqual(data["location_name"], self.location.display_name)
        lines = {(line["product_id"], line["lot_id"]): line for line in data["lines"]}
        # Only the stock at the location itself, loose and unowned: not the
        # sublocation, the package or the partner's.
        self.assertEqual(lines[self.product.id, False]["theoretical_qty"], 10)
        self.assertEqual(lines[self.product.id, False]["lot_name"], False)
        self.assertEqual(lines[self.product.id, False]["uom"], self.product.uom_id.name)
        lot_line = lines[self.lot_product.id, self.lot.id]
        self.assertEqual(lot_line["lot_name"], "LOT-COUNT-1")
        self.assertEqual(lot_line["tracking"], "lot")
        self.assertEqual(lot_line["theoretical_qty"], 5)
        self.assertEqual(len(data["lines"]), 3)

    def test_location_lines_one_per_product_and_lot(self):
        # The same stock split over two quants, and stock that nets to zero.
        self.Quant.sudo().create(
            {
                "product_id": self.lot_product.id,
                "location_id": self.location.id,
                "lot_id": self.lot.id,
                "quantity": 2,
            }
        )
        for quantity in (3, -3):
            self.Quant.sudo().create(
                {
                    "product_id": self.new_product.id,
                    "location_id": self.location.id,
                    "quantity": quantity,
                }
            )
        data = self.Inventory.action_barcode_location_lines(self.location.id)
        lots = [
            line for line in data["lines"] if line["product_id"] == self.lot_product.id
        ]
        self.assertEqual(len(lots), 1)
        self.assertEqual(lots[0]["theoretical_qty"], 7)
        self.assertNotIn(
            self.new_product.id, [line["product_id"] for line in data["lines"]]
        )

    def test_location_lines_for_a_warehouse_user(self):
        user = new_test_user(
            self.env, login="barcode_count_user", groups="stock.group_stock_user"
        )
        data = self.Inventory.with_user(user).action_barcode_location_lines(
            self.location.id
        )
        self.assertEqual(len(data["lines"]), 3)

    def test_invalid_location(self):
        view = self.env["stock.location"].create(
            {"name": "Barcode Count View", "usage": "view"}
        )
        with self.assertRaises(UserError):
            self.Inventory.action_barcode_location_lines(view.id)
        with self.assertRaises(UserError):
            self.Inventory.action_barcode_apply_count(
                0, [{"product_id": self.product.id}]
            )

    # --- lots -----------------------------------------------------------------

    def test_lot_matched_exactly_then_in_another_case(self):
        resolve = self.Inventory._barcode_resolve_lot
        self.assertEqual(
            resolve(self.lot_product, "LOT-COUNT-1", self.company), self.lot
        )
        self.assertEqual(
            resolve(self.lot_product, "lot-count-1", self.company), self.lot
        )
        # Lots that differ only in case are distinct: the exact one wins, and
        # a name matching several of them in another case is refused.
        upper, lower = self.env["stock.lot"].create(
            [
                {"name": "DUP", "product_id": self.lot_product.id},
                {"name": "dup", "product_id": self.lot_product.id},
            ]
        )
        self.assertEqual(resolve(self.lot_product, "DUP", self.company), upper)
        self.assertEqual(resolve(self.lot_product, "dup", self.company), lower)
        with self.assertRaises(UserError):
            resolve(self.lot_product, "Dup", self.company)

    def test_lot_name_wildcards_are_plain_characters(self):
        lot = self.env["stock.lot"].create(
            {"name": "LOT_A%", "product_id": self.lot_product.id}
        )
        resolve = self.Inventory._barcode_resolve_lot
        self.assertEqual(resolve(self.lot_product, "lot_a%", self.company), lot)
        created = resolve(self.lot_product, "LOTXAB", self.company)
        self.assertNotEqual(created, lot)
        self.assertEqual(created.name, "LOTXAB")

    def test_new_lot_company(self):
        other = self.env["res.company"].create({"name": "Barcode Count Co"})
        resolve = self.Inventory._barcode_resolve_lot
        # A shared product gets the lot in the counted location's company...
        lot = resolve(self.lot_product, "LOT-OTHER", other)
        self.assertEqual(lot.company_id, other)
        # ...and a company's product keeps it in its own.
        own_product = self.env["product.product"].create(
            {
                "name": "Count Own Lot",
                "is_storable": True,
                "tracking": "lot",
                "company_id": self.company.id,
            }
        )
        lot = resolve(own_product, "LOT-OWN", other)
        self.assertEqual(lot.company_id, self.company)

    # --- checks before applying -----------------------------------------------

    def test_lines_that_cannot_be_applied(self):
        apply = self.Inventory.action_barcode_apply_count
        cases = [
            [],
            [{"product_id": 0, "counted_qty": 1}],
            [{"product_id": self.consumable.id, "counted_qty": 1}],
            [{"product_id": self.product.id, "counted_qty": -1}],
            [{"product_id": self.product.id, "counted_qty": "twelve"}],
            [{"product_id": self.product.id, "counted_qty": "nan"}],
            [{"product_id": self.product.id, "counted_qty": "inf"}],
            # An infinite number reaches the server as JSON null.
            [{"product_id": self.product.id, "counted_qty": None}],
            [{"product_id": self.lot_product.id, "lot_name": " ", "counted_qty": 1}],
            [
                {"product_id": self.serial_product.id, "lot_name": "SN-COUNT-1"},
                {
                    "product_id": self.serial_product.id,
                    "lot_name": "SN-NEW",
                    "counted_qty": 2,
                },
            ],
            # The same serial number on two lines adds up to two units.
            [
                {
                    "product_id": self.serial_product.id,
                    "lot_name": "SN-COUNT-1",
                    "counted_qty": 1,
                },
                {
                    "product_id": self.serial_product.id,
                    "lot_name": "SN-COUNT-1",
                    "counted_qty": 1,
                },
            ],
        ]
        for lines in cases:
            with self.subTest(lines=lines), self.assertRaises(UserError):
                apply(self.location.id, lines)
        self.assertFalse(
            self.Inventory.search([("location_ids", "=", self.location.id)])
        )

    def test_only_inventory_administrators_apply(self):
        user = new_test_user(
            self.env, login="barcode_count_clerk", groups="stock.group_stock_user"
        )
        with self.assertRaises(AccessError):
            self.Inventory.with_user(user).action_barcode_apply_count(
                self.location.id, [{"product_id": self.product.id, "counted_qty": 1}]
            )

    # --- applying -------------------------------------------------------------

    def test_apply_count(self):
        result = self.Inventory.action_barcode_apply_count(
            self.location.id,
            [
                {"product_id": self.product.id, "counted_qty": 7},
                {
                    "product_id": self.lot_product.id,
                    "lot_name": "LOT-COUNT-1",
                    "counted_qty": 4,
                },
                {
                    "product_id": self.lot_product.id,
                    "lot_name": "lot-count-1",
                    "counted_qty": 2,
                },
                {
                    "product_id": self.lot_product.id,
                    "lot_name": "LOT-NEW",
                    "counted_qty": 3,
                },
                {
                    "product_id": self.serial_product.id,
                    "lot_name": "SN-COUNT-1",
                    "counted_qty": 0,
                },
                {"product_id": self.new_product.id, "counted_qty": 8},
            ],
        )
        new_lot = self.env["stock.lot"].search(
            [("product_id", "=", self.lot_product.id), ("name", "=", "LOT-NEW")]
        )
        self.assertEqual(new_lot.company_id, self.company)
        self.assertEqual(self._qty(self.product), 7)
        # Two lines of the same lot count the same stock: they add up.
        self.assertEqual(self._qty(self.lot_product, self.lot), 6)
        self.assertEqual(self._qty(self.lot_product, new_lot), 3)
        self.assertEqual(self._qty(self.serial_product, self.serial), 0)
        self.assertEqual(self._qty(self.new_product), 8)
        # What the count does not cover is left as it was.
        self.assertEqual(self._qty(self.product, location=self.sublocation), 3)
        self.assertEqual(self._qty(self.product, package=self.package), 4)
        self.assertEqual(self._qty(self.product, owner=self.owner), 2)

        group = self.Inventory.browse(result["group_id"])
        self.assertEqual(result["adjusted"], 5)
        self.assertEqual(result["group_name"], group.name)
        self.assertIn(self.location.display_name, group.name)
        self.assertEqual(group.state, "done")
        self.assertEqual(group.company_id, self.company)
        self.assertEqual(group.location_ids, self.location)
        self.assertTrue(group.exclude_sublocation)
        self.assertEqual(group.product_selection, "manual")
        self.assertEqual(
            group.product_ids,
            self.product | self.lot_product | self.serial_product | self.new_product,
        )
        # One move per counted product and lot, the new stock included.
        self.assertEqual(result["move_count"], 5)
        self.assertEqual(
            group.stock_move_ids.product_id,
            self.product | self.lot_product | self.serial_product | self.new_product,
        )
        self.assertEqual(set(group.stock_move_ids.mapped("state")), {"done"})
        # The adjustment holds the quants counted: none in a package, owned by
        # a partner or in the sublocation.
        self.assertTrue(group.stock_quant_ids)
        self.assertFalse(
            group.stock_quant_ids.filtered(
                lambda q: q.package_id or q.owner_id or q.location_id != self.location
            )
        )
        self.assertFalse(
            self.Quant.search(
                ["|", ("current_inventory_id", "=", group.id), ("to_do", "=", True)]
            )
        )
        self.assertFalse(
            self.Quant.search(
                [
                    ("location_id", "=", self.location.id),
                    ("inventory_quantity_set", "=", True),
                ]
            )
        )

    def test_other_adjustments_take_their_usual_quants(self):
        group = self.Inventory.create(
            {
                "name": "Back office count",
                "location_ids": [Command.set(self.location.ids)],
                "exclude_sublocation": True,
                "product_selection": "manual",
                "product_ids": [Command.set(self.product.ids)],
            }
        )
        quants = group._get_quants(self.location)
        self.assertTrue(quants.filtered("package_id"))
        self.assertTrue(quants.filtered("owner_id"))

    def test_count_not_applied_is_not_done(self):
        # Should Odoo hand back a wizard instead of applying the count, the
        # count fails: no adjustment is recorded as done.
        wizard = {
            "type": "ir.actions.act_window",
            "res_model": "stock.inventory.conflict",
        }
        Quant = type(self.env["stock.quant"])
        with (
            patch.object(Quant, "action_apply_inventory", return_value=wizard),
            self.assertRaises(UserError),
        ):
            self.Inventory.action_barcode_apply_count(
                self.location.id, [{"product_id": self.product.id, "counted_qty": 3}]
            )
        self.assertFalse(
            self.Inventory.search(
                [("location_ids", "=", self.location.id), ("state", "=", "done")]
            )
        )

    def test_stock_changed_while_counting(self):
        data = self.Inventory.action_barcode_location_lines(self.location.id)
        shown = {(line["product_id"], line["lot_name"]): line for line in data["lines"]}
        # Goods come in after the screen showed the stock.
        self.Quant._update_available_quantity(self.product, self.location, 5)
        lines = [
            {
                "product_id": self.product.id,
                "counted_qty": 8,
                "theoretical_qty": shown[self.product.id, False]["theoretical_qty"],
            },
            {
                "product_id": self.lot_product.id,
                "lot_name": "LOT-COUNT-1",
                "counted_qty": 5,
                "theoretical_qty": 5,
            },
            # A lot not created yet held nothing, as shown.
            {
                "product_id": self.lot_product.id,
                "lot_name": "LOT-BRAND-NEW",
                "counted_qty": 2,
                "theoretical_qty": 0,
            },
        ]
        result = self.Inventory.action_barcode_apply_count(self.location.id, lines)
        self.assertFalse(result["done"])
        self.assertEqual(
            result["changed"],
            [
                {
                    "product_id": self.product.id,
                    "product_name": self.product.display_name,
                    "lot_name": "",
                    "shown": 10.0,
                    "now": 15.0,
                    "uom": self.product.uom_id.name,
                }
            ],
        )
        # Nothing applied, nothing created.
        self.assertEqual(self._qty(self.product), 15)
        self.assertFalse(
            self.Inventory.search([("location_ids", "=", self.location.id)])
        )
        self.assertFalse(self.env["stock.lot"].search([("name", "=", "LOT-BRAND-NEW")]))
        # The operator applies it all the same.
        result = self.Inventory.action_barcode_apply_count(
            self.location.id, lines, force=True
        )
        self.assertTrue(result["done"])
        self.assertEqual(self._qty(self.product), 8)

    def test_stock_as_shown_is_applied(self):
        self.Quant._update_available_quantity(self.new_product, self.location, -3)
        result = self.Inventory.action_barcode_apply_count(
            self.location.id,
            [
                {
                    "product_id": self.new_product.id,
                    "counted_qty": 0,
                    "theoretical_qty": -3,
                }
            ],
        )
        self.assertTrue(result["done"])
        self.assertEqual(self._qty(self.new_product), 0)
        # A product gone since is left to the checks, which refuse it.
        with self.assertRaises(UserError):
            self.Inventory.action_barcode_apply_count(
                self.location.id,
                [{"product_id": 0, "counted_qty": 1, "theoretical_qty": 0}],
            )

    def test_lot_names_suggested(self):
        other = self.env["res.company"].create({"name": "Barcode Lots Co"})
        self.env["stock.lot"].create(
            [
                {
                    "name": "LOT-ELSEWHERE",
                    "product_id": self.lot_product.id,
                    "company_id": other.id,
                },
                {
                    "name": "LOT-SHARED",
                    "product_id": self.lot_product.id,
                    "company_id": False,
                },
            ]
        )
        names = self.Inventory.action_barcode_lot_names(
            self.location.id, self.lot_product.id
        )
        # The lots a count here can use, as _barcode_resolve_lot finds them.
        self.assertIn("LOT-COUNT-1", names)
        self.assertIn("LOT-SHARED", names)
        self.assertNotIn("LOT-ELSEWHERE", names)
        self.assertEqual(
            self.Inventory.action_barcode_lot_names(self.location.id, 0), []
        )
        # Looked up as the operator types, a few at a time.
        lot_names = self.Inventory.action_barcode_lot_names
        self.assertEqual(
            lot_names(self.location.id, self.lot_product.id, "shared"), ["LOT-SHARED"]
        )
        self.assertEqual(
            len(lot_names(self.location.id, self.lot_product.id, "", limit=1)), 1
        )

    def test_apply_count_matching_the_stock(self):
        result = self.Inventory.action_barcode_apply_count(
            self.location.id, [{"product_id": self.product.id, "counted_qty": 10}]
        )
        self.assertEqual(self._qty(self.product), 10)
        # The count is recorded all the same, as the back office does.
        self.assertEqual(result["move_count"], 1)

    def test_apply_count_over_split_stock(self):
        self.Quant.sudo().create(
            {
                "product_id": self.product.id,
                "location_id": self.location.id,
                "quantity": 2,
            }
        )
        self.assertEqual(self._qty(self.product), 12)
        self.Inventory.action_barcode_apply_count(
            self.location.id, [{"product_id": self.product.id, "counted_qty": 5}]
        )
        self.assertEqual(self._qty(self.product), 5)

    def test_apply_count_in_a_shared_location(self):
        shared = self.env["stock.location"].create(
            {
                "name": "Barcode Count Shared",
                "usage": "internal",
                "location_id": self.env.ref("stock.stock_location_locations").id,
                "company_id": False,
            }
        )
        result = self.Inventory.action_barcode_apply_count(
            shared.id,
            [
                {
                    "product_id": self.lot_product.id,
                    "lot_name": "LOT-SHARED",
                    "counted_qty": 2,
                }
            ],
        )
        group = self.Inventory.browse(result["group_id"])
        self.assertEqual(group.company_id, self.env.company)
        lot = group.stock_move_ids.lot_id
        self.assertEqual(lot.name, "LOT-SHARED")
        self.assertEqual(lot.company_id, self.env.company)
        self.assertEqual(self._qty(self.lot_product, lot, location=shared), 2)
