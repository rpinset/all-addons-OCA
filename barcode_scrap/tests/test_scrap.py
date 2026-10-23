# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestBarcodeScrap(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Scrap = cls.env["stock.scrap"]
        cls.company = cls.env.company
        cls.location = cls.env["stock.location"].create(
            {
                "name": "Barcode Scrap Shelf",
                "usage": "internal",
                "location_id": cls.env.ref("stock.stock_location_stock").id,
                "company_id": cls.company.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {"name": "Scrap Untracked", "is_storable": True}
        )
        cls.lot_product = cls.env["product.product"].create(
            {"name": "Scrap Lot", "is_storable": True, "tracking": "lot"}
        )
        cls.serial_product = cls.env["product.product"].create(
            {"name": "Scrap Serial", "is_storable": True, "tracking": "serial"}
        )
        cls.lot = cls.env["stock.lot"].create(
            {
                "name": "LOT-SCRAP-1",
                "product_id": cls.lot_product.id,
                "company_id": cls.company.id,
            }
        )
        cls.serial = cls.env["stock.lot"].create(
            {
                "name": "SN-SCRAP-1",
                "product_id": cls.serial_product.id,
                "company_id": cls.company.id,
            }
        )
        Quant = cls.env["stock.quant"]
        Quant._update_available_quantity(cls.product, cls.location, 10)
        Quant._update_available_quantity(
            cls.lot_product, cls.location, 5, lot_id=cls.lot
        )
        Quant._update_available_quantity(
            cls.serial_product, cls.location, 1, lot_id=cls.serial
        )
        cls.reason = cls.env["stock.scrap.reason.tag"].create({"name": "Damaged"})

    def _qty(self, product, lot=None):
        return product.with_context(
            location=self.location.id, lot_id=lot.id if lot else False, strict=True
        ).qty_available

    def test_location_stock(self):
        data = self.Scrap.action_barcode_scrap_location_stock(self.location.id)
        self.assertEqual(data["location_id"], self.location.id)
        by_product = {(s["product_id"], s["lot_id"]): s for s in data["stock"]}
        self.assertEqual(by_product[(self.product.id, False)]["quantity"], 10)
        lot_entry = by_product[(self.lot_product.id, self.lot.id)]
        self.assertEqual(lot_entry["lot_name"], "LOT-SCRAP-1")
        self.assertEqual(lot_entry["quantity"], 5)

    def test_location_stock_is_what_a_scrap_can_take(self):
        # The same lot spread over several quants: loose ones (one of them
        # negative), one in a package, one owned by a partner.
        Quant = self.env["stock.quant"].sudo()
        for quantity in (2, -1):
            Quant.create(
                {
                    "product_id": self.lot_product.id,
                    "location_id": self.location.id,
                    "lot_id": self.lot.id,
                    "quantity": quantity,
                }
            )
        package = self.env["stock.quant.package"].create({"name": "SCRAP-PACK"})
        owner = self.env["res.partner"].create({"name": "Scrap Owner"})
        Quant._update_available_quantity(
            self.lot_product, self.location, 4, lot_id=self.lot, package_id=package
        )
        Quant._update_available_quantity(
            self.lot_product, self.location, 3, lot_id=self.lot, owner_id=owner
        )
        data = self.Scrap.action_barcode_scrap_location_stock(self.location.id)
        lots = [s for s in data["stock"] if s["product_id"] == self.lot_product.id]
        # One entry for the lot, with the net quantity outside packages and
        # owners: 5 + 2 - 1. Exactly what validating a scrap counts.
        self.assertEqual(len(lots), 1)
        self.assertEqual(lots[0]["quantity"], 6)
        vals = {
            "product_id": self.lot_product.id,
            "product_uom_id": self.lot_product.uom_id.id,
            "lot_id": self.lot.id,
            "location_id": self.location.id,
        }
        self.assertTrue(self.Scrap.new(dict(vals, scrap_qty=6)).check_available_qty())
        self.assertFalse(self.Scrap.new(dict(vals, scrap_qty=7)).check_available_qty())
        result = self.Scrap.action_barcode_scrap(
            self.location.id,
            [{"product_id": self.lot_product.id, "lot_id": self.lot.id, "qty": 7}],
        )
        self.assertEqual(result["insufficient"][0]["available"], 6)

    def test_invalid_location(self):
        view = self.env["stock.location"].create(
            {"name": "Barcode Scrap View", "usage": "view"}
        )
        with self.assertRaises(UserError):
            self.Scrap.action_barcode_scrap_location_stock(view.id)
        with self.assertRaises(UserError):
            self.Scrap.action_barcode_scrap(0, [{"product_id": self.product.id}])

    def test_scrap_done_with_reasons(self):
        result = self.Scrap.action_barcode_scrap(
            self.location.id,
            [
                {"product_id": self.product.id, "qty": 3},
                {"product_id": self.lot_product.id, "lot_id": self.lot.id, "qty": 2},
            ],
            [self.reason.id],
        )
        self.assertTrue(result["done"])
        self.assertEqual(result["count"], 2)
        scraps = self.Scrap.search([("name", "in", result["names"])])
        self.assertEqual(set(scraps.mapped("state")), {"done"})
        self.assertEqual(scraps.scrap_reason_tag_ids, self.reason)
        self.assertEqual(self._qty(self.product), 7)
        self.assertEqual(self._qty(self.lot_product, self.lot), 3)

    def test_lot_by_name_and_merge(self):
        # Two lines of the same lot, one by id and one by a GS1 lot name in a
        # different case, become a single scrap of the whole quantity.
        result = self.Scrap.action_barcode_scrap(
            self.location.id,
            [
                {"product_id": self.lot_product.id, "lot_id": self.lot.id, "qty": 1},
                {
                    "product_id": self.lot_product.id,
                    "lot_name": "lot-scrap-1",
                    "qty": 2,
                },
            ],
        )
        self.assertEqual(result["count"], 1)
        self.assertEqual(self._qty(self.lot_product, self.lot), 2)

    def test_lot_name_is_matched_exactly_first(self):
        Lot = self.env["stock.lot"]

        def lot(name):
            return Lot.create(
                {
                    "name": name,
                    "product_id": self.lot_product.id,
                    "company_id": self.company.id,
                }
            )

        def resolve(name):
            return self.Scrap._barcode_scrap_resolve_lot(
                self.lot_product, {"lot_name": name}, self.location
            )

        # GS1 allows "_" and "%" in a lot: they are no wildcards here.
        underscore, lookalike = lot("LOT_1"), lot("LOTA1")
        self.assertEqual(resolve("LOT_1"), underscore)
        self.assertEqual(resolve("LOTA1"), lookalike)
        with self.assertRaises(UserError):
            resolve("LOT%")
        # Lots that differ only in case are distinct lots.
        upper, lower = lot("ABC"), lot("abc")
        self.assertEqual(resolve("ABC"), upper)
        self.assertEqual(resolve("abc"), lower)
        # Another case finds the one lot it names, and refuses to pick among two.
        self.assertEqual(resolve("lot_1"), underscore)
        with self.assertRaises(UserError):
            resolve("Abc")

    def test_only_goods_are_scrapped(self):
        service = self.env["product.product"].create(
            {"name": "Scrap Service", "type": "service"}
        )
        with self.assertRaises(UserError):
            self.Scrap.action_barcode_scrap(
                self.location.id,
                [{"product_id": service.id, "qty": 1}],
                force=True,
            )
        self.assertFalse(self.Scrap.search([("product_id", "=", service.id)]))

    def test_insufficient_asks_then_forces(self):
        lines = [{"product_id": self.product.id, "qty": 12}]
        result = self.Scrap.action_barcode_scrap(self.location.id, lines)
        self.assertFalse(result["done"])
        self.assertEqual(len(result["insufficient"]), 1)
        short = result["insufficient"][0]
        self.assertEqual(short["requested"], 12)
        self.assertEqual(short["available"], 10)
        self.assertFalse(self.Scrap.search([("product_id", "=", self.product.id)]))

        result = self.Scrap.action_barcode_scrap(self.location.id, lines, force=True)
        self.assertTrue(result["done"])
        self.assertEqual(self._qty(self.product), -2)

    def test_merged_lines_checked_together(self):
        # Each line alone fits the stock, together they do not: the operator is
        # asked instead of the second one being scrapped silently.
        result = self.Scrap.action_barcode_scrap(
            self.location.id,
            [
                {"product_id": self.product.id, "qty": 6},
                {"product_id": self.product.id, "qty": 6},
            ],
        )
        self.assertFalse(result["done"])
        self.assertEqual(result["insufficient"][0]["requested"], 12)

    def test_stock_changed_meanwhile(self):
        with patch.object(
            type(self.Scrap), "action_validate", return_value={"type": "wizard"}
        ):
            with self.assertRaises(UserError):
                self.Scrap.action_barcode_scrap(
                    self.location.id, [{"product_id": self.product.id, "qty": 1}]
                )

    def test_line_validation(self):
        cases = [
            [],
            [{"product_id": 0, "qty": 1}],
            [{"product_id": self.product.id, "qty": 0}],
            [{"product_id": self.lot_product.id, "qty": 1}],
            [{"product_id": self.lot_product.id, "lot_name": "NOPE", "qty": 1}],
            [{"product_id": self.lot_product.id, "lot_id": self.serial.id, "qty": 1}],
            [
                {
                    "product_id": self.serial_product.id,
                    "lot_id": self.serial.id,
                    "qty": 2,
                }
            ],
            [
                {
                    "product_id": self.serial_product.id,
                    "lot_id": self.serial.id,
                    "qty": 1,
                },
                {
                    "product_id": self.serial_product.id,
                    "lot_name": "SN-SCRAP-1",
                    "qty": 1,
                },
            ],
        ]
        for lines in cases:
            with self.subTest(lines=lines), self.assertRaises(UserError):
                self.Scrap.action_barcode_scrap(self.location.id, lines)

    def test_serial_scrap(self):
        result = self.Scrap.action_barcode_scrap(
            self.location.id,
            [
                {
                    "product_id": self.serial_product.id,
                    "lot_name": "SN-SCRAP-1",
                    "qty": 1,
                }
            ],
        )
        self.assertTrue(result["done"])
        self.assertEqual(self._qty(self.serial_product, self.serial), 0)

    def test_destination_default_and_choices(self):
        data = self.Scrap.action_barcode_scrap_location_stock(self.location.id)
        default = self.env["stock.location"].browse(data["scrap_location_id"])
        self.assertTrue(default.scrap_location)
        choices = self.env["stock.location"].browse(
            [loc["id"] for loc in data["scrap_locations"]]
        )
        self.assertIn(default, choices)
        self.assertTrue(all(choices.mapped("scrap_location")))

        result = self.Scrap.action_barcode_scrap(
            self.location.id, [{"product_id": self.product.id, "qty": 1}]
        )
        scrap = self.Scrap.search([("name", "in", result["names"])])
        self.assertEqual(scrap.scrap_location_id, default)

    def test_destination_chosen(self):
        other = self.env["stock.location"].create(
            {
                "name": "Barcode Scrap Bin",
                "usage": "inventory",
                "scrap_location": True,
                "company_id": self.company.id,
            }
        )
        data = self.Scrap.action_barcode_scrap_location_stock(self.location.id)
        self.assertIn(other.id, [loc["id"] for loc in data["scrap_locations"]])
        result = self.Scrap.action_barcode_scrap(
            self.location.id,
            [{"product_id": self.product.id, "qty": 1}],
            scrap_location_id=other.id,
        )
        scrap = self.Scrap.search([("name", "in", result["names"])])
        self.assertEqual(scrap.scrap_location_id, other)

    def test_destination_when_the_company_has_none_of_its_own(self):
        company = self.env["res.company"].create({"name": "Scrap Shared Co"})
        Location = self.env["stock.location"]
        Location.search(
            [("company_id", "=", company.id), ("scrap_location", "=", True)]
        ).write({"scrap_location": False})
        Location.create(
            {
                "name": "Shared Scrap",
                "usage": "inventory",
                "scrap_location": True,
                "company_id": False,
            }
        )
        shelf = Location.create(
            {"name": "Shared Co Shelf", "usage": "internal", "company_id": company.id}
        )
        self.env["stock.quant"]._update_available_quantity(self.product, shelf, 3)
        # The back office would preselect nothing: the first shared one is taken.
        data = self.Scrap.action_barcode_scrap_location_stock(shelf.id)
        default = Location.browse(data["scrap_location_id"])
        self.assertTrue(default.scrap_location)
        self.assertFalse(default.company_id)
        result = self.Scrap.action_barcode_scrap(
            shelf.id, [{"product_id": self.product.id, "qty": 1}]
        )
        scrap = self.Scrap.search([("name", "in", result["names"])])
        self.assertEqual(scrap.scrap_location_id, default)

    def test_no_destination_at_all(self):
        with patch.object(
            type(self.Scrap),
            "_barcode_scrap_destinations",
            return_value=self.env["stock.location"],
        ):
            data = self.Scrap.action_barcode_scrap_location_stock(self.location.id)
            self.assertEqual(data["scrap_locations"], [])
            self.assertFalse(data["scrap_location_id"])
            with self.assertRaises(UserError):
                self.Scrap.action_barcode_scrap(
                    self.location.id, [{"product_id": self.product.id, "qty": 1}]
                )

    def test_destination_must_be_a_scrap_location(self):
        with self.assertRaises(UserError):
            self.Scrap.action_barcode_scrap(
                self.location.id,
                [{"product_id": self.product.id, "qty": 1}],
                scrap_location_id=self.location.id,
            )

    def test_create_reason(self):
        created = self.Scrap.action_barcode_scrap_create_reason("  Broken   box ")
        tag = self.env["stock.scrap.reason.tag"].browse(created["id"])
        self.assertEqual(tag.name, "Broken box")
        # Same name in another case: the existing reason, no duplicate.
        again = self.Scrap.action_barcode_scrap_create_reason("broken BOX")
        self.assertEqual(again["id"], tag.id)
        self.assertEqual(
            self.Scrap.action_barcode_scrap_create_reason("damaged")["id"],
            self.reason.id,
        )

    def test_create_reason_wildcards_stay_literal(self):
        wild = self.Scrap.action_barcode_scrap_create_reason("Dam%")
        self.assertNotEqual(wild["id"], self.reason.id)
        self.assertEqual(wild["name"], "Dam%")

    def test_create_reason_needs_a_name(self):
        with self.assertRaises(UserError):
            self.Scrap.action_barcode_scrap_create_reason("   ")

    def test_destination_filter_matches_back_office(self):
        # Offered: the company's scrap locations and the shared ones; never
        # another company's nor a location not flagged as scrap -- the Scrap
        # Location field's domain plus the company check Odoo adds to it.
        Location = self.env["stock.location"]
        shared = Location.create(
            {
                "name": "Barcode Shared Scrap",
                "usage": "inventory",
                "scrap_location": True,
            }
        )
        not_scrap = Location.create(
            {
                "name": "Barcode Not Scrap",
                "usage": "inventory",
                "company_id": self.company.id,
            }
        )
        other_company = self.env["res.company"].create({"name": "Barcode Scrap Co"})
        other = Location.search(
            [("scrap_location", "=", True), ("company_id", "=", other_company.id)]
        )
        self.assertTrue(other)
        data = self.Scrap.action_barcode_scrap_location_stock(self.location.id)
        offered = {loc["id"] for loc in data["scrap_locations"]}
        self.assertIn(shared.id, offered)
        self.assertNotIn(not_scrap.id, offered)
        self.assertFalse(offered & set(other.ids))
        with self.assertRaises(UserError):
            self.Scrap.action_barcode_scrap(
                self.location.id,
                [{"product_id": self.product.id, "qty": 1}],
                scrap_location_id=other[:1].id,
            )
