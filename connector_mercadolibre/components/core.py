# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import AbstractComponent


class MercadoLibreBackendComponent(AbstractComponent):
    """Collection shared by every Mercado Libre component."""

    _name = "mercadolibre.backend.component"
    _inherit = "base.connector"
    _collection = "mercadolibre.backend"
