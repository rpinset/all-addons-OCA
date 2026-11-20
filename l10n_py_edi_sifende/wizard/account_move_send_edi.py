# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models


class AccountMoveSendEDIWizard(models.TransientModel):
    _inherit = "account.move.send.edi.wizard"

    def action_send(self):
        action = super().action_send()
        move = self.invoice_id
        if (
            move.l10n_py_edi_status in ("error", "rejected")
            and move._l10n_py_sifende_connector()
        ):
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": self.env._("Sifende no aceptó el documento"),
                    "message": move.l10n_py_edi_message,
                    "type": "danger",
                    "sticky": True,
                },
            }
        return action
