from odoo import fields, models


class TierValidationTester(models.Model):
    _inherit = "tier.validation.tester"
    _rec_name = "name"

    name = fields.Char()
