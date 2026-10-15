# Copyright 2025 Camptocamp SA (https://www.camptocamp.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields

from odoo.addons.shopfloor.tests.test_location_content_transfer_base import (
    LocationContentTransferCommonCase,
)

# pylint: disable=missing-return


class TestLocationContentTransfer(LocationContentTransferCommonCase):
    @classmethod
    def setUpClassBaseData(cls, *args, **kwargs):
        super().setUpClassBaseData(*args, **kwargs)
        cls.test_loc = (
            cls.env["stock.location"]
            .sudo()
            .create(
                {
                    "location_id": cls.stock_location.id,
                    "name": "test",
                    "barcode": "test_loc",
                }
            )
        )
        cls.product_a.sudo().write({"tracking": "lot", "use_expiration_date": True})
        cls.expired_lot = (
            cls.env["stock.lot"]
            .sudo()
            .create(
                {
                    "name": "EXPIRED_LOT",
                    "product_id": cls.product_a.id,
                    "expiration_date": fields.Datetime.subtract(
                        fields.Datetime.now(), days=10
                    ),
                }
            )
        )
        cls._update_qty_in_location(
            cls.test_loc, cls.product_a, 10, lot=cls.expired_lot
        )
        cls.menu.sudo().allow_move_create = True

    def _get_moves_from_test_loc(self):
        return self.env["stock.move"].search(
            [
                ("location_id", "=", self.test_loc.id),
                ("product_id", "=", self.product_a.id),
            ]
        )

    def test_option_is_possible(self):
        self.assertTrue(self.menu.ignore_expiration_date_is_possible)
        other_menu = self.env.ref("shopfloor.shopfloor_menu_demo_zone_picking")
        self.assertFalse(other_menu.ignore_expiration_date_is_possible)

    def test_scan_location_expired_lot_not_reserved(self):
        self.menu.sudo().ignore_expiration_date = False
        response = self.service.dispatch(
            "scan_location", params={"barcode": self.test_loc.barcode}
        )
        self.assert_response_start(
            response, message=self.service.msg_store.new_move_lines_not_assigned()
        )
        self.assertFalse(self._get_moves_from_test_loc())

    def test_scan_location_expired_lot_reserved(self):
        self.menu.sudo().ignore_expiration_date = True
        response = self.service.dispatch(
            "scan_location", params={"barcode": self.test_loc.barcode}
        )
        self.assertNotEqual(response["next_state"], "scan_location")
        move = self._get_moves_from_test_loc()
        self.assertEqual(move.state, "assigned")
        self.assertEqual(move.move_line_ids.lot_id, self.expired_lot)
