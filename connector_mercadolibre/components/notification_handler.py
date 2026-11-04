# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class MercadoLibreNotificationHandler(Component):
    """Fallback handler. A topic handler sets ``_topic`` in another addon.

    ``_apply_on`` is an Odoo model. The Mercado Libre topic is not a model,
    so dispatch matches ``_topic`` instead.
    """

    _name = "mercadolibre.notification.handler"
    _inherit = "mercadolibre.backend.component"
    _usage = "notification.handler"
    _apply_on = "mercadolibre.notification"
    _topic = None

    def handle(self):
        self.work.notification.write({"state": "skipped", "error_message": False})
