# Copyright 2024 Binhex Rolando Pérez <r.perez@binhex.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleMrpBomCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env.ref("base.res_partner_2")
        cls.warehouse = cls.env.ref("stock.warehouse0")
        route_manufacture = cls.warehouse.manufacture_pull_id.route_id.id
        route_mto = cls.warehouse.mto_pull_id.route_id.id
        cls.product_a = cls.create_product(
            "Product A", route_ids=[(6, 0, [route_manufacture, route_mto])]
        )
        cls.product_b = cls.create_product(
            "Product B", route_ids=[(6, 0, [route_manufacture, route_mto])]
        )
        cls.component_a = cls.create_product("Component A", route_ids=[])
        cls.component_b = cls.create_product("Component B", route_ids=[])
        cls.product_attr_color = cls.env["product.attribute"].create({"name": "Color"})
        cls.product_attr_val_red, cls.product_attr_val_green = cls.env[
            "product.attribute.value"
        ].create(
            [
                {
                    "name": "red",
                    "attribute_id": cls.product_attr_color.id,
                    "sequence": 1,
                },
                {
                    "name": "blue",
                    "attribute_id": cls.product_attr_color.id,
                    "sequence": 2,
                },
            ]
        )

    @classmethod
    def create_product(cls, name, route_ids):
        return cls.env["product.product"].create(
            {"name": name, "type": "product", "route_ids": route_ids}
        )

    @classmethod
    def create_sale_order(cls, client_ref):
        return cls.env["sale.order"].create(
            {"partner_id": cls.partner.id, "client_order_ref": client_ref}
        )

    @classmethod
    def create_bom(cls, template):
        return cls.env["mrp.bom"].create(
            {"product_tmpl_id": template.id, "type": "normal"}
        )

    @classmethod
    def create_bom_line(cls, bom, product, qty):
        cls.env["mrp.bom.line"].create(
            {"bom_id": bom.id, "product_id": product.id, "product_qty": qty}
        )

    @classmethod
    def create_sale_order_line(cls, sale_order, product, qty, price, bom):
        cls.env["sale.order.line"].create(
            {
                "order_id": sale_order.id,
                "product_id": product.id,
                "price_unit": price,
                "product_uom_qty": qty,
                "bom_id": bom.id,
            }
        )
