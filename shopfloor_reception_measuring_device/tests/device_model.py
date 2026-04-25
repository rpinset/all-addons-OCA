# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class MeasuringModel(models.Model):
    _inherit = "measuring.device"

    device_type = fields.Selection(selection_add=[("testdevice", "TestDevice")])
