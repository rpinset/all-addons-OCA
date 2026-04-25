# Copyright 2019 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    voxel_send_mode = fields.Selection(
        related="company_id.voxel_send_mode", readonly=False
    )
    voxel_sent_time = fields.Float(related="company_id.voxel_sent_time", readonly=False)
    voxel_delay_time = fields.Float(
        related="company_id.voxel_delay_time", readonly=False
    )
    voxel_enabled = fields.Boolean(related="company_id.voxel_enabled", readonly=False)
    voxel_login_name = fields.Char(
        related="company_id.voxel_login_ids.name",
        readonly=False,
    )
    voxel_login_url = fields.Char(
        related="company_id.voxel_login_ids.url",
        readonly=False,
    )
    voxel_login_user = fields.Char(
        related="company_id.voxel_login_ids.user",
        readonly=False,
    )
    voxel_login_password = fields.Char(
        related="company_id.voxel_login_ids.password", readonly=False
    )
