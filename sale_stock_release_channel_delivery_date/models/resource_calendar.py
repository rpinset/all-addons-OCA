# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import models


class ResourceCalendar(models.Model):
    _inherit = "resource.calendar"

    def write(self, vals):
        res = super().write(vals)
        self.env.registry.clear_cache()
        return res
