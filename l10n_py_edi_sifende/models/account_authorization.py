# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class AccountAuthorization(models.Model):
    _inherit = "account.authorization"

    # l10n_py_edi_base los lee en la inutilización con estos nombres
    l10n_py_establishment = fields.Char(
        related="establishment", string="Establecimiento (OCA)"
    )
    l10n_py_point = fields.Char(
        related="expedition_point", string="Punto de expedición (OCA)"
    )
    l10n_py_sifende_ultimo_numero_en_uso = fields.Integer(
        string="Último número en uso en Sifende",
        copy=False,
        help="Mayor número que Sifende informó como ya usado o inutilizado en este "
        "punto de expedición. La numeración no lo reutiliza ni retrocede.",
    )

    def _l10n_py_sifende_next_number(self, exclude_move=None):
        self.ensure_one()
        domain = [
            ("l10n_py_authorization_id", "=", self.id),
            ("l10n_py_invoice_number", ">", 0),
            ("move_type", "in", ("out_invoice", "out_refund")),
        ]
        if exclude_move:
            domain.append(("id", "!=", exclude_move.id))
        last = (
            self.env["account.move"]
            .sudo()
            ._read_group(domain, aggregates=["l10n_py_invoice_number:max"])[0][0]
            or 0
        )
        return max(
            last + 1,
            self.invoice_number_from,
            self.l10n_py_sifende_ultimo_numero_en_uso + 1,
        )

    @api.depends("invoice_number_from", "l10n_py_sifende_ultimo_numero_en_uso")
    def _compute_next_number(self):
        res = super()._compute_next_number()
        for authorization in self:
            authorization.next_number = authorization._l10n_py_sifende_next_number()
        return res
