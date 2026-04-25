# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.component.core import Component


class MessageAction(Component):
    _inherit = "shopfloor.message.action"

    def package_height_not_valid(self):
        return {
            "message_type": "error",
            "body": self.env._("The height is required and not valid"),
        }
