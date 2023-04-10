# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models

from odoo.addons.report_xlsx_helper.report.report_xlsx_format import FORMATS


class IntrastatProductDeclarationXlsx(models.AbstractModel):

    _inherit = "report.intrastat_product.product_declaration_xls"

    def _get_template(self, declaration):
        template = super()._get_template(declaration)
        template["stat_value"] = {
            "header": {
                "type": "string",
                "value": self._("Statistic value (in euro)"),
                "format": FORMATS["format_theader_yellow_right"],
            },
            "line": {
                "type": "number",
                "value": self._render("line.amount_company_currency"),
                "format": FORMATS["format_tcell_amount_right"],
            },
            "width": 23,
        }
        return template
