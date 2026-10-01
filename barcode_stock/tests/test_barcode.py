# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase, new_test_user


class TestBarcodeScannerEAN13(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.nomenclature = cls.env["barcode.nomenclature"].create(
            {
                "name": "Test EAN13 Nomenclature",
            }
        )
        cls.rule = cls.env["barcode.rule"].create(
            {
                "name": "EAN13",
                "barcode_nomenclature_id": cls.nomenclature.id,
                "type": "alias",
                "encoding": "ean13",
                "pattern": ".............",
                "alias": "product.product",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test EAN13 Product",
                "is_storable": True,
                "barcode": "5901234123457",
            }
        )

    def test_ean13_decode_returns_product(self):
        result = (
            self.env["barcode.nomenclature"]
            .search([("id", "=", self.nomenclature.id)])
            .parse_barcode("5901234123457")
        )
        self.assertTrue(result)
        self.assertEqual(result["code"], "product.product")

    def test_ean13_resolve_product(self):
        product = self.env["product.product"].search(
            [("barcode", "=", "5901234123457")]
        )
        self.assertTrue(product)
        self.assertEqual(product.id, self.product.id)

    def test_ean13_invalid_barcode_returns_no_result(self):
        product = self.env["product.product"].search(
            [("barcode", "=", "0000000000000")]
        )
        self.assertFalse(product)

    def test_ean13_barcode_checksum_validation(self):
        barcode = "5901234123457"
        digits = [int(d) for d in barcode[:-1]]
        check = int(barcode[-1])
        total = sum(d * 3 if i % 2 == 0 else d for i, d in enumerate(digits))
        expected_check = (10 - (total % 10)) % 10
        self.assertEqual(check, expected_check)

    def test_parse_barcode_scanner_barcode(self):
        result = self.env["barcode.nomenclature"].parse_barcode_scanner_barcode(
            "5901234123457"
        )
        self.assertEqual(result["type"], "ean")
        self.assertIn("product", result)
        self.assertIn("qty", result)

    def test_parse_barcode_scanner_barcode_uses_company_nomenclature(self):
        # A company running its own nomenclature must decode through it, not
        # through the default one: the alias rule below turns the barcode into
        # "product.product", which the default nomenclature never yields.
        self.env.company.nomenclature_id = self.nomenclature
        result = self.env["barcode.nomenclature"].parse_barcode_scanner_barcode(
            "5901234123457"
        )
        self.assertEqual(result["product"], "product.product")


class TestBarcodeScannerStockUserAccess(TransactionCase):
    """A warehouse operator holds stock rights and nothing else.

    The scanner preloads its data as that user, so everything it asks the
    server for has to stay within those rights.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stock_user = new_test_user(
            cls.env,
            login="barcode_stock_operator",
            groups="stock.group_stock_user",
        )

    def test_stock_user_can_probe_lot_expiry_fields(self):
        # How the scanner finds out whether expiry dates are available: it asks
        # stock.lot for the fields it is about to use. Reading ir.module.module
        # instead only works where an optional addon happens to grant it, and
        # leaves the operator with an access error where it does not.
        as_operator = (
            self.env["stock.lot"]
            .with_user(self.stock_user)
            .fields_get(["expiration_date", "removal_date"], ["type"])
        )
        as_admin = self.env["stock.lot"].fields_get(
            ["expiration_date", "removal_date"], ["type"]
        )
        self.assertEqual(sorted(as_operator), sorted(as_admin))
