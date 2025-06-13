# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class CommissionLineMixin(models.AbstractModel):
    _inherit = "commission.line.mixin"

    def _commission_items_query_params(self, commission, product):
        res = super()._commission_items_query_params(commission, product)
        sale_commission_customer = self.env.context.get("sale_commission_customer")
        if sale_commission_customer:
            res["fis_pos_type"] = (
                sale_commission_customer.fiscal_position_type
                if sale_commission_customer.fiscal_position_type
                else ""
            )
        return res

    def _commission_items_where(self):
        res = super()._commission_items_where()
        if self.env.context.get("sale_commission_customer"):
            res = f"""{res} AND (
                item.fiscal_position_type IS NULL
                OR item.fiscal_position_type = %(fis_pos_type)s
            )
            """
        return res

    def _commission_items_order(self):
        res = super()._commission_items_order()
        if self.env.context.get("sale_commission_customer"):
            res = f"item.fiscal_position_type, {res}"
        return res
