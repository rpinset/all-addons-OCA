# Copyright 2025 CamptoCamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def behaviour(self):
        self.ensure_one()
        res = super().behaviour()
        if self._context.get("is_direct_print"):
            if not res["printer"]:
                raise ValueError(_("No printer found for the report."))
            res["action"] = "server"

        return res
