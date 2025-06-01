# Copyright 2025 Foodles (https://www.foodles.co/).
# @author Pierre Verkest <pierreverkest84@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from collections import defaultdict

from odoo import fields
from odoo.tests import SavepointCase


class TestStockQuantHistoryCommon(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                test_queue_job_no_delay=True,  # no jobs thanks
            )
        )

        cls.stock_history_now = cls.env["stock.quant.history.snapshot"].create(
            {
                "inventory_date": fields.Datetime.now(),
            }
        )

        cls.stock_manager_user = cls.env["res.users"].create(
            {
                "name": "foo",
                "login": "stock_manager",
                "email": "foo@bar.com",
                "lang": "en_US",
                "groups_id": [
                    (
                        6,
                        0,
                        (
                            cls.env.ref("base.group_user")
                            | cls.env.ref("stock.group_stock_manager")
                        ).ids,
                    )
                ],
            }
        )
        cls.warehouse = cls.env.ref("stock.warehouse0")
        cls.location = cls.warehouse.lot_stock_id
        cls.product = cls.env["product.product"].create(
            {
                "name": "test",
                "type": "product",
                "tracking": "lot",
            }
        )
        cls.lot = cls.env["stock.production.lot"].create(
            {
                "name": "lot test",
                "product_id": cls.product.id,
                "company_id": cls.warehouse.company_id.id,
            }
        )
        cls.product_consu = cls.env["product.product"].create(
            {
                "name": "test",
                "type": "consu",
            }
        )

    def _update_product_stock(self, qty, lot=None, location=None, uom=None):
        if lot is None:
            lot = self.lot
        if not location:
            location = self.location
        if not uom:
            uom = self.product.uom_id
        inventory = self.env["stock.inventory"].create(
            {
                "name": "Test Inventory",
                "product_ids": [(6, 0, self.product.ids)],
                "state": "confirm",
                "line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_qty": qty,
                            "location_id": location.id,
                            "product_id": self.product.id,
                            "product_uom_id": uom.id,
                            "prod_lot_id": lot.id,
                        },
                    )
                ],
            }
        )
        inventory.action_validate()

    @classmethod
    def quants_quantity_group_by(cls, recordset, key):
        """inspired from sale_product_pack PR: gh:oca/product-pack/pull/159"""
        groups = defaultdict(lambda: 0)
        for elem in recordset:
            groups[key(elem)] += elem.quantity
        return groups

    def assertQuantCompare(self, quants, expected_quants):
        """works either with stock.quant or stock.quants.history"""

        def group_key(quant):
            return quant.product_id, quant.lot_id, quant.location_id

        grouped_quants = self.quants_quantity_group_by(quants, group_key)
        grouped_expected_quants = self.quants_quantity_group_by(
            expected_quants, group_key
        )
        errors1 = []
        errors2 = []
        ok = []
        for key, quantity in grouped_quants.items():
            if grouped_expected_quants[key] != quantity:
                errors1.append(
                    f"got {quantity} != Expected {grouped_expected_quants[key]} for"
                    f"{key}: [{key[0].name}, {key[1].name}, {key[2].name}], "
                )
            else:
                ok.append(
                    f"{grouped_expected_quants[key]} for "
                    f"{key}: [{key[0].name}, {key[1].name}, {key[2].name}], "
                    f"is the same {quantity} !"
                )

        for key, quantity in grouped_expected_quants.items():
            if grouped_quants[key] != quantity:
                errors2.append(
                    f"got {grouped_quants[key]} != Expected {quantity} for "
                    f"{key}: [{key[0].name}, {key[1].name}, {key[2].name}], "
                )
        self.assertEqual(
            len(errors1) + len(errors2),
            0,
            "Following diff detected:\n"
            "\n".join(errors1)
            + "\n or/and \n "
            + "\n".join(errors2)
            + "\n\nOK records:\n"
            + "\n".join(ok),
        )
