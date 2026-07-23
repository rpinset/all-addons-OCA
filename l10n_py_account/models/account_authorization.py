# l10n_py_account/models/account_authorization.py
import re
from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

MAX_INVOICE_NUMBER = 9999999


class AccountAuthorization(models.Model):
    """
    Modelo para gestionar timbrados (autorizaciones) de la SET Paraguay
    """

    _name = "account.authorization"
    _description = "Autorización de Facturación (Timbrado)"
    _order = "date_from desc, id desc"

    name = fields.Char(
        string="Número de Timbrado",
        required=True,
        size=8,
        help="Número de timbrado otorgado por la SET",
    )

    date_from = fields.Date(
        string="Fecha de Inicio",
        required=True,
        help="Fecha desde la cual el timbrado es válido",
    )

    date_to = fields.Date(
        string="Fecha de Vencimiento",
        required=True,
        help="Fecha hasta la cual el timbrado es válido",
    )

    invoice_number_from = fields.Integer(
        string="Número Desde",
        required=True,
        help="Primer número de factura autorizado",
    )

    invoice_number_to = fields.Integer(
        string="Número Hasta",
        required=True,
        help="Último número de factura autorizado",
    )

    establishment = fields.Char(
        string="Establecimiento",
        required=True,
        size=3,
        default="001",
        help="Código de establecimiento (3 dígitos)",
    )

    expedition_point = fields.Char(
        string="Punto de Expedición",
        required=True,
        size=3,
        default="001",
        help="Código de punto de expedición (3 dígitos)",
    )

    series = fields.Char(
        string="Serie",
        size=2,
        default="AA",
        help="Serie del timbrado (2 letras mayúsculas, AA-ZZ). "
        "Permite reiniciar numeración cuando se agota la faja.",
    )

    l10n_latam_document_type_id = fields.Many2one(
        comodel_name="l10n_latam.document.type",
        string="Tipo de Documento",
        required=True,
        help="Tipo de documento LATAM (Factura, NC, ND, etc.)",
    )

    company_id = fields.Many2one(
        "res.company",
        string="Compañía",
        required=True,
        default=lambda self: self.env.company,
    )

    active = fields.Boolean(
        string="Activo",
        default=True,
        help="Marcar como inactivo para deshabilitar el timbrado",
    )

    state = fields.Selection(
        [
            ("valid", "Vigente"),
            ("expired", "Vencido"),
            ("to_expire", "Por Vencer"),
        ],
        string="Estado",
        compute="_compute_state",
        store=True,
    )

    next_number = fields.Integer(
        string="Próximo Número",
        compute="_compute_next_number",
        help="Próximo número de factura a utilizar",
    )

    used_numbers = fields.Integer(
        string="Números Utilizados",
        compute="_compute_used_numbers",
        help="Cantidad de números ya utilizados",
    )

    remaining_numbers = fields.Integer(
        string="Números Disponibles",
        compute="_compute_remaining_numbers",
        help="Cantidad de números aún disponibles",
    )

    usage_percentage = fields.Float(
        string="Porcentaje de Uso",
        compute="_compute_usage_percentage",
        help="Porcentaje de números utilizados respecto al total autorizado",
    )

    _sql_constraints = [
        (
            "unique_timbrado",
            "unique(name, establishment, expedition_point, series, "
            "l10n_latam_document_type_id, company_id)",
            "La combinación timbrado/establecimiento/punto de expedición/"
            "serie/tipo de documento debe ser única.",
        ),
    ]

    @api.depends("date_from", "date_to")
    def _compute_state(self):
        """Calcula el estado del timbrado basado en las fechas"""
        today = date.today()
        for record in self:
            if not record.date_from or not record.date_to:
                record.state = "valid"
                continue

            if record.date_to < today:
                record.state = "expired"
            elif (record.date_to - today).days <= 30:
                record.state = "to_expire"
            else:
                record.state = "valid"

    def _compute_next_number(self):
        """Calcula el próximo número disponible"""
        for record in self:
            last_invoice = self.env["account.move"].search(
                [
                    ("l10n_py_authorization_id", "=", record.id),
                    ("move_type", "in", ["out_invoice", "out_refund"]),
                ],
                order="l10n_py_invoice_number desc",
                limit=1,
            )

            if last_invoice and last_invoice.l10n_py_invoice_number:
                record.next_number = last_invoice.l10n_py_invoice_number + 1
            else:
                record.next_number = record.invoice_number_from

    def _compute_used_numbers(self):
        """Calcula cuántos números se han utilizado"""
        for record in self:
            count = self.env["account.move"].search_count(
                [
                    ("l10n_py_authorization_id", "=", record.id),
                    ("move_type", "in", ["out_invoice", "out_refund"]),
                ]
            )
            record.used_numbers = count

    def _compute_remaining_numbers(self):
        """Calcula cuántos números quedan disponibles"""
        for record in self:
            total = record.invoice_number_to - record.invoice_number_from + 1
            record.remaining_numbers = total - record.used_numbers

    def _compute_usage_percentage(self):
        """Calcula el porcentaje de uso de la faja de numeración"""
        for record in self:
            total = record.invoice_number_to - record.invoice_number_from + 1
            if total > 0:
                record.usage_percentage = (record.used_numbers / total) * 100
            else:
                record.usage_percentage = 0.0

    @api.constrains("name")
    def _check_timbrado_format(self):
        """Valida el formato del número de timbrado"""
        for record in self:
            if not record.name.isdigit() or len(record.name) != 8:
                raise ValidationError(
                    _(
                        "El número de timbrado debe contener exactamente "
                        "8 dígitos numéricos."
                    )
                )

    @api.constrains("establishment", "expedition_point")
    def _check_codes_format(self):
        """Valida el formato de establecimiento y punto de expedición"""
        for record in self:
            if not record.establishment.isdigit() or len(record.establishment) != 3:
                raise ValidationError(
                    _(
                        "El código de establecimiento debe contener "
                        "exactamente 3 dígitos."
                    )
                )
            if (
                not record.expedition_point.isdigit()
                or len(record.expedition_point) != 3
            ):
                raise ValidationError(
                    _(
                        "El código de punto de expedición debe contener "
                        "exactamente 3 dígitos."
                    )
                )

    @api.constrains("invoice_number_from", "invoice_number_to")
    def _check_invoice_range(self):
        """Valida que el rango de numeración sea válido"""
        for record in self:
            if record.invoice_number_from <= 0:
                raise ValidationError(_("El número inicial debe ser mayor a cero."))
            if record.invoice_number_to <= record.invoice_number_from:
                raise ValidationError(
                    _("El número final debe ser mayor al número inicial.")
                )
            if record.invoice_number_to > MAX_INVOICE_NUMBER:
                raise ValidationError(
                    _(
                        "El número final no puede exceder %(max)s.",
                        max=MAX_INVOICE_NUMBER,
                    )
                )

    @api.constrains("series")
    def _check_series_format(self):
        """Valida que la serie sea exactamente 2 letras mayúsculas (AA-ZZ)"""
        for record in self:
            if record.series and not re.match(r"^[A-Z]{2}$", record.series):
                raise ValidationError(
                    _(
                        "La serie debe ser exactamente 2 letras mayúsculas "
                        "(ej: AA, AB, ZZ)."
                    )
                )

    @api.constrains("date_from", "date_to")
    def _check_dates(self):
        """Valida que las fechas sean coherentes"""
        for record in self:
            if record.date_to < record.date_from:
                raise ValidationError(
                    _(
                        "La fecha de vencimiento debe ser posterior "
                        "a la fecha de inicio."
                    )
                )

    @api.depends(
        "name",
        "establishment",
        "expedition_point",
        "series",
        "l10n_latam_document_type_id",
    )
    def _compute_display_name(self):
        """Formato de visualización del timbrado"""
        for record in self:
            doc_type_name = (
                record.l10n_latam_document_type_id.name
                if record.l10n_latam_document_type_id
                else ""
            )
            name = (
                f"Timbrado {record.name} "
                f"({record.establishment}-{record.expedition_point})"
            )
            if record.series and record.series != "AA":
                name = f"{name} Serie {record.series}"
            if doc_type_name:
                name = f"{name} [{doc_type_name}]"
            record.display_name = name

    def check_validity(self):
        """Verifica si el timbrado es válido en la fecha actual"""
        self.ensure_one()
        today = date.today()

        if not self.active:
            raise ValidationError(_("El timbrado está inactivo."))

        if today < self.date_from:
            raise ValidationError(_("El timbrado aún no ha entrado en vigencia."))

        if today > self.date_to:
            raise ValidationError(_("El timbrado ha vencido."))

        return True

    def check_number_available(self, number, exclude_move_id=False):
        """Verifica si un número está disponible en este timbrado"""
        self.ensure_one()

        if number < self.invoice_number_from or number > self.invoice_number_to:
            raise ValidationError(
                _(
                    "El número %(number)s está fuera del rango autorizado "
                    "(%(from)s - %(to)s)."
                )
                % {
                    "number": number,
                    "from": self.invoice_number_from,
                    "to": self.invoice_number_to,
                }
            )

        # Verificar si el número ya fue utilizado
        domain = [
            ("l10n_py_authorization_id", "=", self.id),
            ("l10n_py_invoice_number", "=", number),
        ]
        if exclude_move_id:
            domain.append(("id", "!=", exclude_move_id))

        existing = self.env["account.move"].search(domain)

        if existing:
            raise ValidationError(
                _(
                    "El número %(number)s ya ha sido utilizado en la factura "
                    "%(invoice_name)s."
                )
                % {
                    "number": number,
                    "invoice_name": existing[0].name,
                }
            )

        return True
