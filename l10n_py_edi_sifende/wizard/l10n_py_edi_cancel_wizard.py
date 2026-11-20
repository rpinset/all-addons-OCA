# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models


class EDICancelWizard(models.TransientModel):
    _inherit = "l10n_py.edi.cancel.wizard"

    def action_cancel(self):
        return super(
            EDICancelWizard, self.with_context(l10n_py_cancel_motive=self.motive)
        ).action_cancel()
