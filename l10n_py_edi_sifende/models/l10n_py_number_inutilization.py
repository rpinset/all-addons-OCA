# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

REQUEST_FIELDS = ("authorization_id", "number_from", "number_to", "motive")


class NumberInutilization(models.Model):
    _inherit = "l10n_py.number.inutilization"

    l10n_py_sifende_event_key = fields.Char(copy=False, readonly=True)

    def write(self, vals):
        changed = [name for name in REQUEST_FIELDS if name in vals]
        for rec in self.filtered("l10n_py_sifende_event_key"):
            if any(
                rec._fields[name].convert_to_write(rec[name], rec) != vals[name]
                for name in changed
            ):
                raise UserError(
                    self.env._(
                        "La inutilización tiene un envío pendiente de confirmación "
                        "en Sifende: el timbrado, el rango y el motivo no se pueden "
                        "cambiar. Envíela de nuevo tal como está o elimínela."
                    )
                )
        return super().write(vals)

    def action_send(self):
        self.check_access("write")
        return super(
            NumberInutilization, self.with_context(l10n_py_inutilization_id=self.id)
        ).action_send()

    # SIFEN acepta inutilizar el número de un documento rechazado
    @api.constrains("number_from", "number_to", "authorization_id")
    def _check_no_used_numbers(self):
        for rec in self:
            used = self.env["account.move"].search_count(
                [
                    ("l10n_py_authorization_id", "=", rec.authorization_id.id),
                    ("l10n_py_invoice_number", ">=", rec.number_from),
                    ("l10n_py_invoice_number", "<=", rec.number_to),
                    ("state", "=", "posted"),
                    ("l10n_py_edi_status", "!=", "rejected"),
                ]
            )
            if used:
                raise ValidationError(
                    self.env._(
                        "Hay %(count)s número(s) en el rango que ya fueron usados "
                        "en facturas confirmadas y no fueron rechazadas por SIFEN.",
                        count=used,
                    )
                )
