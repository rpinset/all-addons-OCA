# Copyright 2021 Tecnativa - David Vidal
# Copyright 2025 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.addons.sale_product_pack.tests.common import TestSaleProductPackBase


class TestSaleStockProductPack(TestSaleProductPackBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pack.type = "consu"
        cls.pack.invoice_policy = "delivery"
        cls.pack.pack_line_ids.product_id.invoice_policy = "delivery"

    def test_delivered_quantities(self):
        pack_line = self._add_so_line()
        pack_line.product_uom_qty = 9
        self.sale = self.sale_order
        self.sale.action_confirm()
        self.assertEqual(0, pack_line.qty_delivered)
        # Process the picking
        for line in self.sale.picking_ids.move_ids.filtered(
            lambda x: x.product_id != self.pack
        ):
            line.quantity = line.product_uom_qty
        self.sale.picking_ids.move_ids.picked = True
        self.sale.picking_ids._action_done()
        # All components delivered, all the pack quantities should be so
        self.assertEqual(9, pack_line.qty_delivered)
