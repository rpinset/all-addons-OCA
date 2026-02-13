# Copyright 2024 Antoni Marroig(APSL-Nagarro)<amarroig@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class RMARepairOrderTest(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.warehouse_company = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.env.company.id)], limit=1
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test product",
                "is_storable": True,
                "tracking": "lot",
            }
        )
        cls.rma_loc = cls.warehouse_company.rma_loc_id
        cls.res_partner = cls.env["res.partner"].create({"name": "Test"})
        cls.operation = cls.env.ref("rma.rma_operation_return")
        cls.lot = cls.env["stock.lot"].create({"product_id": cls.product.id})
        cls.rma = cls.env["rma"].create(
            {
                "product_id": cls.product.id,
                "product_uom_qty": 2,
                "location_id": cls.rma_loc.id,
                "partner_id": cls.res_partner.id,
                "operation_id": cls.operation.id,
                "lot_id": cls.lot.id,
            }
        )

    def test_repair_order_default_vals(self):
        vals = self.rma._get_repair_order_default_vals()
        self.assertEqual(vals["default_lot_id"], self.lot.id)
