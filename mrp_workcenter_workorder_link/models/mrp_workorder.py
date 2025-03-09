# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    def button_workcenter(self):
        self.ensure_one()
        view = self.env.ref("mrp.mrp_workcenter_view")
        action = {
            "view_id": view.id,
            "res_model": "mrp.workcenter",
            "res_id": self.workcenter_id.id,
            "name": "'%s' Workcenter" % self.name,
            "view_mode": "form",
            "type": "ir.actions.act_window",
            "target": "current",
        }
        return action
