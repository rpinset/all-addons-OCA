# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class MessageAction(Component):
    _inherit = "shopfloor.message.action"

    def package_type_not_found(self):
        return {
            "message_type": "error",
            "body": self.env._("The package type could not be found"),
        }

    def package_type_changed(self):
        return {
            "message_type": "success",
            "body": self.env._("The package type was successfully changed"),
        }

    def package_type_not_valid(self):
        return {
            "message_type": "error",
            "body": self.env._("The package type is not valid"),
        }
