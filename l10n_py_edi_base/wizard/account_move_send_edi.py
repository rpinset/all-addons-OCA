# l10n_py_edi_base/wizard/account_move_send_edi.py

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountMoveSendEDIWizard(models.TransientModel):
    _name = "account.move.send.edi.wizard"
    _description = "Wizard para enviar factura a EDI"

    invoice_id = fields.Many2one("account.move", string="Factura", required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get("active_id"):
            res["invoice_id"] = self.env.context["active_id"]
        return res

    def action_send(self):
        """Enviar factura a EDI"""
        self.ensure_one()
        if not self.invoice_id:
            raise UserError(_("No se seleccionó una factura"))

        self.invoice_id.action_send_edi()

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Envío Exitoso"),
                "message": _("La factura ha sido enviada al sistema EDI"),
                "type": "success",
                "sticky": False,
            },
        }
