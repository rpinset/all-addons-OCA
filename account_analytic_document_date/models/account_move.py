# Copyright 2024 (APSL - Nagarro) Miquel Pascual, Bernat Obrador
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    analytic_document_date = fields.Date()

    @api.onchange("invoice_date", "date")
    def _onchange_invoice_date(self):
        for record in self:
            if not record.analytic_document_date:
                record.analytic_document_date = record.invoice_date or record.date

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            analytic_document_date = (
                vals.get("analytic_document_date")
                or vals.get("invoice_date")
                or vals.get("date")
            )
            vals["analytic_document_date"] = analytic_document_date

        return super().create(vals_list)

    def action_post(self):
        res = super().action_post()
        for record in self:
            if not record.analytic_document_date:
                record.analytic_document_date = record.invoice_date
        return res
