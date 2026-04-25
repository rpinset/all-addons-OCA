# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    crowdfunding_public = fields.Boolean("Show on website")
