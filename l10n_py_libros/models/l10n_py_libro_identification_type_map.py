# l10n_py_libros/models/l10n_py_libro_identification_type_map.py

from odoo import fields, models


class L10nPyLibroIdentificationTypeMap(models.Model):
    """Mapeamento Tabla 3 DNIT <-> l10n_latam.identification.type."""

    _name = "l10n_py.libro.identification.type.map"
    _description = "Mapeamento Tabla 3 DNIT - Tipo de Identificación"
    _order = "codigo_tabla3"

    l10n_latam_identification_type_id = fields.Many2one(
        "l10n_latam.identification.type",
        string="Tipo de Identificación LATAM",
        required=True,
    )
    codigo_tabla3 = fields.Char(string="Código Tabla 3", required=True, size=2)
    active = fields.Boolean(default=True)

    _ident_type_unique = models.Constraint(
        "unique(l10n_latam_identification_type_id)",
        "Cada tipo de identificación só pode ter um mapeamento Tabla 3.",
    )

    def _get_codigo(self, identification_type):
        if not identification_type:
            return False
        rec = self.with_context(active_test=False).search(
            [("l10n_latam_identification_type_id", "=", identification_type.id)],
            limit=1,
        )
        return rec.codigo_tabla3 if rec else False
