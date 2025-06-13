# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    group_riba = fields.Boolean(
        "Group C/O", help="Group C/O by customer while issuing."
    )
    riba_exclude_expenses = fields.Boolean(
        string="Exclude expenses Ri.Ba.",
    )
    is_supplier_payment_riba = fields.Boolean(
        string="Is Riba Paymnet",
        related="property_supplier_payment_term_id.riba",
        readonly=True,
    )
    riba_policy_expenses = fields.Selection(
        [
            ("one_a_month", "More invoices, one expense per Month"),
            ("unlimited", "One expense per maturity"),
        ],
        default="one_a_month",
        string="Ri.Ba. Policy expenses",
    )

    def _domain_property_riba_supplier_company_bank_id(self):
        """Allow to select bank accounts linked to the current company."""
        return self.env["res.partner.bank"]._domain_riba_partner_bank_id()

    property_riba_supplier_company_bank_id = fields.Many2one(
        comodel_name="res.partner.bank",
        company_dependent=True,
        string="Company Bank Account for Supplier",
        domain=_domain_property_riba_supplier_company_bank_id,
        help="Bank account used for the Riba of this suplier.",
    )
