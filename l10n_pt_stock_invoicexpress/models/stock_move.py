# Copyright (C) 2021 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _prepare_invoicexpress_line_vals(self):
        self.ensure_one()
        tax = self.sale_line_id.tax_id[:1]
        tax_detail = {"name": tax.name} if tax else {}

        # Build description
        description = self.description_picking or self.product_id.name or ""
        if self.picking_id.picking_type_id.invoicexpress_include_uom:
            description = f"{description} ({self.product_uom.name})"

        return {
            "name": self.product_id.default_code or self.product_id.display_name,
            "description": description,
            # TODO: add an option to allow having the prices set?
            "unit_price": 0.0,  # self.sale_line_id.price_unit,
            "quantity": self.quantity,
            "discount": self.sale_line_id.discount,
            "tax": tax_detail,
        }
