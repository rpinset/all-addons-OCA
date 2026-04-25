# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

from odoo.addons.point_of_sale.models.pos_category import (
    PosCategory as OriginalPosCategory,
)


class PosCategory(models.Model):
    _inherit = "pos.category"
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = "complete_name"

    complete_name = fields.Char(
        compute="_compute_complete_name", recursive=True, store=True
    )

    parent_path = fields.Char(index=True, unaccent=False)

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = "%s / %s" % (
                    category.parent_id.complete_name,
                    category.name,
                )
            else:
                category.complete_name = category.name


# Disable the definition of pos.category name_get function
# and fallback in the default function.
OriginalPosCategory.name_get = models.BaseModel.name_get
