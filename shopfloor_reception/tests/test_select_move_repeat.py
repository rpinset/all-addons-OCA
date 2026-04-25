# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
# pylint: disable=missing-return

from .common import CommonCase


class TestSelectMoveRepeat(CommonCase):
    @classmethod
    def setUpClassBaseData(cls):
        super().setUpClassBaseData()
        cls.product_a.tracking = "lot"
        cls.location_dest = cls.env.ref("stock.stock_location_stock")

    def test_previous_processed_line_move_finished(self):
        """Check move done no possible repeat case."""
        picking = self._create_picking()
        working_line = picking.move_line_ids.filtered(
            lambda li: li.product_id == self.product_a
        )
        # Receiving the full quantity
        working_line.qty_picked = 10
        working_line.lot_id = self.env["stock.lot"].create(
            {"name": "Lot-001", "product_id": working_line.product_id.id}
        )
        working_line.result_package_id = self.env["stock.quant.package"].create({})
        working_line.location_dest_id = self.location_dest
        response = self.service.dispatch(
            "set_destination",
            params={
                "picking_id": picking.id,
                "selected_line_id": working_line.id,
                "location_name": self.shelf2.name,
            },
        )
        # The last_move_line is not return -> no Repeat button
        self.assert_response(
            response, next_state="select_move", data=self._data_for_select_move(picking)
        )

    def test_repeat_previous_reception_with_auto_post(self):
        """Check repeating an operation with the auto post option on."""
        self.menu.sudo().auto_post_line = True
        picking = self._create_picking()
        lot_name = "LOT-TEST-001"
        working_line = picking.move_line_ids.filtered(
            lambda li: li.product_id == self.product_a
        )
        working_move = working_line.move_id
        # Receive the first package
        working_line.location_dest_id = self.location_dest
        # Only processing half the move quantity with a package
        working_line.qty_picked = 5
        working_line.lot_id = self.env["stock.lot"].create(
            {"name": lot_name, "product_id": working_line.product_id.id}
        )
        working_line.result_package_id = self.env["stock.quant.package"].create({})
        response = self.service.dispatch(
            "set_destination",
            params={
                "picking_id": picking.id,
                "selected_line_id": working_line.id,
                "location_name": self.shelf2.name,
            },
        )
        self.assert_response(
            response,
            next_state="select_move",
            data=self._data_for_select_move(picking, last_processed_line=working_line),
        )
        # Lets repeat the previous reception
        response = self.service.dispatch(
            "scan_line_repeat",
            params={
                "picking_id": picking.id,
                "last_processed_line_id": working_line.id,
            },
        )
        new_move_line = self.env["stock.move.line"].search(
            [("move_id", "=", working_move.id)], order="id desc", limit=1
        )
        self.assertEqual(new_move_line.lot_id.name, lot_name)
        self.assert_response(
            response,
            next_state="set_quantity",
            data={
                "picking": self.data.picking(picking),
                "selected_move_line": self.data.move_lines(new_move_line),
                "confirmation_required": None,
            },
        )

    def test_repeat_previous_reception_standard(self):
        """Check repeating an operation without the auto post option."""
        picking = self._create_picking()
        selected_move_line = picking.move_line_ids.filtered(
            lambda li: li.product_id == self.product_b
        )
        selected_move_line.location_dest_id = self.location_dest
        self.service.dispatch(
            "set_quantity",
            params={
                "picking_id": picking.id,
                "selected_line_id": selected_move_line.id,
                # Only processing half the move quantity
                "quantity": 5,
            },
        )
        selected_move_line.result_package_id = self.env["stock.quant.package"].create(
            {}
        )
        response = self.service.dispatch(
            "set_destination",
            params={
                "picking_id": picking.id,
                "selected_line_id": selected_move_line.id,
                "location_name": self.shelf2.name,
            },
        )
        self.assert_response(
            response,
            next_state="select_move",
            data=self._data_for_select_move(
                picking, last_processed_line=selected_move_line
            ),
        )
        # Lets repeat...
        response = self.service.dispatch(
            "scan_line_repeat",
            params={
                "picking_id": picking.id,
                "last_processed_line_id": selected_move_line.id,
            },
        )
        self.env.invalidate_all()
        new_move_line = self.env["stock.move.line"].search(
            [("move_id", "=", selected_move_line.move_id.id)], order="id desc", limit=1
        )
        # FIXME
        new_move_line.quantity = 5
        data_line = self.data.move_lines(new_move_line)
        picking._compute_picking_info()
        data_picking = self.data.picking(picking)
        data_picking["weight"] = 80.0
        self.assert_response(
            response,
            next_state="set_quantity",
            data={
                # "picking": self.data.picking(picking),
                "picking": data_picking,
                # "selected_move_line": self.data.move_lines(new_move_line),
                "selected_move_line": data_line,
                "confirmation_required": None,
            },
        )

    def test_previous_processed_line_move_line_not_found(self):
        picking = self._create_picking()
        response = self.service.dispatch(
            "scan_line_repeat",
            params={"picking_id": picking.id, "last_processed_line_id": 123},
        )
        self.assert_response(
            response,
            data=self._data_for_select_move(picking),
            message={
                "message_type": "error",
                "body": "The record you were working on does not exist anymore.",
            },
            next_state="select_move",
        )
