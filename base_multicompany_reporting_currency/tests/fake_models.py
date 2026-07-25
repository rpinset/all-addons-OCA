# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


# For testing ``multicompany.reporting.currency.mixin`` features on new models
class FakeModel(models.Model):
    _name = "fake.model"
    _description = "Fake Model"
    _inherit = "multicompany.reporting.currency.mixin"
