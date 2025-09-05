# Copyright 2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    pricelist_id = fields.Many2one("product.pricelist", readonly=True)

    def _select(self):
        select_str = super()._select()
        return f"{select_str}, move.pricelist_id"
