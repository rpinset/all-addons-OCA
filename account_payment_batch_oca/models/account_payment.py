# Copyright 2019 ACSONE SA/NV
# Copyright 2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.misc import format_amount, format_date


class AccountPayment(models.Model):
    _inherit = "account.payment"

    payment_order_id = fields.Many2one(
        comodel_name="account.payment.order", readonly=True
    )
    payment_lot_id = fields.Many2one(comodel_name="account.payment.lot", readonly=True)
    payment_line_ids = fields.Many2many(
        comodel_name="account.payment.line", readonly=True
    )
    order_state = fields.Selection(
        related="payment_order_id.state", string="Payment Order State"
    )

    @api.depends("payment_type", "journal_id")
    def _compute_payment_method_line_fields(self):
        res = super()._compute_payment_method_line_fields()
        for pay in self:
            if pay.payment_order_id:
                pay.available_payment_method_line_ids = (
                    pay.journal_id._get_available_payment_method_lines(pay.payment_type)
                )
            else:
                pay.available_payment_method_line_ids = (
                    pay.journal_id._get_available_payment_method_lines(
                        pay.payment_type
                    ).filtered(lambda x: not x.payment_method_id.payment_order_ok)
                )
            to_exclude = pay._get_payment_method_codes_to_exclude()
            if to_exclude:
                pay.available_payment_method_line_ids = [
                    line.id
                    for line in pay.available_payment_method_line_ids
                    if line.code not in to_exclude
                ]
        return res

    # Don't generate a journal entry when the account.payment is an "internal transfer"
    # of the company i.e. a money transfer between 2 bank accounts of the company
    @api.depends("partner_id", "company_id", "payment_type")
    def _compute_outstanding_account_id(self):
        res = super()._compute_outstanding_account_id()
        for pay in self:
            if (
                pay.company_id.partner_id == pay.partner_id
                and pay.payment_type == "outbound"
            ):
                pay.outstanding_account_id = False
        return res

    def _prepare_payment_order_mail(self, lang, account_number_scrambled_ctx):
        res = []
        detail_col = False
        for pay in sorted(self, key=lambda p: p.date):
            pay_dict = {
                "id": pay.id,
                "name": pay.name,
                "memo": pay.memo,
                "payment_ref": pay.payment_reference,
                "date": format_date(self.env, pay.date, lang),
                "amount": format_amount(self.env, pay.amount, pay.currency_id, lang),
                "currency": pay.currency_id.name,
                "bank_account_number_scrambled": pay.partner_bank_id.with_context(
                    **account_number_scrambled_ctx
                ).acc_number_scrambled,
                "bank_account_number": pay.partner_bank_id.acc_number,
                "lines": [],
            }
            if len(pay.payment_line_ids) > 1:
                detail_col = True
                for line in pay.payment_line_ids:
                    pay_dict["lines"].append(
                        {
                            "communication": line.communication,
                            "amount": format_amount(
                                self.env, line.amount_currency, line.currency_id, lang
                            ),
                            "currency": line.currency_id.name,
                            "id": line.id,
                        }
                    )
            res.append(pay_dict)
        return res, detail_col
