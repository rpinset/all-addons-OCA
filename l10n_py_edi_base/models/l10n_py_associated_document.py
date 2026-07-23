# l10n_py_edi_base/models/l10n_py_associated_document.py

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AssociatedDocument(models.Model):
    """Documento Asociado (Grupo H del SIFEN v150).

    Permite vincular documentos de referencia a facturas electrónicas:
    - Electrónico: referencia por CDC (44 dígitos)
    - Impreso: referencia por timbrado/establecimiento/punto/número
    - Constancia Electrónica: tipo y número de constancia
    """

    _name = "l10n_py.associated.document"
    _description = "Documento Asociado (Grupo H SIFEN)"
    _order = "id"

    move_id = fields.Many2one(
        "account.move",
        string="Factura",
        required=True,
        ondelete="cascade",
        index=True,
    )

    association_type = fields.Selection(
        [
            ("1", "Electrónico"),
            ("2", "Impreso"),
            ("3", "Constancia Electrónica"),
        ],
        string="Tipo de Asociación (H002)",
        required=True,
    )

    # === Electrónico (H004) ===
    cdc = fields.Char(
        string="CDC",
        size=44,
        help="Código de Control del Documento Electrónico (44 dígitos)",
    )

    # === Impreso (H005-H012) ===
    timbrado = fields.Char(
        size=8,
        help="Número de timbrado del documento impreso (H005)",
    )

    establishment = fields.Char(
        string="Establecimiento",
        size=3,
        help="Código de establecimiento (H006)",
    )

    expedition_point = fields.Char(
        string="Punto de Expedición",
        size=3,
        help="Punto de expedición (H007)",
    )

    doc_number = fields.Char(
        string="Número de Documento",
        size=7,
        help="Número del documento (H008)",
    )

    doc_type_code = fields.Selection(
        [
            ("1", "Factura"),
            ("2", "Nota de crédito"),
            ("3", "Nota de débito"),
            ("4", "Nota de remisión"),
            ("5", "Comprobante de retención"),
        ],
        string="Tipo de Documento Impreso (H009)",
    )

    doc_date = fields.Date(
        string="Fecha del Documento (H010)",
    )

    # === Constancia Electrónica (H011-H012) ===
    constancia_type = fields.Selection(
        [
            ("1", "Constancia de no ser contribuyente"),
            ("2", "Constancia de microproductor"),
        ],
        string="Tipo de Constancia (H011)",
    )

    constancia_number = fields.Char(
        string="Número de Constancia (H012)",
        size=20,
    )

    # ============== CONSTRAINTS ==============

    @api.constrains("association_type", "cdc")
    def _check_electronic_fields(self):
        """Electrónico requiere CDC; impreso/constancia no permiten CDC."""
        for rec in self:
            if rec.association_type == "1":
                if not rec.cdc:
                    raise ValidationError(
                        _("Documento electrónico: el CDC es obligatorio.")
                    )
                if rec.cdc and (len(rec.cdc) != 44 or not rec.cdc.isdigit()):
                    raise ValidationError(
                        _("El CDC debe contener exactamente 44 dígitos " "numéricos.")
                    )
            else:
                if rec.cdc:
                    raise ValidationError(
                        _("Solo documentos electrónicos pueden tener CDC.")
                    )

    @api.constrains(
        "association_type",
        "timbrado",
        "establishment",
        "expedition_point",
        "doc_number",
        "doc_type_code",
        "doc_date",
    )
    def _check_printed_fields(self):
        """Impreso requiere todos los campos; electrónico/constancia no permiten."""
        printed_fields = {
            "timbrado": "Timbrado",
            "establishment": "Establecimiento",
            "expedition_point": "Punto de Expedición",
            "doc_number": "Número de Documento",
            "doc_type_code": "Tipo de Documento",
            "doc_date": "Fecha del Documento",
        }
        for rec in self:
            if rec.association_type == "2":
                missing = [
                    label
                    for field_name, label in printed_fields.items()
                    if not getattr(rec, field_name)
                ]
                if missing:
                    raise ValidationError(
                        _(
                            "Documento impreso: campos obligatorios "
                            "faltantes: %(fields)s",
                            fields=", ".join(missing),
                        )
                    )
            elif rec.association_type in ("1", "3"):
                has_printed = any(
                    getattr(rec, f) for f in printed_fields if f != "doc_date"
                )
                if has_printed:
                    raise ValidationError(
                        _(
                            "Documentos electrónicos o constancias no "
                            "pueden tener campos de documento impreso."
                        )
                    )

    @api.constrains("association_type", "constancia_type", "constancia_number")
    def _check_constancia_fields(self):
        """Constancia requiere tipo y número; otros tipos no permiten."""
        for rec in self:
            if rec.association_type == "3":
                if not rec.constancia_type or not rec.constancia_number:
                    raise ValidationError(
                        _("Constancia electrónica: tipo y número son " "obligatorios.")
                    )
            else:
                if rec.constancia_type or rec.constancia_number:
                    raise ValidationError(
                        _(
                            "Solo constancias electrónicas pueden tener "
                            "tipo y número de constancia."
                        )
                    )
