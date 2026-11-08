# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class MercadoLibreProductBinder(Component):
    """Bind a Mercado Libre item, including one row per variation."""

    _name = "mercadolibre.product.binder"
    _inherit = "mercadolibre.binder"
    _apply_on = "mercadolibre.product.product"

    def to_internal(self, external_id, unwrap=False, variation_id=False):
        """Return the binding for an item id and an optional variation.

        ``variation_id`` is empty for an item that has no variations. The
        same item id is stored on every variation, so the search has to
        include it or ``ensure_one`` would fail.
        """
        context = self.env.context
        bindings = self.model.with_context(active_test=False).search(
            [
                (self._external_field, "=", external_id),
                (self._backend_field, "=", self.backend_record.id),
                ("variation_id", "=", variation_id or False),
            ]
        )
        if not bindings:
            if unwrap:
                return self.model.browse()[self._odoo_field]
            return self.model.browse()
        bindings.ensure_one()
        if unwrap:
            bindings = bindings[self._odoo_field]
        return bindings.with_context(**context)
