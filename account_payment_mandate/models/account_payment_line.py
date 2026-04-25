# Copyright 2014 Compassion CH - Cyril Sester <csester@compassion.ch>
# Copyright 2014 Tecnativa - Pedro M. Baeza
# Copyright 2015-16 Akretion - Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountPaymentLine(models.Model):
    _inherit = "account.payment.line"

    mandate_id = fields.Many2one(
        comodel_name="account.banking.mandate",
        compute="_compute_mandate_id",
        store=True,
        readonly=False,
        precompute=True,
        string="Direct Debit Mandate",
        domain="[('state', 'in', ('valid', 'final')), ('partner_id', '=', partner_id), "
        "('company_id', '=', company_id)]",
        check_company=True,
    )
    mandate_required = fields.Boolean(
        related="order_id.payment_method_id.mandate_required"
    )

    @api.depends("partner_id", "move_line_id")
    def _compute_mandate_id(self):
        for line in self:
            mandate = False
            move = line.move_line_id.move_id
            payment_method = line.order_id.payment_method_id
            if payment_method.mandate_required:
                if move and move.mandate_id:
                    mandate = move.mandate_id
                elif line.partner_id:
                    mandate = line.partner_id.valid_mandate_id
            line.mandate_id = mandate

    @api.depends("mandate_id")
    def _compute_partner_bank_id(self):
        res = super()._compute_partner_bank_id()
        for line in self:
            payment_method = line.order_id.payment_method_id
            if payment_method.mandate_required:
                if line.mandate_id:
                    line.partner_bank_id = line.mandate_id.partner_bank_id
                else:
                    line.partner_bank_id = False
        return res

    @api.constrains("mandate_id", "partner_bank_id")
    def _check_mandate_bank_link(self):
        for pline in self:
            if (
                pline.mandate_id
                and pline.partner_bank_id
                and pline.mandate_id.partner_bank_id != pline.partner_bank_id
            ):
                raise ValidationError(
                    _(
                        "The payment line number {line_number} has "
                        "the bank account '{line_bank_account}' which "
                        "is not attached to the mandate '{mandate_ref}' "
                        "(this mandate is attached to the bank account "
                        "'{mandate_bank_account}')."
                    ).format(
                        line_number=pline.name,
                        line_bank_account=pline.partner_bank_id.acc_number,
                        mandate_ref=pline.mandate_id.display_name,
                        mandate_bank_account=pline.mandate_id.partner_bank_id.acc_number,
                    )
                )

    def _draft2open_payment_line_check(self):
        errors = super()._draft2open_payment_line_check()
        if self.mandate_required and not self.mandate_id:
            errors.append(
                _("Missing mandate on payment line '%s'.") % self.display_name
            )
        return errors

    @api.model
    def _payment_grouping_fields(self):
        res = super()._payment_grouping_fields()
        res.append("mandate_id")
        return res
