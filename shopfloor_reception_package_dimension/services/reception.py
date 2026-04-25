# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

# from odoo.osv import expression

# from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component

# from odoo.addons.shopfloor.utils import to_float


class Reception(Component):
    _inherit = "shopfloor.reception"

    def _set_destination_handle_extra_params(
        self, picking, selected_move_line, **kwargs
    ):
        if "height" in kwargs:
            height = kwargs.get("height")
            package = selected_move_line.result_package_id
            if package:
                if package.package_type_id.height_required and height <= 0:
                    return self.msg_store.package_height_not_valid()
                package.height = height
        return super()._set_destination_handle_extra_params(
            picking, selected_move_line, **kwargs
        )


class ShopfloorReceptionValidator(Component):
    _inherit = "shopfloor.reception.validator"

    def set_destination(self):
        res = super().set_destination()
        res["height"] = {"type": "float", "required": False}
        res["height_uom"] = {"type": "string", "required": False}
        res["height_required"] = {"type": "boolean", "required": False}
        return res
