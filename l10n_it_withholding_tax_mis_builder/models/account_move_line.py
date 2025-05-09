# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    withholding_tax_debit = fields.Float(
        string="Debit without Withholding Tax",
        compute="_compute_withholding_tax_debit_credit",
        store=True,
    )
    withholding_tax_credit = fields.Float(
        string="Credit without Withholding Tax",
        compute="_compute_withholding_tax_debit_credit",
        store=True,
    )

    @api.depends(
        "debit",
        "credit",
        "withholding_tax_amount",
    )
    def _compute_withholding_tax_debit_credit(self):
        for line in self:
            withholding_tax_amount = line.withholding_tax_amount
            withholding_tax_debit = line.debit
            withholding_tax_credit = line.credit
            if not line.company_currency_id.is_zero(withholding_tax_amount):
                if not line.company_currency_id.is_zero(withholding_tax_debit):
                    withholding_tax_debit -= withholding_tax_amount
                else:
                    withholding_tax_credit -= withholding_tax_amount

            line.withholding_tax_debit = withholding_tax_debit
            line.withholding_tax_credit = withholding_tax_credit

    @api.model
    def _inject_withholding_tax_debit_credit_fields(self, fields):
        if "debit" in fields:
            fields.append("withholding_tax_debit")
        if "credit" in fields:
            fields.append("withholding_tax_credit")
        return fields

    @api.model
    def _swap_withholding_tax_debit_credit_groups(self, groups):
        for group in groups:
            group["debit"] = group.pop("withholding_tax_debit")
            group["credit"] = group.pop("withholding_tax_credit")
        return groups

    @api.model
    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        if self.env.context.get("inject_withholding_tax_amounts"):
            self._inject_withholding_tax_debit_credit_fields(fields)

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
            self._swap_withholding_tax_debit_credit_groups(groups)
        return groups
