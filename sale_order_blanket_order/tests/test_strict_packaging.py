# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import freezegun

from odoo import Command
from odoo.exceptions import ValidationError

from .common import SaleOrderBlanketOrderCase


class TestStrictPackaging(SaleOrderBlanketOrderCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.blanket_line_product_2 = cls.blanket_so.order_line.filtered(
            lambda line: line.product_id == cls.product_2
        )
        cls.blanket_line_product_2.product_packaging_id = cls.product_2_pack2
        cls.blanket_line_product_2.flush_recordset()
        cls.blanket_so.blanket_strict_packaging = True
        cls.blanket_so.action_confirm()
        cls._set_call_off_auto_create_mode(True)

    @freezegun.freeze_time("2025-02-01")
    def test_call_off_non_multiple_of_packaging(self):
        with self.assertRaisesRegex(
            ValidationError, "The product is not part of linked"
        ), self.env.cr.savepoint():
            call_off_so = self.env["sale.order"].create(
                {
                    "order_type": "call_off",
                    "partner_id": self.partner.id,
                    "blanket_order_id": self.blanket_so.id,
                    "order_line": [
                        Command.create(
                            {
                                "product_id": self.product_2.id,
                                "product_uom_qty": 3,
                            }
                        )
                    ],
                }
            )
            call_off_so.action_confirm()

        call_off_so = self.env["sale.order"].create(
            {
                "order_type": "call_off",
                "partner_id": self.partner.id,
                "blanket_order_id": self.blanket_so.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product_2.id,
                            "product_uom_qty": 4,
                        }
                    )
                ],
            }
        )
        call_off_so.action_confirm()
        self.assertEqual(
            call_off_so.order_line.product_packaging_id, self.product_2_pack2
        )

    @freezegun.freeze_time("2025-02-01")
    def test_call_off_wrong_packaging(self):
        with self.assertRaisesRegex(
            ValidationError, "The product is not part of linked"
        ):
            call_off_so = self.env["sale.order"].create(
                {
                    "order_type": "call_off",
                    "partner_id": self.partner.id,
                    "blanket_order_id": self.blanket_so.id,
                    "order_line": [
                        Command.create(
                            {
                                "product_id": self.product_2.id,
                                "product_uom_qty": 2,
                                "product_packaging_id": self.product_2_pack3.id,
                            }
                        )
                    ],
                }
            )
            call_off_so.action_confirm()
