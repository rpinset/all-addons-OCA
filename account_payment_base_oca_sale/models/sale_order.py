# Copyright 2014-2020 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Inherit native field to add selectable=True in domain
    preferred_payment_method_line_id = fields.Many2one(
        domain="[('payment_type', '=', 'inbound'), ('company_id', '=', company_id), "
        "('selectable', '=', True)]",
    )

    def _get_invoice_grouping_keys(self) -> list:
        """
        When several sale orders are generating invoices,
        we want to add the payment method in grouping criteria.
        """
        keys = super()._get_invoice_grouping_keys()
        if "preferred_payment_method_line_id" not in keys:
            keys.append("preferred_payment_method_line_id")
        return keys
