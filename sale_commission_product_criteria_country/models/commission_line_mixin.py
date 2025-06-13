# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class CommissionLineMixin(models.AbstractModel):
    _inherit = "commission.line.mixin"

    def _commission_items_query_params(self, commission, product):
        res = super()._commission_items_query_params(commission, product)
        sale_commission_customer = self.env.context.get("sale_commission_customer")
        if sale_commission_customer:
            res["country"] = (
                sale_commission_customer.country_id.id
                if sale_commission_customer.country_id
                else 0
            )
        return res

    def _commission_items_where(self):
        res = super()._commission_items_where()
        if self.env.context.get("sale_commission_customer"):
            res = f"""{res} AND (
                item.country_id IS NULL
                OR item.country_id = %(country)s
            )
            """
        return res

    def _commission_items_order(self):
        res = super()._commission_items_order()
        if self.env.context.get("sale_commission_customer"):
            res = f"item.country_id, {res}"
        return res
