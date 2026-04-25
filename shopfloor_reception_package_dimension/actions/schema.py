# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.component.core import Component


class ShopfloorSchemaAction(Component):
    _inherit = "shopfloor.schema.action"

    def package(self, with_package_type=False):
        res = super().package(with_package_type=with_package_type)
        res["height"] = {"type": "float", "nullable": True, "required": False}
        res["height_uom"] = {"type": "string", "nullable": True, "required": False}
        return res

    def package_type(self):
        res = super().package_type()
        res["height_required"] = {
            "type": "boolean",
            "nullable": True,
            "required": False,
        }
        return res
