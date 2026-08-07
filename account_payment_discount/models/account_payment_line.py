# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountPaymentLine(models.Model):
    _inherit = "account.payment.line"

    pay_with_discount = fields.Boolean(
        compute="_compute_pay_with_discount",
        readonly=False,
        store=True,
        precompute=True,
    )

    discount_date = fields.Date(
        related="move_line_id.discount_date",
    )
    discount_amount_currency = fields.Monetary(
        compute="_compute_discount_amount_currency",
        help="Total amount discount included",
    )
    amount_residual_currency = fields.Monetary(
        compute="_compute_amount_residual_currency",
    )

    diff_amount_residual_currency_amount_discount_currency = fields.Monetary(
        compute="_compute_diff_amount_residual_currency_amount_discount_currency",
        string="Discount Amount",
        help="Amount of discount",
    )

    can_have_discount = fields.Boolean(
        related="move_line_id.move_id.invoice_payment_term_id.early_discount"
    )

    @api.depends("order_id.date_prefered", "order_id.date_scheduled")
    def _compute_pay_with_discount(self):
        for rec in self:
            if not rec.can_have_discount:
                rec.pay_with_discount = False
            elif rec.order_id.date_prefered == "now" and rec.discount_date:
                rec.pay_with_discount = rec.discount_date >= fields.Date.today()
            elif (
                rec.order_id.date_prefered == "fixed"
                and rec.discount_date
                and rec.order_id.date_scheduled
            ):
                rec.pay_with_discount = rec.discount_date >= rec.order_id.date_scheduled
            else:
                rec.pay_with_discount = False

    @api.depends("pay_with_discount")
    def _compute_payment_line(self):
        ret = super()._compute_payment_line()

        for rec in self:
            if rec.pay_with_discount:
                rec.amount_currency = rec.discount_amount_currency

        return ret

    @api.depends(
        "move_line_id.discount_amount_currency", "amount_currency", "pay_with_discount"
    )
    def _compute_discount_amount_currency(self):
        """Get total amount with discount including refunds amount (with discount)"""
        for rec in self:
            refund_lines = rec.move_line_id.reconciled_lines_ids.filtered(
                lambda r: r.is_refund
            )
            refund_discount_amount = sum(
                line.discount_amount_currency for line in refund_lines
            )
            total_with_discount = (
                rec.move_line_id.discount_amount_currency + refund_discount_amount
            )
            if rec.order_id.payment_type == "outbound":
                total_with_discount *= -1

            rec.discount_amount_currency = total_with_discount

    @api.depends("move_line_id.amount_residual_currency", "payment_type")
    def _compute_amount_residual_currency(self):
        for rec in self:
            rec.amount_residual_currency = rec.move_line_id.amount_residual_currency * (
                -1 if rec.payment_type == "outbound" else 1
            )

    @api.depends("amount_residual_currency", "discount_amount_currency")
    def _compute_diff_amount_residual_currency_amount_discount_currency(self):
        for rec in self:
            rec.diff_amount_residual_currency_amount_discount_currency = (
                self.currency_id.round(
                    rec.amount_residual_currency - rec.discount_amount_currency
                )
            )

    def _prepare_account_payment_vals(self, payment_lot, pay_sequence):
        """
        Add lines that correspond to early payment discount (and discount on tax)

        If invoice is linked to refunds, also add their discount lines
        """
        vals = super()._prepare_account_payment_vals(payment_lot, pay_sequence)

        lines_with_discount = self.filtered(lambda r: r.pay_with_discount)

        if lines_with_discount:
            epd_aml_values_list = []
            payment_date = lines_with_discount[:1].date
            for aml in lines_with_discount.move_line_id:
                if aml.move_id._is_eligible_for_early_payment_discount(
                    self.currency_id, False
                ):
                    epd_aml_values_list.append(
                        {
                            "aml": aml,
                            "amount_currency": -aml.amount_residual_currency,
                            "balance": aml.currency_id._convert(
                                -aml.amount_residual_currency,
                                aml.company_currency_id,
                                date=payment_date,
                            ),
                        }
                    )
                    refund_lines = aml.reconciled_lines_ids.filtered(
                        lambda r: r.is_refund
                    )
                    for refund_line in refund_lines:
                        amt_curr = -refund_line.amount_residual_currency
                        epd_aml_values_list.append(
                            {
                                "aml": refund_line,
                                "amount_currency": amt_curr,
                                "balance": refund_line.currency_id._convert(
                                    amt_curr,
                                    refund_line.company_currency_id,
                                    date=payment_date,
                                ),
                            }
                        )

            diff = sum(lines_with_discount.mapped("amount_residual_currency")) - sum(
                lines_with_discount.mapped("amount_currency")
            )
            open_amount_currency = diff * (
                -1 if self.order_id.payment_type == "outbound" else 1
            )
            open_balance = self.currency_id._convert(
                open_amount_currency,
                self.company_id.currency_id,
                self.company_id,
                payment_date,
            )

            early_payment_values = self.env[
                "account.move"
            ]._get_invoice_counterpart_amls_for_early_payment_discount(
                epd_aml_values_list, open_balance
            )

            if not self.currency_id.is_zero(diff):
                vals["write_off_line_vals"] = []
                for aml_values_list in early_payment_values.values():
                    vals["write_off_line_vals"] += aml_values_list

        return vals
