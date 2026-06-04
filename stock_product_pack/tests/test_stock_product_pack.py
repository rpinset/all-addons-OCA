# Copyright 2019 Tecnativa - Ernesto Tejeda
# Copyright 2020 Tecnativa - João Marques
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo.tests import Form, TransactionCase, tagged

_logger = logging.getLogger(__name__)


@tagged("post_install", "-at_install")
class TestStockProductPack(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a product category for testing instead of relying on demo data
        category = cls.env["product.category"].create(
            {
                "name": "Test Category",
            }
        )
        category_all_id = category.id
        cls.product_obj = cls.env["product.product"]
        cls.stock_rule_obj = cls.env["stock.rule"]
        # The model stock doesn't add anymore the 'product'
        # selection to the product type.
        # Thus the type is changed to 'consu'
        component_1 = cls.product_obj.create(
            {
                "name": "Component 1",
                "type": "consu",
                "is_storable": True,
                "categ_id": category_all_id,
            }
        )
        component_2 = cls.product_obj.create(
            {
                "name": "Component 2",
                "type": "consu",
                "is_storable": True,
                "categ_id": category_all_id,
            }
        )
        component_3 = cls.product_obj.create(
            {
                "name": "Component 3",
                "type": "service",
                "categ_id": category_all_id,
            }
        )
        component_4 = cls.product_obj.create(
            {
                "name": "Component 4",
                "type": "consu",
                "is_storable": True,
                "categ_id": category_all_id,
            }
        )
        cls.pack_dc = cls.product_obj.create(
            {
                "name": "Pack",
                "type": "consu",
                "pack_ok": True,
                "pack_type": "detailed",
                "pack_component_price": "detailed",
                "categ_id": category_all_id,
                "pack_line_ids": [
                    (
                        0,
                        0,
                        {"product_id": component_1.id, "quantity": 1},
                    ),
                    (
                        0,
                        0,
                        {"product_id": component_2.id, "quantity": 1},
                    ),
                    (
                        0,
                        0,
                        {"product_id": component_3.id, "quantity": 1},
                    ),
                    (
                        0,
                        0,
                        {"product_id": component_4.id, "quantity": 1},
                    ),
                ],
            }
        )
        warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.env.user.id)], limit=1
        )
        cls.stock_rule = cls.stock_rule_obj.create(
            {
                "name": "Stock to Costumers",
                "action": "pull",
                "picking_type_id": cls.env.ref("stock.picking_type_internal").id,
                "route_id": cls.env.ref("stock.route_warehouse0_mto").id,
                "procure_method": "make_to_stock",
                "warehouse_id": warehouse.id,
                "location_dest_id": cls.env.ref("stock.stock_location_stock").id,
            }
        )
        cls.pack_dc_with_dm = cls.product_obj.create(
            {
                "name": "Pack With storeable and not move product",
                "type": "consu",
                "pack_ok": True,
                "dont_create_move": True,
                "pack_type": "detailed",
                "pack_component_price": "detailed",
                "categ_id": category_all_id,
                "pack_line_ids": [
                    (
                        0,
                        0,
                        {"product_id": component_1.id, "quantity": 1},
                    ),
                    (
                        0,
                        0,
                        {"product_id": component_2.id, "quantity": 1},
                    ),
                    (
                        0,
                        0,
                        {"product_id": component_3.id, "quantity": 1},
                    ),
                    (
                        0,
                        0,
                        {"product_id": component_4.id, "quantity": 1},
                    ),
                ],
            }
        )

    def test_compute_quantities_dict(self):
        location_id = (self.env.ref("stock.stock_location_suppliers").id,)
        location_dest_id = (self.env.ref("stock.stock_location_stock").id,)
        components = self.pack_dc.pack_line_ids.mapped("product_id")
        partner = self.env["res.partner"].create({"name": "Test Partner"})

        picking = self.env["stock.picking"].create(
            {
                "partner_id": partner.id,
                "picking_type_id": self.env.ref("stock.picking_type_in").id,
                "location_id": location_id,
                "location_dest_id": location_dest_id,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": components[0].id,
                            "product_uom_qty": 5,
                            "location_id": location_id,
                            "location_dest_id": location_dest_id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": components[1].id,
                            "product_uom_qty": 7,
                            "location_id": location_id,
                            "location_dest_id": location_dest_id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "product_id": components[3].id,
                            "product_uom_qty": 9,
                            "location_id": location_id,
                            "location_dest_id": location_dest_id,
                        },
                    ),
                ],
            }
        )
        picking.action_confirm()
        self.assertEqual(self.pack_dc.virtual_available, 5)
        self.assertEqual(self.pack_dc.qty_available, 0)
        wizard_dict = picking.button_validate()
        if wizard_dict is not True:
            wizard = Form(
                self.env[(wizard_dict.get("res_model"))].with_context(
                    **wizard_dict["context"]
                )
            ).save()
            wizard.process()
        self.assertEqual(self.pack_dc.virtual_available, 5)
        self.assertEqual(self.pack_dc.qty_available, 5)

    def test_pack_with_dont_move_the_parent(self):
        """Run a procurement for prod pack products when there are only 5 in stock then
        check that MTO is applied on the moves when the rule is set to 'mts_else_mto'
        """

        def create_orderpoint(product, qty_min, qty_max, location):
            return self.env["stock.warehouse.orderpoint"].create(
                {
                    "name": f"OP/{product.name}",
                    "product_id": product.id,
                    "product_min_qty": qty_min,
                    "product_max_qty": qty_max,
                    "location_id": location.id,
                }
            )

        create_orderpoint(
            self.pack_dc_with_dm,
            10,
            155,
            self.env.ref("stock.stock_location_stock"),
        )
        # Check that no moves were created for the pack product itself
        # Only components should have moves created
        pack_moves = self.env["stock.move"].search(
            [("product_id", "=", self.pack_dc_with_dm.id)]
        )
        self.assertFalse(pack_moves)
