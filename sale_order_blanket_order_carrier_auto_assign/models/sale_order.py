from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _skip_blanket_carrier_auto_assign(self):
        skip_assign = self.env.context.get("skip_blanket_carrier_auto_assign")
        return self.order_type == "call_off" and not skip_assign

    def _is_auto_set_carrier_on_create(self):
        if self._skip_blanket_carrier_auto_assign():
            return False
        return super()._is_auto_set_carrier_on_create()

    def _is_auto_set_carrier_on_write(self, vals):
        if self._skip_blanket_carrier_auto_assign():
            return False
        return super()._is_auto_set_carrier_on_write(vals)

    def _is_auto_set_carrier_on_confirm(self):
        if self._skip_blanket_carrier_auto_assign():
            return False
        return super()._is_auto_set_carrier_on_confirm()
