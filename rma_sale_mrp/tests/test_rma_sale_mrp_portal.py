# Copyright 2026 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import HttpCase, new_test_user, tagged

from .test_rma_sale_mrp import TestRmaSaleMrpBase


@tagged("-at_install", "post_install")
class TestRmaSaleMrpPortal(TestRmaSaleMrpBase, HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale_order = cls._create_sale_order([[cls.product_kit, 5]])
        cls.sale_order.action_confirm()
        cls.sale_order.name = "Test Sale Mrp RMA SO"
        cls.order_out_picking = cls.sale_order.picking_ids
        for move in cls.order_out_picking.move_ids:
            move.quantity = move.product_uom_qty
        cls.order_out_picking.button_validate()
        # Let's create some companion contacts
        cls.partner_company = cls.res_partner.create(
            {"name": "Partner test Co", "email": "partner_co@test.com"}
        )
        cls.another_partner = cls.res_partner.create(
            {
                "name": "Another address",
                "email": "another_partner@test.com",
                "parent_id": cls.partner_company.id,
            }
        )
        cls.partner.parent_id = cls.partner_company
        # Create our portal user
        new_test_user(
            cls.env,
            login="rma_portal",
            partner_id=cls.partner.id,
            groups="base.group_portal",
        )

    def test_rma_sale_mrp_portal(self):
        self.start_tour("/", "rma_sale_mrp_portal", login="rma_portal")
        # Check that the portal values are properly transmited
        self.assertEqual(len(self.sale_order.rma_ids), 2)
        rmas = self.sale_order.rma_ids
        self.assertIn(self.product_kit_comp_1, rmas.mapped("product_id"))
        rma_1 = rmas.filtered(lambda x: x.product_id == self.product_kit_comp_1)
        self.assertEqual(rma_1.state, "draft")
        self.assertEqual(rma_1.partner_id, self.partner)
        self.assertEqual(rma_1.product_uom_qty, 10)
        self.assertIn(self.product_kit_comp_2, rmas.mapped("product_id"))
        rma_2 = rmas.filtered(lambda x: x.product_id == self.product_kit_comp_2)
        self.assertEqual(rma_2.state, "draft")
        self.assertEqual(rma_2.partner_id, self.partner)
        self.assertEqual(rma_2.product_uom_qty, 20)
