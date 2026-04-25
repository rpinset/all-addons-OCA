from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    iface_payment_terminal = fields.Boolean(
        string="OCA Payment Terminal",
        help="A payment terminal is available on the Proxy",
    )
    payment_terminal_hide_back_btn = fields.Boolean(
        string="Hide Back Button",
        help="Prevent from returning to basket from payment "
        "screen as soon as a payment line exists",
        default=True,
    )
