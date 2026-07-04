# Copyright 2020-23 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _stock_account_prepare_anglo_saxon_out_lines_vals(self):
        res = super()._stock_account_prepare_anglo_saxon_out_lines_vals()
        # Cases in which we have multiple SOL with same product and
        # quantity. We want to ensure that each SOL is only assigned
        # to two distinct COGS pairs of the same invoice.
        assigned_sols_per_move = {}
        # Core emits two consecutive dicts per eligible invoice line
        # (interim + expense) sharing move_id, product_id and quantity.
        # pair_pending carries the SOL chosen for the first dict over to
        # the second one so both halves of the pair are linked to the
        # same sale.order.line. It is popped as soon as it is reused.
        pair_pending = {}
        for i, vals in enumerate(res):
            move_id = vals["move_id"]
            key = (move_id, vals["product_id"], vals["quantity"])
            if key in pair_pending:
                res[i]["sale_line_id"] = pair_pending.pop(key)
                continue
            assigned = assigned_sols_per_move.setdefault(move_id, set())
            am = self.env["account.move"].browse(move_id)
            candidate_sols = am.invoice_line_ids.filtered(
                lambda il: il.product_id.id == vals["product_id"]
                and il.quantity == vals["quantity"]
            ).mapped("sale_line_ids")
            available = candidate_sols.filtered(lambda sol: sol.id not in assigned)
            if available:
                chosen_id = available[0].id
                assigned.add(chosen_id)
                res[i]["sale_line_id"] = chosen_id
                pair_pending[key] = chosen_id
        return res


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    sale_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        string="Sale Order Line",
        ondelete="set null",
        index=True,
        copy=False,
    )

    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        related="sale_line_id.order_id",
        string="Sales Order",
        ondelete="set null",
        store=True,
        index=True,
        copy=False,
    )

    def _copy_data_extend_business_fields(self, values):
        # Same way Odoo standard does for purchase_line_id field
        res = super(AccountMoveLine, self)._copy_data_extend_business_fields(values)
        values["sale_line_id"] = self.sale_line_id.id
        return res
