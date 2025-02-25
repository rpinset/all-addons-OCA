# Copyright 2022 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class StockRoute(models.Model):
    _inherit = "stock.route"

    mo_component_selectable = fields.Boolean(string="Selectable on MO Components")
