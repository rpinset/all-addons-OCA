# l10n_py_edi_base/models/product_template.py

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # ============== CAMPOS EDI PARAGUAY ==============

    l10n_py_ncm_code = fields.Char(
        string="Código NCM", size=8, help="Nomenclatura Común del Mercosur (8 dígitos)"
    )

    l10n_py_unit_code = fields.Integer(
        string="Código Unidad de Medida",
        default=77,
        help="Código de unidad de medida según SET (77 = UNI - Unidad)",
    )
