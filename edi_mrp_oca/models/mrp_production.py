# Copyright 2026 ForgeFlow S.L. (http://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MrpProduction(models.Model):
    _name = "mrp.production"
    _inherit = ["mrp.production", "edi.exchange.consumer.mixin"]
