# Copyright 2019 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MaintenanceRequest(models.Model):

    _inherit = "maintenance.request"

    purchase_order_ids = fields.Many2many(
        "purchase.order",
        "maintenance_purchase_order",
        "maintenance_request_id",
        "purchase_order_id",
        groups="purchase.group_purchase_user",
        string="Purchase Orders",
        copy=False,
    )
    purchases_count = fields.Integer(
        compute="_compute_purchases_count",
        store=True,
        groups="purchase.group_purchase_user",
    )

    total_purchase_amount = fields.Monetary(
        compute="_compute_total_purchase_amount",
        store=True,
        groups="purchase.group_purchase_user",
        currency_field="currency_id",
    )

    currency_id = fields.Many2one(
        "res.currency",
        compute="_compute_currency_id",
        store=True,
        readonly=True,
    )

    # The company is not required so we have to ensure that a currency is stablished
    @api.depends("company_id.currency_id")
    def _compute_currency_id(self):
        for record in self:
            record.currency_id = (
                record.company_id.currency_id.id or self.env.company.currency_id.id
            )

    @api.depends(
        "purchase_order_ids.amount_total",
        "purchase_order_ids.currency_id",
        "currency_id",
        "purchase_order_ids.state",
    )
    def _compute_total_purchase_amount(self):
        date = self.env.context.get("actual_date") or fields.Date.today()
        for record in self:
            company_currency = record.currency_id
            total = sum(
                po.currency_id._convert(
                    po.amount_total,
                    company_currency,
                    record.company_id,
                    date,
                )
                for po in record.purchase_order_ids.filtered(
                    lambda po: po.state in ("purchase", "done")
                )
            )
            record.total_purchase_amount = total

    @api.depends("purchase_order_ids")
    def _compute_purchases_count(self):
        for record in self:
            record.purchases_count = len(record.purchase_order_ids.ids)
