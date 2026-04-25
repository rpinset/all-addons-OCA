# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.addons.shopfloor_reception.tests.common import CommonCase


# pylint: disable=W8110
class TestSetPackDimension(CommonCase):
    @classmethod
    def setUpClassBaseData(cls):
        super().setUpClassBaseData()
        cls.input_location.sudo().active = True
        cls.picking = cls._create_picking(
            lines=[(cls.product_a, 10), (cls.product_b, 10), (cls.product_c, 10)]
        )
        cls.move_line = cls.picking.move_line_ids.filtered(
            lambda li: li.product_id == cls.product_a
        )

    def test_scan_location_ok_and_change_height(self):
        location = self.move_line.move_id.location_dest_id
        package = self.picking._put_in_pack(self.move_line)
        response = self.service.dispatch(
            "set_destination",
            params={
                "picking_id": self.picking.id,
                "selected_line_id": self.move_line.id,
                "location_name": location.barcode,
                "height": 4,
            },
        )
        self.assertEqual(package.height, 4)
        self.assert_response(
            response,
            next_state="select_move",
            data=self._data_for_select_move(
                self.picking, last_processed_line=self.move_line
            ),
        )

    def test_scan_location_not_ok_and_change_height(self):
        package = self.picking._put_in_pack(self.move_line)
        response = self.service.dispatch(
            "set_destination",
            params={
                "picking_id": self.picking.id,
                "selected_line_id": self.move_line.id,
                "location_name": "BURP",
                "height": 5,
            },
        )
        self.assertEqual(package.height, 5)
        self.assert_response(
            response,
            next_state="set_destination",
            data={
                "picking": self.data.picking(self.picking),
                "selected_move_line": self.data.move_lines(
                    self.move_line, with_package_type=True
                ),
            },
            message={
                "message_type": "error",
                "body": "No location found for this barcode.",
            },
        )
