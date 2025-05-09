# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MisCashFlow(models.Model):

    _inherit = "mis.cash_flow"

    withholding_tax_debit = fields.Float(
        string="Debit without Withholding Tax",
        readonly=True,
    )
    withholding_tax_credit = fields.Float(
        string="Credit without Withholding Tax",
        readonly=True,
    )

    def _init_query(self):
        query = super()._init_query()
        query = query.replace(
            "'move_line' as line_type,",
            """
            'move_line' as line_type,
            CASE
                WHEN aml.amount_residual > 0
                    AND (aml.amount_residual - COALESCE(aml.withholding_tax_amount, 0)) > 0
                THEN aml.amount_residual - COALESCE(aml.withholding_tax_amount, 0)
                ELSE 0.0
            END AS withholding_tax_debit,
            CASE
                WHEN aml.amount_residual < 0
                    AND (aml.amount_residual + COALESCE(aml.withholding_tax_amount, 0)) < 0
                THEN -(aml.amount_residual + COALESCE(aml.withholding_tax_amount, 0))
                ELSE 0.0
            END AS withholding_tax_credit,
            """,
        )
        query = query.replace(
            "'forecast_line' as line_type,",
            """
            'forecast_line' as line_type,
            CASE
                WHEN fl.balance > 0
                THEN fl.balance
                ELSE 0.0
            END AS withholding_tax_debit,
            CASE
                WHEN fl.balance < 0
                THEN -fl.balance
                ELSE 0.0
            END AS withholding_tax_credit,
            """,
        )
        return query

    @api.model
    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        if self.env.context.get("inject_withholding_tax_amounts"):
            self.env["account.move.line"]._inject_withholding_tax_debit_credit_fields(
                fields
            )

        groups = super().read_group(
            domain,
            fields,
            groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy,
        )

        if self.env.context.get("inject_withholding_tax_amounts"):
            self.env["account.move.line"]._swap_withholding_tax_debit_credit_groups(
                groups
            )
        return groups
