# Copyright 2025 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class StockReleaseChannel(models.Model):
    _inherit = "stock.release.channel"

    country_ids = fields.Many2many("res.country", string="Countries")
    state_ids = fields.Many2many("res.country.state", string="States")
