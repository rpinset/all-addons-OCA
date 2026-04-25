# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from .common import CommonCase


# pylint: disable=W8110
class TestShopfloorReceptionChangeStorageType(CommonCase):
    @classmethod
    def setUpClassBaseData(cls):
        super().setUpClassBaseData()
        cls.picking = cls._create_picking(
            lines=[(cls.product_a, 10), (cls.product_b, 10)]
        )
        # Picking has 2 products
        # Product A with one packaging of quantity 3
        # Set a package type on product A packaging
        cls.package_type = cls.env.ref("stock.package_type_01")
        cls.package_type.sudo().barcode = "CAGE"
        cls.product_a.packaging_ids.package_type_id = cls.package_type
        # Product B with no packaging
        cls.product_b.packaging_ids = [(5, 0, 0)]

    def test_go_to_set_package_type_screen(self):
        picking = self.picking
        self.service.dispatch("scan_document", params={"barcode": picking.name})
        selected_move_line = picking.move_line_ids.filtered(
            lambda li: li.product_id == self.product_a
        )
        response = self.service.dispatch(
            "set_package_type",
            params={
                "picking_id": picking.id,
                "selected_line_id": selected_move_line.id,
            },
        )
        response["data"]["set_package_type"]["picking"].pop("progress")
        self.assert_response(
            response,
            next_state="set_package_type",
            data={
                "picking": self.data.picking(picking),
                "selected_move_line": self.data.move_lines(selected_move_line),
                "package_types": self.data.package_type_list(
                    self.service._get_package_type()
                ),
            },
        )

    def test_change_package_type_on_package(self):
        picking = self.picking
        self.service.dispatch("scan_document", params={"barcode": picking.name})
        selected_move_line = picking.move_line_ids.filtered(
            lambda li: li.product_id == self.product_a
        )
        selected_move_line.qty_picked = selected_move_line.quantity_product_uom
        response = self.service.dispatch(
            "select_dest_package",
            params={
                "picking_id": picking.id,
                "selected_line_id": selected_move_line.id,
                "barcode": "CAGE-0001",
                "confirmation": True,
            },
        )
        response = self.service.dispatch(
            "set_package_type",
            params={
                "picking_id": picking.id,
                "selected_line_id": selected_move_line.id,
                "barcode": "CAGE",
            },
        )
        self.assertEqual(response["next_state"], "set_destination")
        self.assertTrue(selected_move_line.result_package_id)
        self.assertEqual(
            selected_move_line.result_package_id.package_type_id, self.package_type
        )
