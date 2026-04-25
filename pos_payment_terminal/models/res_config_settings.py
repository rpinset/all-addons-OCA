from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_iface_payment_terminal = fields.Boolean(
        related="pos_config_id.iface_payment_terminal",
        readonly=False,
    )
    pos_payment_terminal_hide_back_btn = fields.Boolean(
        related="pos_config_id.payment_terminal_hide_back_btn",
        readonly=False,
    )
