# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoices(self, sale_orders):
        if self.advance_payment_method == "delivered" and self.stock_picking_ids:
            return sale_orders.with_context(
                invoice_service_products=self.inv_service_products,
                default_invoice_date=self.invoice_date,
            )._create_invoices_from_pickings(self.stock_picking_ids)
        return super()._create_invoices(sale_orders)
