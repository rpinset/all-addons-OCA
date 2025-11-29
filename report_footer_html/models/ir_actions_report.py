# Copyright 2025 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import fields, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    footer_html = fields.Html(
        string="Extra Footer",
        help="This HTML will be displayed in the footer of this report.\n"
        "It's recommended to change Paper Format to a new one that fits "
        "correctly to this report by adjusting 'Bottom Margin (mm)' accordingly.",
    )

    def _render_template(self, template, values=None):
        values = values and dict(values) or {}
        report = self.sudo().search([("report_name", "=", template)], limit=1)
        if report.report_type in ("qweb-pdf", "qweb-html"):
            values["footer_html"] = report.footer_html
        return super()._render_template(template, values=values)
