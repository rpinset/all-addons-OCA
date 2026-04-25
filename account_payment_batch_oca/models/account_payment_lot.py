# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.misc import format_date


class AccountPaymentLot(models.Model):
    _name = "account.payment.lot"
    _description = "Account Payment Lot"
    _order = "order_id, name"

    name = fields.Char(required=True, readonly=True)
    order_id = fields.Many2one(
        comodel_name="account.payment.order",
        string="Payment Order",
        ondelete="cascade",
        required=True,
        check_company=True,
        index=True,
        readonly=True,
    )
    payment_type = fields.Selection(related="order_id.payment_type", store=True)
    state = fields.Selection(related="order_id.state", store=True)
    company_id = fields.Many2one(related="order_id.company_id", store=True)
    journal_id = fields.Many2one(related="order_id.journal_id", store=True)
    date = fields.Date(required=True, string="Execution Date", readonly=True)
    currency_id = fields.Many2one("res.currency", readonly=True)
    amount = fields.Monetary(compute="_compute_payment_lot", store=True)
    payment_ids = fields.One2many("account.payment", "payment_lot_id")
    payment_count = fields.Integer(compute="_compute_payment_lot", store=True)

    _sql_constraints = [
        (
            "name_company_uniq",
            "unique(name, company_id)",
            "This lot name already exists!",
        )
    ]

    @api.depends("payment_ids")
    def _compute_payment_lot(self):
        rg_res = self.env["account.payment"]._read_group(
            [("payment_lot_id", "in", self.ids)],
            groupby=["payment_lot_id"],
            aggregates=["__count", "amount:sum"],
        )
        mapped_data = {
            lot.id: {"count": count, "total": total} for (lot, count, total) in rg_res
        }
        for lot in self:
            lot.payment_count = mapped_data.get(lot.id, {}).get("count")
            lot.amount = mapped_data.get(lot.id, {}).get("total", 0)

    @api.depends("name", "date", "currency_id")
    def _compute_display_name(self):
        for lot in self:
            dname = f"{lot.name} {format_date(self.env, lot.date)}"
            if lot.currency_id != lot.company_id.currency_id:
                dname = f"{dname} {lot.currency_id.name}"
            lot.display_name = dname
