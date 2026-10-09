# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component


class Reception(Component):
    _inherit = "shopfloor.reception"

    def _get_measuring_device_domain(self):
        warehouse = self.work.menu.picking_type_ids.warehouse_id
        return [
            ("warehouse_id", "in", warehouse.ids),
            ("state", "=", "ready"),
        ]

    def set_packaging_dimension__measuring_device_assign(
        self, picking_id, selected_line_id, packaging_id
    ):
        picking = self.env["stock.picking"].sudo().browse(picking_id)
        selected_line = self.env["stock.move.line"].sudo().browse(selected_line_id)
        packaging = self.env["product.packaging"].sudo().browse(packaging_id)
        device_domain = self._get_measuring_device_domain()
        device = self.env["measuring.device"].search(device_domain, limit=1)
        msg = ""
        if not packaging:
            msg = self.msg_store.record_not_found()
        elif not device:
            msg = self.msg_store.no_measuring_device_found()
        elif device._is_being_used():
            msg = self.msg_store.measuring_device_already_in_use(device)
        if msg:
            return self._response_for_set_packaging_dimension(
                picking, selected_line, packaging, message=msg
            )
        packaging._measuring_device_assign(device)
        return self._response_for_use_measuring_device(
            picking, selected_line, packaging
        )

    def set_packaging_dimension__measuring_device_release(
        self, picking_id, selected_line_id, packaging_id
    ):
        picking = self.env["stock.picking"].sudo().browse(picking_id)
        selected_line = self.env["stock.move.line"].sudo().browse(selected_line_id)
        packaging = self.env["product.packaging"].sudo().browse(packaging_id)
        device = packaging.measuring_device_id
        if not packaging:
            msg = self.msg_store.record_not_found()
        elif not device:
            msg = self.msg_store.no_measuring_device_to_release(packaging)
        else:
            packaging._measuring_device_release()
            msg = self.msg_store.measuring_device_released(packaging, device)
        return self._response_for_set_packaging_dimension(
            picking, selected_line, packaging, message=msg
        )

    def _response_for_use_measuring_device(
        self, picking, line, packaging, message=None
    ):
        return self._response(
            next_state="use_measuring_device",
            data={
                "picking": self.data.picking(picking),
                "selected_move_line": self.data.move_line(line),
                "packaging": self._set_packaging_dimension_data_for_packaging(
                    packaging
                ),
                "measuring_device": self.data.measuring_device(
                    packaging.measuring_device_id
                ),
            },
            message=message,
        )


class ShopfloorReceptionValidator(Component):
    _inherit = "shopfloor.reception.validator"

    def set_packaging_dimension__measuring_device_assign(self):
        return {
            "picking_id": {"coerce": to_int, "required": True, "type": "integer"},
            "selected_line_id": {
                "coerce": to_int,
                "required": True,
                "type": "integer",
            },
            "packaging_id": {"coerce": to_int, "required": True, "type": "integer"},
        }

    def set_packaging_dimension__measuring_device_release(self):
        return {
            "picking_id": {"coerce": to_int, "required": True, "type": "integer"},
            "selected_line_id": {
                "coerce": to_int,
                "required": True,
                "type": "integer",
            },
            "packaging_id": {"coerce": to_int, "required": True, "type": "integer"},
        }


class ShopfloorReceptionValidatorResponse(Component):
    _inherit = "shopfloor.reception.validator.response"

    def _states(self):
        res = super()._states()
        res.update({"use_measuring_device": self._schema_use_measuring_device})
        return res

    @property
    def _schema_use_measuring_device(self):
        return {
            "picking": {"type": "dict", "schema": self.schemas.picking()},
            "selected_move_line": {"type": "dict", "schema": self.schemas.move_line()},
            "packaging": self._schema_packaging(),
            "measuring_device": {
                "type": "dict",
                "schema": self.schemas.measuring_device(),
                "required": False,
            },
        }

    def _set_packaging_dimension__measuring_device_next_states(self):
        # If the measuring device assign/cancel button is pressed,
        # get back on the same screen.
        return {"set_packaging_dimension", "use_measuring_device"}

    def set_packaging_dimension__measuring_device_assign(self):
        return self._response_schema(
            next_states=self._set_packaging_dimension__measuring_device_next_states()
        )

    def set_packaging_dimension__measuring_device_release(self):
        return self._response_schema(
            next_states=self._set_packaging_dimension__measuring_device_next_states()
        )

    def _set_packaging_dimension_next_states(self):
        res = super()._set_packaging_dimension_next_states()
        res.update({"use_measuring_device"})
        return res
