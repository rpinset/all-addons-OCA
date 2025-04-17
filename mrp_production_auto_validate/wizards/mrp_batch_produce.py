# Copyright 2025 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models


class MrpBatchProduct(models.TransientModel):
    _inherit = "mrp.batch.produce"

    def action_done(self):
        # Bypass the 'auto_validate' constraint regarding qty to produce
        # when creating a backorder.
        self = self.with_context(disable_check_mo_auto_validate=True)
        return super().action_done()
