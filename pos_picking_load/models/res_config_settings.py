# Copyright (C) 2026 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_iface_load_picking = fields.Boolean(
        related="pos_config_id.iface_load_picking", readonly=False
    )

    pos_iface_load_picking_max_qty = fields.Integer(
        related="pos_config_id.iface_load_picking_max_qty", readonly=False
    )
