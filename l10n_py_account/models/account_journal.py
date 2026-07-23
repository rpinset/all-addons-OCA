# l10n_py_account/models/account_journal.py

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    # ============== CAMPOS EDI PARAGUAY ==============

    l10n_py_establishment = fields.Char(
        string="Establecimiento",
        size=3,
        default="001",
        help="Código de establecimiento (3 dígitos)",
    )

    l10n_py_point = fields.Char(
        string="Punto de Expedición",
        size=3,
        default="001",
        help="Código de punto de expedición (3 dígitos)",
    )

    l10n_py_authorization_id = fields.Many2one(
        "account.authorization",
        string="Timbrado",
        domain="[('company_id', '=', company_id), ('active', '=', True)]",
        help="Timbrado autorizado por SET para este diario",
    )

    l10n_py_authorization_validity = fields.Date(
        string="Vencimiento del Timbrado",
        related="l10n_py_authorization_id.date_to",
        store=True,
        readonly=True,
        help="Fecha de vencimiento del timbrado",
    )

    # ============== CONSTRAINT METHODS ==============

    @api.constrains("l10n_py_establishment")
    def _check_establishment(self):
        """Validar formato del establecimiento"""
        for journal in self:
            if journal.l10n_py_establishment:
                if not journal.l10n_py_establishment.isdigit():
                    raise ValidationError(_("El establecimiento debe ser numérico"))
                if len(journal.l10n_py_establishment) != 3:
                    raise ValidationError(_("El establecimiento debe tener 3 dígitos"))

    @api.constrains("l10n_py_point")
    def _check_point(self):
        """Validar formato del punto"""
        for journal in self:
            if journal.l10n_py_point:
                if not journal.l10n_py_point.isdigit():
                    raise ValidationError(_("El punto de expedición debe ser numérico"))
                if len(journal.l10n_py_point) != 3:
                    raise ValidationError(
                        _("El punto de expedición debe tener 3 dígitos")
                    )

    @api.constrains("l10n_py_authorization_id")
    def _check_timbrado_consistency(self):
        """Validar consistencia del timbrado con establecimiento y punto"""
        for journal in self:
            if journal.l10n_py_authorization_id:
                if (
                    journal.l10n_py_authorization_id.establishment
                    != journal.l10n_py_establishment
                    or journal.l10n_py_authorization_id.expedition_point
                    != journal.l10n_py_point
                ):
                    raise ValidationError(
                        _(
                            "El timbrado seleccionado no corresponde al "
                            "establecimiento y punto de expedición "
                            "configurados en el diario."
                        )
                    )
