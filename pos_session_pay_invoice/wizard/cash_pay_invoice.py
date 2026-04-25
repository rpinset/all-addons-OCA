# Copyright (C) 2017 Creu Blanca
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class CashPayInvoice(models.TransientModel):
    _inherit = "cash.pay.invoice"

    pos_payment_method_id = fields.Many2one(
        "pos.payment.method", string="Payment Method"
    )
    pos_session_id = fields.Many2one("pos.session")
    pos_payment_method_domain = fields.Binary(
        compute="_compute_pos_payment_method_domain"
    )

    @api.depends("pos_session_id")
    @api.depends_context("pos_pay_invoice_domain")
    def _compute_pos_payment_method_domain(self):
        for wizard in self:
            payment_method_available = (
                wizard.pos_session_id.payment_method_ids.filtered(
                    lambda pm: pm.journal_id.type == "cash"
                    if self.env.context.get("pos_pay_invoice_domain") == "in_invoice"
                    else pm.journal_id.type in ["bank", "cash"]
                )
            )
            wizard.pos_payment_method_domain = [
                ("id", "in", payment_method_available.ids)
            ]

    @api.onchange("pos_payment_method_id")
    def _onchange_pos_payment_method_id(self):
        if self.pos_payment_method_id:
            self.journal_id = self.pos_payment_method_id.journal_id

    def _compute_invoice_domain(self):
        res = super()._compute_invoice_domain()
        # Only allow the payment of invoices of the same expected type.
        # By default, in the module account_cash_invoice, the allowed types are:
        #   - Customer: out_invoice, in_refund
        #   - Vendor: in_invoice, out_refund
        # In this module, we will allow the payment of invoices of the same type
        # according to the context pos_pay_invoice_domain:
        #   - Customer: out_invoice
        #   - Vendor: in_invoice
        #   - Refund: out_refund
        pos_pay_invoice_domain = self.env.context.get("pos_pay_invoice_domain")
        if pos_pay_invoice_domain:
            for wizard in self:
                new_domain = []
                for domain in wizard.invoice_domain:
                    if domain[0] == "move_type":
                        new_domain.append(("move_type", "=", pos_pay_invoice_domain))
                    else:
                        new_domain.append(domain)
                wizard.invoice_domain = new_domain
        return res

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        if "invoice_type" in fields_list and self.env.context.get(
            "pos_pay_invoice_type"
        ):
            values["invoice_type"] = self.env.context.get("pos_pay_invoice_type")
        return values

    def _prepare_statement_line_vals(self):
        vals = super()._prepare_statement_line_vals()
        if self.pos_session_id:
            vals["pos_session_id"] = self.pos_session_id.id
        return vals

    def action_pay_invoice(self):
        # When it is a vendor invoice, use the standard method
        # and generate a statement line to reconcile the invoice correctly,
        # because the POS only works with receivable accounts.
        if not self.pos_session_id or self.invoice_id.move_type == "in_invoice":
            return super().action_pay_invoice()
        # If we are in a POS session, we need to create a pos.order
        # and a pos.payment to pay the invoice.
        # This way, when the user closes the session
        # and checks the cash control, the payments are correctly displayed.
        # Otherwise, all payments are shown in Cash regardless of the journal type.
        PosOrder = self.env["pos.order"]
        pos_order = PosOrder.create(self._prepare_pos_order_vals())
        pos_order.write({"name": pos_order._compute_order_name()})
        pos_order.add_payment(self._prepare_pos_payment_vals(pos_order))
        pos_order._apply_invoice_payments()

    def _prepare_pos_order_vals(self):
        return {
            "amount_total": self.amount,
            "partner_id": self.invoice_id.partner_id.id,
            "account_move": self.invoice_id.id,
            "state": "invoiced",
            "to_invoice": False,
            "session_id": self.pos_session_id.id,
            "amount_tax": 0,
            "amount_paid": self.amount,
            "amount_return": 0,
        }

    def _prepare_pos_payment_vals(self, pos_order):
        return {
            "pos_order_id": pos_order.id,
            "amount": pos_order._get_rounded_amount(self.amount),
            "name": self.invoice_id.name,
            "payment_method_id": self.pos_payment_method_id.id,
        }
