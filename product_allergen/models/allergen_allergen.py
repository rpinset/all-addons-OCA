# Copyright 2025 Tecnativa - Christian Ramos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AllergenAllergen(models.Model):
    _name = "allergen.allergen"
    _description = "Allergen"

    name = fields.Char(required=True, translate=True)
    image = fields.Image(string="Icon", max_width=128, max_height=128)
    active = fields.Boolean(default=True)
