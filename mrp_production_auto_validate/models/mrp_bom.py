# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    mo_auto_validation = fields.Boolean(
        string="Order Auto Validation",
        help=(
            "Validate automatically the manufacturing order "
            "when the 'Pick Components' transfer is validated.\n"
            "This behavior is available only if the warehouse is configured "
            "with 2 or 3 steps."
        ),
        default=False,
    )

    @api.onchange("type")
    def onchange_type_auto_validation(self):
        if self.type != "normal":
            self.mo_auto_validation = False
