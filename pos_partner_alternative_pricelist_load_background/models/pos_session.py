# Copyright 2024 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class POSSession(models.Model):
    _inherit = "pos.session"

    def get_pos_ui_partner_pricelist_background(self, pricelist_id, product_ids):
        pricelists = super().get_pos_ui_partner_pricelist_background(
            pricelist_id, product_ids
        )
        # By design we do not calculate alternative prices on base pricelits
        if self.env.context.get("base_pricelist"):
            return pricelists
        pricelist_rec = self.env["product.pricelist"].browse(pricelist_id)
        alternative_pricelists = []
        for alt_pricelist_rec in pricelist_rec.alternative_pricelist_ids:
            alternative_pricelists += self.get_pos_ui_partner_pricelist_background(
                alt_pricelist_rec.id, product_ids
            )
        if alternative_pricelists:
            return pricelists + alternative_pricelists
        return pricelists
