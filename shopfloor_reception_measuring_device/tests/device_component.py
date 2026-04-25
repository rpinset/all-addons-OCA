# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.addons.component.core import Component


class MeasuringComponent(Component):
    _name = "device.component.testdevice"
    _inherit = "measuring.device.base"
    _usage = "testdevice"
