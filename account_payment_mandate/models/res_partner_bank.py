# Copyright 2014 Compassion CH - Cyril Sester <csester@compassion.ch>
# Copyright 2014 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Domain


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    mandate_ids = fields.One2many(
        comodel_name="account.banking.mandate",
        inverse_name="partner_bank_id",
        string="Direct Debit Mandates",
        help="Banking mandates represent an authorization that the bank "
        "account owner gives to a company for a specific operation.",
    )

    @api.constrains("company_id")
    def _company_constrains(self):
        for rpb in self:
            if rpb.company_id and (
                self.env["account.banking.mandate"]
                .sudo()
                .search_count(
                    Domain(
                        [
                            ("partner_bank_id", "=", rpb.id),
                            ("company_id", "!=", rpb.company_id.id),
                        ]
                    ),
                )
            ):
                raise ValidationError(
                    self.env._(
                        "You cannot change the company of bank account '%s' "
                        "as there are mandates referencing it that "
                        "belong to another company.",
                        rpb.display_name,
                    )
                )
