# l10n_py_edi_base/wizard/l10n_py_edi_cancel_wizard.py

from odoo import _, api, fields, models
from odoo.exceptions import UserError

# Límites de cancelación por tipo de DTE (en horas)
CANCEL_LIMITS = {
    "1": 48,  # FE: 48 horas
    "4": 48,  # AFE: 48 horas
    "5": 168,  # NCE: 168 horas (7 días)
    "6": 168,  # NDE: 168 horas
    "7": 168,  # NRE: 168 horas
}


class EDICancelWizard(models.TransientModel):
    _name = "l10n_py.edi.cancel.wizard"
    _description = "Wizard para cancelar documento EDI"

    invoice_id = fields.Many2one("account.move", string="Factura", required=True)
    motive = fields.Text(string="Motivo de Cancelación", required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self.env.context.get("active_id"):
            res["invoice_id"] = self.env.context["active_id"]
        return res

    def action_cancel(self):
        """Cancelar documento EDI con verificación de plazos."""
        self.ensure_one()
        if not self.invoice_id:
            raise UserError(_("No se seleccionó una factura"))

        if not self.invoice_id.l10n_py_cdc:
            raise UserError(_("La factura no tiene CDC, no se puede cancelar"))

        # Verificar plazo de cancelación
        self._check_cancel_deadline()

        self.invoice_id.action_cancel_edi()

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Cancelación Exitosa"),
                "message": _("El documento ha sido cancelado"),
                "type": "success",
                "sticky": False,
            },
        }

    def _check_cancel_deadline(self):
        """Verificar si el plazo de cancelación no ha expirado."""
        invoice = self.invoice_id
        doc_type_code = (
            invoice.l10n_latam_document_type_id.code
            if invoice.l10n_latam_document_type_id
            else ""
        )

        limit_hours = CANCEL_LIMITS.get(doc_type_code, 48)

        # Calcular horas desde la aceptación
        if invoice.l10n_py_edi_status == "accepted" and invoice.write_date:
            now = fields.Datetime.now()
            # Usar write_date como proxy de cuando fue aceptado
            delta = now - invoice.write_date
            hours_since = delta.total_seconds() / 3600

            if hours_since > limit_hours:
                raise UserError(
                    _(
                        "El plazo de cancelación ha expirado. "
                        "Tipo %(doc_type)s permite cancelación hasta "
                        "%(limit)s horas después de la aceptación "
                        "(han transcurrido %(elapsed).0f horas).",
                        doc_type=invoice.l10n_latam_document_type_id.name
                        or doc_type_code,
                        limit=limit_hours,
                        elapsed=hours_since,
                    )
                )
