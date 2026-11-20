# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class UomUom(models.Model):
    _inherit = "uom.uom"

    l10n_py_sifende_unidad_medida = fields.Integer(
        string="Código de unidad de medida SIFEN",
        default=77,
        help="Código del catálogo de unidades de medida de SIFEN (77 = Unidad).",
    )
