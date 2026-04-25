# Copyright 2021 Camptocamp SA (http://www.camptocamp.com)
# Copyright 2025 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.addons.component.core import Component


class PackingAction(Component):
    """Provide methods to work with packing operations."""

    _name = "shopfloor.packing.action"
    _inherit = "shopfloor.process.action"
    _usage = "packing"

    def package_type_valid_for_carrier(self, package_type, carrier):
        return package_type.package_carrier_type in (
            "none",
            carrier.delivery_type,
        )

    def create_delivery_package(self, carrier):
        default_package_type = self._get_default_package_type(carrier)
        return self.create_package_from_package_type(default_package_type)

    def _get_default_package_type(self, carrier):
        # TODO: refactor `delivery_[carrier_name]` modules
        # to have always the same field named `default_package_type_id`
        # to unify lookup of this field.
        # As alternative add a computed field.
        # AFAIS there's no reason to have 1 field per carrier type.
        fname = carrier.delivery_type + "_default_package_type_id"
        if fname not in carrier._fields:
            return self.env["stock.package.type"].browse()
        return carrier[fname]

    def create_package_from_package_type(self, package_type=None):
        if package_type:
            vals = self._package_vals_from_package_type(package_type)
        else:
            vals = self._package_vals_without_package_type()
        return self.env["stock.quant.package"].create(vals)

    def _package_vals_from_package_type(self, package_type):
        return {
            "package_type_id": package_type.id,
            "pack_length": package_type.packaging_length,
            "width": package_type.width,
            "height": package_type.height,
        }

    def _package_vals_without_package_type(self):
        return {}

    def package_has_several_products(self, package):
        return len(package.quant_ids.product_id) > 1

    def package_has_several_lots(self, package):
        return len(package.quant_ids.lot_id) > 1

    def is_complete_mix_pack(self, package):
        """Check if a package is mixed and completely reserved.

        Will return true if the package has multiple distinct products and
        all the package quantities are reserved.
        """
        return self.package_has_several_products(package) and all(
            quant.quantity == quant.reserved_quantity for quant in package.quant_ids
        )
