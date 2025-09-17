# Copyright 2024-Today GRAP (<http://www.grap.coop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def _sync_user(self, user, employee_has_image=False):
        vals = super()._sync_user(user, employee_has_image=employee_has_image)
        vals.update({"firstname": user.firstname, "lastname": user.lastname})
        return vals
