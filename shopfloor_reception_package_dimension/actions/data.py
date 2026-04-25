# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


from odoo.addons.component.core import Component


class DataAction(Component):
    _inherit = "shopfloor.data.action"

    @property
    def _package_parser(self):
        res = super()._package_parser
        res.append("height")
        res.append("length_uom_name:height_uom")
        return res

    @property
    def _package_type_parser(self):
        res = super()._package_type_parser
        res.append("height_required")
        return res
