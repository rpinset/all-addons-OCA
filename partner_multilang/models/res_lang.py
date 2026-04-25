# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class Lang(models.Model):
    _inherit = "res.lang"

    transliterate = fields.Boolean()
