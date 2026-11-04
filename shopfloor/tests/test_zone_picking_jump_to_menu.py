# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo.addons.shopfloor.tests.test_zone_picking_base import ZonePickingCommonCase


class ZonePickingJumpToMenu(ZonePickingCommonCase):
    def setUp(self):
        super().setUp()
        self.service.work.current_picking_type = self.picking1.picking_type_id
        self.menu2 = self.env.ref(
            "shopfloor.shopfloor_menu_demo_single_pallet_transfer"
        )

    def assert_response_jump_to_menu(self, response, data=None, message=None):
        self.assert_response(
            response,
            next_state="jump_to_menu",
            data=data,
            message=message,
        )

    def test_set_destination_location_jump_to(self):
        self.service.work.menu.sudo().jump_to_zone_picking_unload_all_menu_id = (
            self.menu2
        )
        moves_before = self.picking1.move_ids
        move_line = moves_before.move_line_ids
        response = self.service.dispatch(
            "set_destination",
            params={
                "move_line_id": move_line.id,
                "barcode": self.packing_location.barcode,
                "quantity": move_line.quantity,
                "confirmation": None,
            },
        )
        data = {
            "menu_id": self.menu2.id,
            "next_state": "start",
            "states_data": '{"start": {}}',
        }
        self.assert_response_jump_to_menu(response, data)
