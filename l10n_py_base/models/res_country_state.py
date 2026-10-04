# l10n_py_base/models/res_country_state.py

from odoo import fields, models


class CountryState(models.Model):
    """Extensión de res.country.state para Paraguay (Departamentos).

    Este objeto extiende res.country.state para incluir el código SET
    (Subsecretaría de Estado de Tributación) necesario para documentos
    fiscales en Paraguay.
    """

    _inherit = "res.country.state"

    l10n_py_code = fields.Integer(
        string="Código SET",
        help=(
            "Código del departamento según SET (Subsecretaría de Estado de Tributación)"
        ),
    )

    _l10n_py_code_unique = models.Constraint(
        "unique(l10n_py_code, country_id)",
        "El código SET del departamento debe ser único por país",
    )
