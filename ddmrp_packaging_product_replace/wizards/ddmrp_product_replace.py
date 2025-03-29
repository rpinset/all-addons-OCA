# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class DdmrpProductReplace(models.TransientModel):
    _inherit = "ddmrp.product.replace"

    def _get_new_buffer_default_value(self):
        vals = super()._get_new_buffer_default_value()
        vals["packaging_id"] = False
        return vals
