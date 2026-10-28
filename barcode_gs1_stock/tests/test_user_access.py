# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestBarcodeGs1StockUserAccess(HttpCase):
    """The app reads the units of measure as whoever opens it.

    The Scanner menu is open to every internal user, so a plain employee must be
    able to make the same calls ``gs1_stock_quantity.esm.js`` makes when the app
    starts, through the same RPC route.
    """

    def call_kw(self, model, method, args, kwargs=None):
        return self.make_jsonrpc_request(
            f"/web/dataset/call_kw/{model}/{method}",
            {"model": model, "method": method, "args": args, "kwargs": kwargs or {}},
        )

    def test_employee_reads_the_units_and_the_stored_decimals(self):
        new_test_user(
            self.env, login="barcode_gs1_stock_employee", groups="base.group_user"
        )
        self.authenticate("barcode_gs1_stock_employee", "barcode_gs1_stock_employee")
        uoms = self.call_kw(
            "uom.uom",
            "search_read",
            [[]],
            {"fields": ["name", "category_id", "factor", "rounding"]},
        )
        kilogram = self.env.ref("uom.product_uom_kgm")
        self.assertIn(
            kilogram.rounding,
            [uom["rounding"] for uom in uoms if uom["id"] == kilogram.id],
        )
        # The decimals come from a quantity field stored with them, not from
        # decimal.precision.precision_get: `account` overrides that method
        # without @api.model, which breaks it over RPC.
        fields = self.call_kw(
            "stock.move.line", "fields_get", [["quantity"]], {"attributes": ["digits"]}
        )
        self.assertEqual(
            fields["quantity"]["digits"][1],
            self.env["decimal.precision"].precision_get("Product Unit of Measure"),
        )
