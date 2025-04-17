# Copyright 2016-2024 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    returned_payment = fields.Boolean(
        string="Payment returned",
        help="Invoice has been included on a payment that has been returned later.",
        copy=False,
    )

    def check_payment_return(self):
        returned_invoices = (
            self.env["account.partial.reconcile"]
            .search([("origin_returned_move_ids.move_id", "in", self.ids)])
            .mapped("origin_returned_move_ids.move_id")
        )
        returned_invoices.filtered(lambda x: not x.returned_payment).write(
            {"returned_payment": True}
        )
        (self - returned_invoices).filtered("returned_payment").write(
            {"returned_payment": False}
        )

    def _get_all_reconciled_invoice_partials(self):
        res = super()._get_all_reconciled_invoice_partials()
        domain = [("origin_returned_move_ids.move_id", "=", self.id)]
        move_reconciles = self.env["account.partial.reconcile"].search(domain)
        for move_reconcile in move_reconciles:
            res.append(
                {
                    "aml_id": move_reconcile.credit_move_id.id,
                    "partial_id": move_reconcile.id,
                    "amount": move_reconcile.amount,
                    "currency": move_reconcile.credit_move_id.currency_id,
                    "aml": move_reconcile.credit_move_id,
                    "is_exchange": bool(move_reconcile.exchange_move_id),
                }
            )
            res.append(
                {
                    "aml_id": move_reconcile.debit_move_id.id,
                    "partial_id": move_reconcile.id,
                    "amount": -move_reconcile.amount,
                    "currency": move_reconcile.debit_move_id.currency_id,
                    "aml": move_reconcile.debit_move_id,
                    "is_exchange": bool(move_reconcile.exchange_move_id),
                }
            )
        return sorted(res, key=lambda ln: (ln["aml"].date, ln["aml_id"]))


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    partial_reconcile_returned_ids = fields.Many2many(
        comodel_name="account.partial.reconcile",
        relation="account_partial_reconcile_account_move_line_rel",
        column1="move_line_id",
        column2="partial_reconcile_id",
    )


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    origin_returned_move_ids = fields.Many2many(
        comodel_name="account.move.line",
        relation="account_partial_reconcile_account_move_line_rel",
        column1="partial_reconcile_id",
        column2="move_line_id",
    )
