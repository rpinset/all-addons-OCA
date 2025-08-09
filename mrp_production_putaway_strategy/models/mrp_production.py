# Copyright 2017-18 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    @api.model_create_multi
    def create(self, vals_list):
        putaway_applied_flags = []

        for vals in vals_list:
            product = self.env["product.product"].browse(vals.get("product_id"))
            original_location = self.env["stock.location"].browse(
                vals.get("location_dest_id")
            )
            putaway_location = original_location._get_putaway_strategy(product)
            putaway_flag = False

            if putaway_location.id != original_location.id:
                vals["location_dest_id"] = putaway_location.id
                putaway_flag = True

            putaway_applied_flags.append(putaway_flag)

        mos = super().create(vals_list)

        for mo, applied in zip(mos, putaway_applied_flags, strict=False):
            if applied:
                mo.message_post(
                    body=_(
                        "Applied Putaway strategy to finished products.\n"
                        "Finished Products Location: %s."
                    )
                    % mo.location_dest_id.complete_name,
                    message_type="comment",
                )

        return mos
