# Copyright 2025 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _get_pos_ui_hr_employee(self, params):
        employee_vals = super()._get_pos_ui_hr_employee(params)
        for employee in employee_vals:
            user_id = employee.get("user_id", False)
            if not user_id:
                user_id = self.env.user.id
            user = self.env["res.users"].browse(user_id)
            groups = user.groups_id
            config = self.config_id
            employee.update(
                hasGroupPayment=config.group_payment_id in groups,
                hasGroupDiscount=config.group_discount_id in groups,
                hasGroupNegativeQty=config.group_negative_qty_id in groups,
                hasGroupPriceControl=config.group_change_unit_price_id in groups,
                hasGroupMultiOrder=config.group_multi_order_id in groups,
                hasGroupDeleteOrder=config.group_delete_order_id in groups,
            )
        return employee_vals
