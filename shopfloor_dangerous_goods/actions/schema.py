# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.component.core import Component


class ShopfloorSchemaAction(Component):
    _inherit = "shopfloor.schema.action"

    def move_line(self, with_package_type=False, with_picking=False):
        res = super().move_line(
            with_package_type=with_package_type, with_picking=with_picking
        )
        res["has_lq_products"] = {
            "type": "boolean",
            "nullable": False,
            "required": False,
        }
        return res

    def package(self, with_package_type=False):
        res = super().package(with_package_type=with_package_type)
        res["has_lq_products"] = {
            "type": "boolean",
            "nullable": False,
            "required": False,
        }
        return res
