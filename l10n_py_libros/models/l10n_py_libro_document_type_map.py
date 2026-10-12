# l10n_py_libros/models/l10n_py_libro_document_type_map.py

from odoo import fields, models


class L10nPyLibroDocumentTypeMap(models.Model):
    """Mapeamento Tabla 4 DNIT (codigo_tabla4) <-> l10n_latam.document.type.

    Modelo dedicado: nunca reaproveita o campo ``code`` existente de
    ``l10n_latam.document.type`` (numeração SIFEN 1/4/5/6/7, incompatível com
    a Tabla 4 da DNIT, 101-112/201-211).
    """

    _name = "l10n_py.libro.document.type.map"
    _description = "Mapeamento Tabla 4 DNIT - Tipo de Comprobante"
    _order = "codigo_tabla4"

    name = fields.Char(string="Descripción", required=True)
    codigo_tabla4 = fields.Char(string="Código Tabla 4", required=True, size=3)
    l10n_latam_document_type_id = fields.Many2one(
        "l10n_latam.document.type",
        string="Tipo de Documento LATAM",
        help="Vacío para tipos 'de papel' sem equivalente LATAM",
    )
    aplica_ventas = fields.Boolean(default=False)
    aplica_compras = fields.Boolean(default=False)
    aplica_ingresos = fields.Boolean(default=False)
    aplica_egresos = fields.Boolean(default=False)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "codigo_tabla4_unique",
            "unique(codigo_tabla4)",
            "El código Tabla 4 debe ser único.",
        ),
    ]

    def _get_codigos_for_tipo_registro(self, tipo_registro):
        """Return list of codigo_tabla4 applicable to a given tipo_registro."""
        field_name = f"aplica_{tipo_registro}"
        maps = self.with_context(active_test=False).search([(field_name, "=", True)])
        return maps.mapped("codigo_tabla4")
