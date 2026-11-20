# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, models


class AccountMoveSendWizard(models.TransientModel):
    _inherit = "account.move.send.wizard"

    @api.depends("move_id")
    def _compute_display_pdf_report_id(self):
        res = super()._compute_display_pdf_report_id()
        for wizard in self.filtered(lambda w: w.move_id._l10n_py_sifende_has_kude()):
            wizard.display_pdf_report_id = False
        return res
