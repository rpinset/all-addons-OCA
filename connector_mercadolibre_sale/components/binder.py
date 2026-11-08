# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import AbstractComponent, Component


class MercadoLibreIdBinder(AbstractComponent):
    """Lookup of one external id. Concrete binders set ``_apply_on``."""

    _name = "mercadolibre.id.binder"
    _inherit = "mercadolibre.binder"

    def to_internal(self, external_id, unwrap=False):
        context = self.env.context
        bindings = self.model.with_context(active_test=False).search(
            [
                (self._external_field, "=", str(external_id)),
                (self._backend_field, "=", self.backend_record.id),
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


class MercadoLibreSaleBinder(Component):
    _name = "mercadolibre.sale.binder"
    _inherit = "mercadolibre.id.binder"
    _apply_on = "mercadolibre.sale.order"


class MercadoLibrePartnerBinder(Component):
    _name = "mercadolibre.partner.binder"
    _inherit = "mercadolibre.id.binder"
    _apply_on = "mercadolibre.res.partner"


class MercadoLibreShipmentBinder(Component):
    _name = "mercadolibre.shipment.binder"
    _inherit = "mercadolibre.binder"
    _apply_on = "mercadolibre.shipment"

    def to_internal(self, external_id, unwrap=False):
        binding = self.model.with_context(active_test=False).search(
            [
                (self._external_field, "=", str(external_id)),
                (self._backend_field, "=", self.backend_record.id),
            ],
            limit=1,
        )
        if unwrap:
            return binding.picking_id
        return binding
