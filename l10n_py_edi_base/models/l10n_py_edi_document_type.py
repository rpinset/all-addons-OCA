# l10n_py_edi_base/models/l10n_py_edi_document_type.py

from odoo import fields, models


class EDIDocumentType(models.Model):
    """Tipos de Documentos Electrónicos"""

    _name = "l10n_py.edi.document.type"
    _description = "Tipo de Documento Electrónico"
    _order = "code"

    code = fields.Char(string="Código", required=True, size=2)
    name = fields.Char(string="Nombre", required=True, translate=True)
    description = fields.Text(string="Descripción", translate=True)

    _sql_constraints = [
        (
            "code_unique",
            "unique(code)",
            "El código del tipo de documento debe ser único",
        )
    ]
