# Copyright 2026 OCA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("-at_install", "post_install")
class TestTaricAssignment(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.template"].create(
            {
                "name": "TARIC Test Product",
                "uom_id": cls.env.ref("uom.product_uom_unit").id,
                "uom_po_id": cls.env.ref("uom.product_uom_unit").id,
                "list_price": 5.0,
                "type": "consu",
            }
        )

    def test_write_sets_history_and_hs_code(self):
        taric_code = self.env["taric.code"].create(
            {"code": "1234567890", "description": "Test TARIC"}
        )

        self.product.write({"taric_code_id": taric_code.id})

        # hs_code should mirror the TARIC code
        self.assertEqual(self.product.hs_code, taric_code.code)

        # classification method and history should be recorded
        self.assertEqual(self.product.classification_method, "manual")
        history = self.env["taric.classification.history"].search(
            [
                ("product_id", "=", self.product.id),
                ("taric_code_id", "=", taric_code.id),
            ]
        )
        self.assertTrue(history, "Classification history should be created")
