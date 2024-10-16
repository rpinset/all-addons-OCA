# Copyright 2017-2020 Akretion France (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    fr_chorus_invoice_format = fields.Selection(
        selection_add=[("xml_cii", "CII 16B XML"), ("pdf_factur-x", "Factur-X PDF")],
        ondelete={"xml_cii": "set null", "pdf_factur-x": "set null"},
    )

    def _check_chorus_invoice_format(self):
        self.ensure_one()
        if (
            self.fr_chorus_invoice_format == "pdf_factur-x"
            and self.xml_format_in_pdf_invoice != "factur-x"
        ):
            raise ValidationError(
                _(
                    "For company '%s', if you select 'Factur-X' as 'Chorus "
                    "Invoice Format', then you should also select 'Factur-X' as "
                    "electronic invoice format in the section 'Customer Invoices'."
                )
                % self.display_name
            )
