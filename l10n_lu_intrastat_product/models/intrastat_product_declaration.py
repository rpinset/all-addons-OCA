# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class IntrastatProductDeclaration(models.Model):

    _inherit = "intrastat.product.declaration"

    @api.model
    def _xls_computation_line_fields(self):
        return super()._xls_computation_line_fields() + ["stat_value"]

    @api.model
    def _xls_declaration_line_fields(self):
        return super()._xls_declaration_line_fields() + ["stat_value"]
