# l10n_py_base/models/l10n_py_neighborhood.py

from odoo import fields, models


class Neighborhood(models.Model):
    """Modelo de Barrio para Paraguay"""

    _name = "l10n_py.neighborhood"
    _description = "Barrio"
    _order = "name"

    name = fields.Char(
        string="Nombre",
        required=True,
        help="Nombre del barrio",
    )

    code = fields.Char(
        string="Código",
        help="Código del barrio",
    )

    city_id = fields.Many2one(
        "res.city",
        string="Ciudad",
        required=True,
        ondelete="cascade",
        help="Ciudad a la que pertenece el barrio",
    )

    state_id = fields.Many2one(
        "res.country.state",
        string="Departamento",
        related="city_id.state_id",
        store=True,
        readonly=True,
        help="Departamento al que pertenece el barrio",
    )

    country_id = fields.Many2one(
        "res.country",
        string="País",
        related="city_id.country_id",
        store=True,
        readonly=True,
        help="País al que pertenece el barrio",
    )

    zipcode = fields.Char(
        string="Código Postal",
        help="Código postal del barrio",
    )
