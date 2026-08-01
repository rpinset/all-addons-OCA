# Copyright (C) 2019, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    type = fields.Selection(selection_add=[("google_map", "Google Maps")])

    def _get_view_info(self):
        return {"google_map": {"icon": "fa fa-map-o"}} | super()._get_view_info()
