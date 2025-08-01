# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import TransactionCase


class TestOrderLinePackagingImport(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.currency = cls.env.ref("base.main_company").currency_id
        cls.pricelist_currency = cls.env["product.pricelist"].create(
            {"name": "Pricelist Currency", "currency_id": cls.currency.id}
        )
        cls.product = cls.env.ref("product.product_delivery_02")
        cls.pack1 = cls.env["product.packaging"].create(
            {
                "name": "Pack Number One",
                "barcode": "PACK001",
                "product_id": cls.product.id,
                "qty": 12,
            }
        )
        cls.pack2 = cls.env["product.packaging"].create(
            {
                "name": "Pack Number Two",
                "barcode": "PACK002",
                "product_id": cls.product.id,
                "qty": 3,
            }
        )
        cls.parsed_order = {
            "partner": {
                "email": "deco.addict82@example.com",
                "property_product_pricelist": cls.pricelist_currency,
            },
            "date": "2018-08-14",
            "order_ref": "TEST1234",
            "lines": [
                {
                    "product": {"barcode": "PACK001"},
                    "qty": 2,
                    "uom": {"unece_code": "C62"},
                }
            ],
            "chatter_msg": [],
            "doc_type": "rfq",
        }
        cls.soio = cls.env["sale.order.import"]

    def test_order_line_packaging_import(self):
        order = self.soio.create_order(self.parsed_order, "pricelist")
        line = order.order_line[0]
        self.assertEqual(line.product_packaging_id, self.pack1)
        self.assertEqual(line.product_packaging_qty, 2)
        self.assertEqual(line.product_uom_qty, 2 * 12)
        # Change the quantity
        self.parsed_order["lines"][0]["qty"] = 3
        self.soio.update_order_lines(self.parsed_order, order, "pricelist")
        self.assertEqual(line.product_uom_qty, 3 * 12)
        self.assertEqual(line.product_packaging_qty, 3)
        # Change the packaging and quantity
        self.parsed_order["lines"][0]["qty"] = 5
        self.parsed_order["lines"][0]["product"]["barcode"] = "PACK002"
        self.soio.update_order_lines(self.parsed_order, order, "pricelist")
        self.assertEqual(line.product_packaging_id, self.pack2)
        self.assertEqual(line.product_uom_qty, 5 * 3)
        self.assertEqual(line.product_packaging_qty, 5)
        # Remove the packaging
        self.parsed_order["lines"][0]["product"]["code"] = "FURN_8888"
        self.parsed_order["lines"][0]["product"]["barcode"] = ""
        self.soio.update_order_lines(self.parsed_order, order, "pricelist")
        self.assertFalse(line.product_packaging_id)
        self.assertEqual(line.product_uom_qty, 5)
        self.assertEqual(line.product_packaging_qty, False)
        # Add the packaging again
        self.parsed_order["lines"][0]["qty"] = 1
        self.parsed_order["lines"][0]["product"]["barcode"] = "PACK001"
        self.soio.update_order_lines(self.parsed_order, order, "pricelist")
        self.assertEqual(line.product_packaging_id, self.pack1)
        self.assertEqual(line.product_uom_qty, 1 * 12)
        self.assertEqual(line.product_packaging_qty, 1)
