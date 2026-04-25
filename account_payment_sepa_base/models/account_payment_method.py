# Copyright 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountPaymentMethod(models.Model):
    _inherit = "account.payment.method"

    pain_version = fields.Selection([], string="PAIN Version")
    warn_not_sepa = fields.Boolean(string="Warn If Not SEPA")

    def _get_xsd_file_path(self):
        """This method is designed to be inherited in the SEPA modules"""
        self.ensure_one()
        raise UserError(_("No XSD file path found for payment method '%s'") % self.name)

    _sql_constraints = [
        (
            # Inherit native constraint of the 'account' module to add pain_version
            "name_code_unique",
            "unique(code, payment_type, pain_version)",
            "A payment method of the same type already exists with this code"
            " and PAIN version",
        )
    ]
