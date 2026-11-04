# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import json

from odoo.tests import Form

from odoo.addons.shopfloor.tests.test_single_pack_transfer_base import (
    SinglePackTransferCommonBase,
)

# pylint: disable=missing-return


class TestSinglePackTransferJumptoMenu(SinglePackTransferCommonBase):
    @classmethod
    def setUpClassBaseData(cls, *args, **kwargs):
        super().setUpClassBaseData(*args, **kwargs)
        cls.pack_a = cls.env["stock.quant.package"].create(
            {"location_id": cls.stock_location.id}
        )
        cls.quant_a = (
            cls.env["stock.quant"]
            .sudo()
            .create(
                {
                    "product_id": cls.product_a.id,
                    "location_id": cls.shelf1.id,
                    "quantity": 1,
                    "package_id": cls.pack_a.id,
                }
            )
        )
        cls.shelf1_2 = cls.shelf1.sudo().copy({"name": "Shelf 1_2"})
        cls.pack_b = cls.env["stock.quant.package"].create(
            {"location_id": cls.stock_location.id}
        )
        cls.quant_b = (
            cls.env["stock.quant"]
            .sudo()
            .create(
                {
                    "product_id": cls.product_b.id,
                    "location_id": cls.shelf1_2.id,
                    "quantity": 1,
                    "package_id": cls.pack_b.id,
                }
            )
        )
        cls.picking = cls._create_initial_move(
            lines=[(cls.product_a, 1), (cls.product_b, 1)]
        )
        cls.menu2 = cls.env.ref("shopfloor.shopfloor_menu_demo_zone_picking")
        # The single pack transfer scenario has no zone picking data set up,
        # so configure one zone with stock for the zone picking menu (menu2)
        # to have a non-empty "zones" list when jumping to it.
        cls.zone_picking_sublocation = (
            cls.env["stock.location"]
            .sudo()
            .create(
                {
                    "name": "Zone Picking Sublocation",
                    "location_id": cls.stock_location.id,
                    "barcode": "ZONE_PICKING_SUB",
                }
            )
        )
        cls._update_qty_in_location(cls.zone_picking_sublocation, cls.product_a, 10)
        cls.zone_picking_picking = cls._create_picking(
            picking_type=cls.menu2.picking_type_ids,
            lines=[(cls.product_a, 10)],
        )
        cls.zone_picking_picking.action_assign()

    @classmethod
    def _create_initial_move(cls, lines):
        """Create the move to satisfy the pre-condition before /start"""
        picking_form = Form(cls.env["stock.picking"])
        picking_form.picking_type_id = cls.picking_type
        picking_form.location_id = cls.stock_location
        picking_form.location_dest_id = cls.shelf2
        for line in lines:
            with picking_form.move_ids_without_package.new() as move:
                move.product_id = line[0]
                move.product_uom_qty = line[1]
        picking = picking_form.save()
        picking.action_confirm()
        picking.action_assign()
        return picking

    def _simulate_started(self, package):
        """Replicate what the /start endpoint would do on the given package.

        Used to test the next endpoints (/validate and /cancel)
        """
        package_level = self.picking.move_line_ids.package_level_id.filtered(
            lambda pl: pl.package_id == package
        )
        package_level.is_done = True
        return package_level

    def assert_response_jump_to_menu(self, response, data=None, message=None):
        self.assert_response(
            response,
            next_state="jump_to_menu",
            data=data,
            message=message,
        )

    def test_validate_jump_to_menu(self):
        self.menu.sudo().jump_to_single_pack_transfer_validate_menu_id = self.menu2
        package_level = self._simulate_started(self.pack_a)
        response = self.service.dispatch(
            "validate",
            params={
                "package_level_id": package_level.id,
                "location_barcode": self.shelf2.barcode,
            },
        )
        # The zone picking menu's initial state (reachable through the
        # jump) is "scan_location": _get_data_for_jump_to_menu remaps the
        # "start" state to "scan_location". Build the expected zones data
        # manually (one zone with one assigned move line).
        picking_type = self.menu2.picking_type_ids[0]
        zone_data = dict(
            self.data.location(self.zone_picking_sublocation),
            operation_types=[
                dict(
                    self.data.picking_type(picking_type),
                    lines_count=1,
                    picking_count=1,
                    priority_lines_count=0,
                    priority_picking_count=0,
                )
            ],
            lines_count=1,
            picking_count=1,
            priority_lines_count=0,
            priority_picking_count=0,
        )
        expected_data = {
            "menu_id": self.menu2.id,
            "next_state": "scan_location",
            "states_data": json.dumps({"scan_location": {"zones": [zone_data]}}),
        }
        self.assert_response_jump_to_menu(response, expected_data)

    def test_jump_to_zone_picking_menu(self):
        picking1 = self._create_picking(
            picking_type=self.menu2.picking_type_ids,
            lines=[(self.product_a, 10)],
        )
        self._fill_stock_for_moves(
            picking1.move_ids, in_package=True, location=self.shelf2
        )
        picking1.action_assign()

        self.menu.sudo().jump_to_single_pack_transfer_validate_menu_id = self.menu2
        package_level = self._simulate_started(self.pack_a)
        response = self.service.dispatch(
            "validate",
            params={
                "package_level_id": package_level.id,
                "location_barcode": self.shelf2.barcode,
            },
        )
        jump_data = response["data"]["jump_to_menu"]
        self.assertEqual(jump_data["next_state"], "select_line")
        states_data = json.loads(jump_data["states_data"])
        self.assertIn("scan_location", states_data)
        self.assertIn("select_picking_type", states_data)
        self.assertIn("select_line", states_data)
        move_lines = states_data["select_line"]["move_lines"]
        self.assertTrue(move_lines)
        self.assertEqual(move_lines[0]["product"]["id"], self.product_a.id)

    def test_jump_to_zone_picking_menu_location_not_in_zone(self):
        dest_location = (
            self.env["stock.location"]
            .sudo()
            .create(
                {
                    "name": "Non Zone Destination",
                    "location_id": self.input_location.id,
                    "barcode": "NON_ZONE_DEST",
                }
            )
        )
        picking = self._create_picking(
            picking_type=self.picking_type,
            lines=[(self.product_a, 1)],
            location_dest_id=dest_location,
        )
        self._fill_stock_for_moves(
            picking.move_ids, in_package=True, location=self.shelf1
        )
        picking.action_assign()
        package_level = picking.move_line_ids.package_level_id
        package_level.is_done = True

        self.menu.sudo().jump_to_single_pack_transfer_validate_menu_id = self.menu2
        response = self.service.dispatch(
            "validate",
            params={
                "package_level_id": package_level.id,
                "location_barcode": dest_location.barcode,
            },
        )
        jump_data = response["data"]["jump_to_menu"]
        self.assertEqual(jump_data["next_state"], "scan_location")
        states_data = json.loads(jump_data["states_data"])
        self.assertEqual(set(states_data), {"scan_location"})

    def test_jump_to_zone_picking_menu_zone_without_ready_lines(self):
        self.menu.sudo().jump_to_single_pack_transfer_validate_menu_id = self.menu2
        package_level = self._simulate_started(self.pack_a)
        response = self.service.dispatch(
            "validate",
            params={
                "package_level_id": package_level.id,
                "location_barcode": self.shelf2.barcode,
            },
        )
        jump_data = response["data"]["jump_to_menu"]
        self.assertEqual(jump_data["next_state"], "scan_location")
        states_data = json.loads(jump_data["states_data"])
        self.assertEqual(set(states_data), {"scan_location"})
