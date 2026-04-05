# Copyright 2019 Roberto Fichera <roberto.fichera@levelprime.com>
# Copyright 2023 Simone Rubino - Aion Tech
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .company import E_INVOICE_HIDE_LINE_TYPE_SELECTION


class ResPartner(models.Model):
    _inherit = "res.partner"

    max_invoice_in_xml = fields.Integer(
        string="Max Invoice # in XML",
        default=lambda self: self.env.company.max_invoice_in_xml,
        help="Maximum number of invoices to group in a single "
        "XML file.\n"
        "If this is 0, then the number configured "
        "in the account settings is considered.",
    )
    e_invoice_hide_line_type = fields.Selection(
        selection=E_INVOICE_HIDE_LINE_TYPE_SELECTION,
        help="Choose which type of descriptive line "
        "will not be present in the e-invoices of this partner.\n"
        "If empty, the same field in the company is evaluated.",
    )

    @api.constrains("max_invoice_in_xml")
    def _validate_max_invoice_in_xml(self):
        for partner in self:
            if partner.max_invoice_in_xml < 0:
                raise ValidationError(
                    _(
                        "The max number of invoice to group "
                        "can't be negative for partner %s",
                        partner.name,
                    )
                )
