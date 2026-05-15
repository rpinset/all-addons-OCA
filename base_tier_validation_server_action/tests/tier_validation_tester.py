# Copyright 2020 Ecosoft (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TierValidationTester(models.Model):
    _inherit = "tier.validation.tester"

    test_bool = fields.Boolean()

    def _get_under_validation_exceptions(self):
        return super()._get_under_validation_exceptions() + ["test_bool"]
