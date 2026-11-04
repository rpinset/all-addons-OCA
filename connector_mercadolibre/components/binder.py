# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import AbstractComponent


class MercadoLibreBinder(AbstractComponent):
    """Binder shell. Concrete binders set ``_apply_on`` to a binding model."""

    _name = "mercadolibre.binder"
    _inherit = ["mercadolibre.backend.component", "base.binder"]
    _usage = "binder"
    _external_field = "external_id"
    _backend_field = "backend_id"
