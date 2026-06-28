# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HrExpenseSheet(models.Model):
    _name = "hr.expense.sheet"
    _inherit = ["hr.expense.sheet", "tier.validation"]

    _state_field = "approval_state"
    _state_from = ["submit"]
    _state_to = ["approve", "post", "done"]

    _tier_validation_manual_config = False

    def _allow_to_remove_reviews(self, values):
        self.ensure_one()
        res = super()._allow_to_remove_reviews(values)
        # Reset to draft, approval_state is set to False
        if self._name == "hr.expense.sheet" and self._state_field in values:
            state_to = values[self._state_field]
            if not state_to:
                return True
        return res

    @api.model
    def _get_validation_exceptions(self, extra_domain=None, add_base_exceptions=True):
        res = super()._get_validation_exceptions(
            extra_domain=extra_domain, add_base_exceptions=add_base_exceptions
        )
        if add_base_exceptions:
            res.append("accounting_date")
        return list(set(res))
