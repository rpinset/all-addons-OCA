# Copyright 2023 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_reserve_procurement_values(self, reference):
        values = self._prepare_procurement_values()
        values["reference_ids"] = reference
        values["used_for_sale_reservation"] = True
        return values

    def _should_prebook_stock(self):
        """Checks if SOL product has no_sale_stock_prebook set
        to know if we need to reserve it or not"""
        self.ensure_one()
        for route in self.product_id.route_ids:
            if route.no_sale_stock_prebook:
                return False
        return True

    def _prepare_reserve_procurement(self, reference):
        """Adjusts UOM qty for product, prepares the reservation procurement"""
        product_qty, procurement_uom = self.product_uom_id._adjust_uom_quantities(
            self.product_uom_qty, self.product_id.uom_id
        )
        return self.env["stock.rule"].Procurement(
            self.product_id,
            product_qty,
            procurement_uom,
            self._get_location_final(),
            self.product_id.display_name,
            reference.name,
            self.order_id.company_id,
            self._prepare_reserve_procurement_values(reference),
        )

    def _prepare_reserve_procurements(self, reference):
        """Prepares list of dicts - reserve procurements"""
        procurements = []
        for line in self:
            if not line._should_prebook_stock():
                continue
            procurements.append(line._prepare_reserve_procurement(reference))
        return procurements
