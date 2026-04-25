# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    pack_weight_in_kg = fields.Float(
        help="Technical field, to speed up comparaisons",
        compute="_compute_pack_weight_in_kg",
        store=True,
    )
    height_in_m = fields.Float(
        help="Technical field, to speed up comparaisons",
        compute="_compute_height_in_m",
        store=True,
    )
    height = fields.Float(compute="_compute_height", store=True, readonly=False)

    @api.depends("package_type_id", "product_packaging_id")
    def _compute_height(self):
        no_override = self.env.context.get("_auto_assign_packaging")
        for package in self:
            # Do not override package height when already set,
            # in the context of auto_assign_packaging
            if package.height and no_override:
                continue
            if package.product_packaging_id.height:
                package.height = package.product_packaging_id.height
            elif package.package_type_id:
                package.height = package.package_type_id.height
            else:
                package.height = 0.0

    @api.depends("pack_weight", "weight_uom_id")
    def _compute_pack_weight_in_kg(self):
        uom_kg = self.env.ref("uom.product_uom_kgm")
        for package in self:
            package.pack_weight_in_kg = package.weight_uom_id._compute_quantity(
                qty=package.pack_weight,
                to_unit=uom_kg,
                round=False,
            )

    @api.depends("height", "length_uom_id")
    def _compute_height_in_m(self):
        uom_meters = self.env.ref("uom.product_uom_meter")
        for package in self:
            package.height_in_m = package.length_uom_id._compute_quantity(
                qty=package.height,
                to_unit=uom_meters,
                round=False,
            )

    @api.constrains("height", "package_type_id", "product_packaging_id")
    def _check_package_type_height_required(self):
        for package in self:
            if package.package_type_id.height_required and not package.height:
                raise ValidationError(
                    _("The height is mandatory on package {}.").format(package.name)
                )
