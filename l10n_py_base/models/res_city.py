# l10n_py_base/models/res_city.py

from odoo import fields, models


class City(models.Model):
    """Extensión de res.city para Paraguay con código SET.

    Este objeto extiende res.city para incluir el código SET
    (Subsecretaría de Estado de Tributación) necesario para
    documentos fiscales en Paraguay.
    """

    _inherit = "res.city"

    l10n_py_code = fields.Char(
        string="Código SET",
        size=4,
        help=(
            "Código de la ciudad según SET " "(Subsecretaría de Estado de Tributación)"
        ),
    )

    _sql_constraints = [
        (
            "l10n_py_code_unique",
            "unique(l10n_py_code, country_id)",
            "El código SET de la ciudad debe ser único por país",
        )
    ]
