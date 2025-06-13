# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoiceLineAgent(models.Model):
    _inherit = "account.invoice.line.agent"

    @api.depends(
        "invoice_id.partner_id",
    )
    def _compute_amount(self):
        res = None
        for line in self:
            res = super(
                AccountInvoiceLineAgent,
                line.with_context(sale_commission_customer=line.invoice_id.partner_id),
            )._compute_amount()
        return res
