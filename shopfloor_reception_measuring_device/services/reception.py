# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component


class Reception(Component):
    _inherit = "shopfloor.reception"

    def _get_measuring_device_domain(self):
        return []

    def set_packaging_dimension__measuring_device_assign(
        self, picking_id, selected_line_id, packaging_id
    ):
        picking = self.env["stock.picking"].sudo().browse(picking_id)
        selected_line = self.env["stock.move.line"].sudo().browse(selected_line_id)
        packaging = self.env["product.packaging"].sudo().browse(packaging_id)
        device_domain = self._get_measuring_device_domain()
        device = self.env["measuring.device"].search(device_domain)
        if not packaging:
            msg = self.msg_store.record_not_found()
        elif not device:
            msg = self.msg_store.no_measuring_device_found()
        elif device._is_being_used():
            msg = self.msg_store.measuring_device_already_in_use(device)
        else:
            packaging._measuring_device_assign(device)
            msg = self.msg_store.measuring_device_selected(device, packaging)
        return self._response_for_set_packaging_dimension(
            picking, selected_line, packaging, message=msg
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

    def _set_packaging_dimension_data_for_packaging(self, packaging):
        # Add flag `is_being_measured` to indicate
        # if the packaging is being measured on the app
        return dict(
            super()._set_packaging_dimension_data_for_packaging(packaging),
            is_being_measured=bool(packaging.measuring_device_id),
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

    def _set_packaging_dimension__measuring_device_next_states(self):
        # If the measuring device assign/cancel button is pressed,
        # get back on the same screen.
        return {"set_packaging_dimension"}

    def set_packaging_dimension__measuring_device_assign(self):
        return self._response_schema(
            next_states=self._set_packaging_dimension__measuring_device_next_states()
        )

    def set_packaging_dimension__measuring_device_release(self):
        return self._response_schema(
            next_states=self._set_packaging_dimension__measuring_device_next_states()
        )

    def _schema_packaging(self):
        schema = super()._schema_packaging()
        schema["schema"]["is_being_measured"] = {"type": "boolean", "default": False}
        return schema
