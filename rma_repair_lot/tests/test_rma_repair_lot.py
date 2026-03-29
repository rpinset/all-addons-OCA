# Copyright 2024 Antoni Marroig(APSL-Nagarro)<amarroig@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.rma.tests.test_rma import TestRma


class RMARepairOrderTest(TestRma):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product.tracking = "lot"
        cls.operation = cls.operation_return
        cls.rma = cls._create_rma(
            cls.partner, cls.product, 2, cls.rma_loc, cls.operation_return
        )
        cls.lot = cls.env["stock.lot"].create({"product_id": cls.product.id})
        cls.rma.lot_id = cls.lot

    def test_repair_order_default_vals(self):
        vals = self.rma._get_repair_order_default_vals()
        self.assertEqual(vals["default_lot_id"], self.lot.id)
