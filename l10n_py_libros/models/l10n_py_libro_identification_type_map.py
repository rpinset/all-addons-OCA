# l10n_py_libros/models/l10n_py_libro_identification_type_map.py

from odoo import fields, models

# l10n_py_base ``l10n_py_doc_type`` -> kind of the Tabla 3 mapping
_DOC_TYPE_KIND = {
    "1": "ci",
    "2": "passport",
    "3": "residence",
    "4": "unnamed",
}


class L10nPyLibroIdentificationTypeMap(models.Model):
    """Mapeamento Tabla 3 DNIT <-> tipo de identificación del contacto.

    Odoo 20 removed ``l10n_latam_base`` (and its identification types): the
    kind of identification is now derived from the partner (RUC in ``vat`` for
    Paraguayan partners, ``l10n_py_doc_type`` of ``l10n_py_base`` for identity
    documents, any other tax number as foreign tax id).
    """

    _name = "l10n_py.libro.identification.type.map"
    _description = "Mapeamento Tabla 3 DNIT - Tipo de Identificación"
    _order = "codigo_tabla3"

    partner_doc_kind = fields.Selection(
        [
            ("ruc", "RUC"),
            ("ci", "Cédula de Identidad"),
            ("passport", "Pasaporte"),
            ("residence", "Carnet de Residencia"),
            ("unnamed", "Sin Nombre"),
            ("diplomatic", "Diplomático"),
            ("foreign_tax", "Identificación Tributaria (extranjero)"),
        ],
        required=True,
    )
    codigo_tabla3 = fields.Char(string="Código Tabla 3", required=True, size=2)
    active = fields.Boolean(default=True)

    _partner_doc_kind_unique = models.Constraint(
        "unique(partner_doc_kind)",
        "Cada tipo de identificación só pode ter um mapeamento Tabla 3.",
    )

    def _get_partner_doc_kind(self, partner):
        """Return the Tabla 3 kind of the identification of ``partner``."""
        py = self.env.ref("base.py")
        if partner.vat and partner.country_id == py:
            return "ruc"
        if partner.l10n_py_doc_type:
            return _DOC_TYPE_KIND.get(partner.l10n_py_doc_type)
        if partner.vat:
            return "foreign_tax"
        return False

    def _get_codigo(self, partner):
        kind = self._get_partner_doc_kind(partner)
        if not kind:
            return False
        rec = self.with_context(active_test=False).search(
            [("partner_doc_kind", "=", kind)],
            limit=1,
        )
        return rec.codigo_tabla3 if rec else False
