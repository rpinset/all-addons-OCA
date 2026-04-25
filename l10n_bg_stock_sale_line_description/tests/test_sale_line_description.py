# Copyright 2026 OCA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("-at_install", "post_install")
class TestSaleLineDescription(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Test partner"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "uom_po_id": cls.env.ref("uom.product_uom_unit").id,
                "list_price": 10.0,
                "type": "consu",
            }
        )
        cls.pricelist = cls.env["product.pricelist"].create(
            {"name": "Test Pricelist", "currency_id": cls.env.ref("base.EUR").id}
        )
        cls.loc_stock = cls.env.ref("stock.stock_location_stock")
        cls.loc_customer = cls.env.ref("stock.stock_location_customers")

    def test_sale_line_description_related(self):
        order = self.env["sale.order"].create(
            {"partner_id": self.partner.id, "pricelist_id": self.pricelist.id}
        )
        line = self.env["sale.order.line"].create(
            {
                "order_id": order.id,
                "product_id": self.product.id,
                "name": "Custom description",
                "product_uom_qty": 1.0,
                "price_unit": 10.0,
            }
        )

        move = self.env["stock.move"].create(
            {
                "name": "Move with sale desc",
                "product_id": self.product.id,
                "product_uom": self.product.uom_id.id,
                "product_uom_qty": 1.0,
                "location_id": self.loc_stock.id,
                "location_dest_id": self.loc_customer.id,
                "sale_line_id": line.id,
            }
        )

        self.assertEqual(move.sale_line_description, "Custom description")
