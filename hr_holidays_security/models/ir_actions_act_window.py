# Copyright 2024 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class IrActionsActWindow(models.Model):
    _inherit = "ir.actions.act_window"

    def _compute_views(self):
        # HACK: Not a very nice override but negative groups don't work right in this
        # case as they don't trigger the necessary compute changes in the views. So we
        # want to use a different view for this
        res = super()._compute_views()
        leave_action = self.filtered(
            lambda x: x
            == self.env.ref("hr_holidays.hr_leave_action_action_approve_department")
        )
        allocation_action = self.filtered(
            lambda x: x
            == self.env.ref("hr_holidays.hr_leave_allocation_action_approve_department")
        )
        if leave_action or allocation_action:
            bare_responsible = self.env.user.has_group(
                "hr_holidays.group_hr_holidays_responsible"
            ) and not self.env.user.has_group("hr_holidays.group_hr_holidays_user")
            if bare_responsible and leave_action:
                bare_responsible_form = self.env.ref(
                    "hr_holidays_security.hr_leave_view_form_responsible"
                )
                leave_action.views = [
                    (view, view_type)
                    if view_type != "form"
                    else (bare_responsible_form.id, view_type)
                    for view, view_type in leave_action.views
                ]
            if bare_responsible and allocation_action:
                bare_responsible_form = self.env.ref(
                    "hr_holidays_security.hr_leave_allocation_view_form_manager"
                )
                allocation_action.views = [
                    (view, view_type)
                    if view_type != "form"
                    else (bare_responsible_form.id, view_type)
                    for view, view_type in allocation_action.views
                ]
        return res
