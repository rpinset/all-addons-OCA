# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.addons.component.core import Component


class MessageAction(Component):
    _inherit = "shopfloor.message.action"

    def no_measuring_device_found(self):
        return {
            "message_type": "error",
            "body": self.env._("No measuring device found"),
        }

    def measuring_device_already_in_use(self, device):
        return {
            "message_type": "error",
            "body": self.env._(
                "Measuring device %(name)s already in use", name=device.name
            ),
        }

    def measuring_device_selected(self, device, packaging):
        return {
            "message_type": "success",
            "body": self.env._(
                (
                    "The device %(name)s has been reserved, "
                    "you can now measure packaging %(packaging)s"
                ),
                name=device.name,
                packaging=packaging.name,
            ),
        }

    def no_measuring_device_to_release(self, packaging):
        return {
            "message_type": "warning",
            "body": self.env._(
                "No measuring device to release from packaging %(packaging)s",
                packaging=packaging.name,
            ),
        }

    def measuring_device_released(self, packaging, device):
        return {
            "message_type": "success",
            "body": self.env._(
                "The device has %(device_name)s has been released "
                "from packaging %(packaging_name)s",
                device_name=device.name,
                packaging_name=packaging.name,
            ),
        }
