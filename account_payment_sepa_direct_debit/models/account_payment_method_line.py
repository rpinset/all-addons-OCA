# Copyright 2016 Tecnativa - Antonio Espinosa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from lxml import objectify
from stdnum.eu.at_02 import is_valid

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class AccountPaymentMethodLine(models.Model):
    _inherit = "account.payment.method.line"

    sepa_creditor_identifier = fields.Char(
        string="SEPA Creditor Identifier",
        size=35,
        help="Enter the Creditor Identifier that has been attributed to your "
        "company to make SEPA Direct Debits. If not defined, "
        "SEPA Creditor Identifier from company will be used.\n"
        "This identifier is composed of :\n"
        "- your country ISO code (2 letters)\n"
        "- a 2-digits checkum\n"
        "- a 3-letters business code\n"
        "- a country-specific identifier",
    )

    @api.constrains("sepa_creditor_identifier")
    def _check_sepa_creditor_identifier(self):
        for pay_method_line in self:
            ics = pay_method_line.sepa_creditor_identifier
            if ics and not is_valid(ics):
                raise ValidationError(
                    _("The SEPA Creditor Identifier '%s' is invalid.") % ics
                )

    def _generate_creditor_scheme_identification(
        self,
        parent_node,
        scheme_name_proprietary,
        gen_args,
    ):
        self.ensure_one()
        sepa_creditor_identifier = (
            self.sepa_creditor_identifier or self.company_id.sepa_creditor_identifier
        )
        if not sepa_creditor_identifier:
            raise UserError(
                _(
                    "Missing SEPA Creditor Identifier on company %(company)s "
                    "(or on payment method %(payment_method)s).",
                    company=self.company_id.display_name,
                    payment_method=self.display_name,
                )
            )
        csi_root = objectify.SubElement(parent_node, "CdtrSchmeId")
        csi_id = objectify.SubElement(csi_root, "Id")
        csi_privateid = objectify.SubElement(csi_id, "PrvtId")
        csi_other = objectify.SubElement(csi_privateid, "Othr")
        csi_other.Id = self.env["account.payment.order"]._prepare_field(
            "SEPA Creditor Identifier",
            sepa_creditor_identifier,
            35,
            gen_args,
            raise_if_oversized=True,
        )
        if scheme_name_proprietary:
            csi_scheme_name = objectify.SubElement(csi_other, "SchmeNm")
            csi_scheme_name.Prtry = scheme_name_proprietary
