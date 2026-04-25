# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
# pylint: disable=missing-return
from .common import CommonCase


class TestAssignPackageType(CommonCase):
    @classmethod
    def setUpClassBaseData(cls):
        super().setUpClassBaseData()
        cls.picking = cls._create_picking(
            lines=[(cls.product_a, 10), (cls.product_b, 10), (cls.product_c, 10)]
        )
        # Product A has one packaging of quantity 3
        cls.selected_move_line = cls.picking.move_line_ids.filtered(
            lambda li: li.product_id == cls.product_a
        )
        cls.package_type = cls.env.ref("stock.package_type_01")
        cls.product_a.packaging_ids.package_type_id = cls.package_type

    def test_process_with_new_pack__package_type_is_set(self):
        picking = self.picking
        self.service.dispatch("scan_document", params={"barcode": picking.name})
        response = self.service.dispatch(
            "process_with_new_pack",
            params={
                "picking_id": picking.id,
                "selected_line_id": self.selected_move_line.id,
                "quantity": 3.0,
            },
        )
        picking_data = self.data.picking(picking)
        line_data = self.data.move_lines(
            self.selected_move_line, with_package_type=True
        )
        self.assert_response(
            response,
            next_state="set_destination",
            data={
                "picking": picking_data,
                "selected_move_line": line_data,
            },
        )
        package = self.selected_move_line.result_package_id
        self.assertEqual(package.package_type_id, self.package_type)

    def test_process_with_new_pack__package_type_not_set(self):
        picking = self.picking
        self.service.dispatch("scan_document", params={"barcode": picking.name})
        response = self.service.dispatch(
            "process_with_new_pack",
            params={
                "picking_id": picking.id,
                "selected_line_id": self.selected_move_line.id,
                "quantity": 5.0,
            },
        )
        picking_data = self.data.picking(picking)
        line_data = self.data.move_lines(
            self.selected_move_line, with_package_type=True
        )
        self.assert_response(
            response,
            next_state="set_destination",
            data={
                "picking": picking_data,
                "selected_move_line": line_data,
            },
        )
        package = self.selected_move_line.result_package_id
        self.assertFalse(package.package_type_id)
