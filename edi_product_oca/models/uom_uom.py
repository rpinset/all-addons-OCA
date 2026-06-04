# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class UomUom(models.Model):
    _name = "uom.uom"
    _inherit = ["uom.uom", "edi.exchange.consumer.mixin"]
