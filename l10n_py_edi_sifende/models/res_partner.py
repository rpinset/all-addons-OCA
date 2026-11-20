# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_py_sifende_city_id = fields.Many2one(
        "l10n_py.sifende.city",
        string="Ciudad SIFEN",
        help="Sólo hace falta si Sifende no reconoce la ciudad del contacto: "
        "se envía esta en lugar de deducirla del nombre.",
    )
