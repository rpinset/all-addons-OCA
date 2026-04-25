# Copyrght 2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    def _get_payment_terminal_selection(self):
        res = super()._get_payment_terminal_selection()
        res.append(("oca_payment_terminal", "OCA Payment Terminal"))
        return res

    oca_payment_terminal_mode = fields.Selection(
        [("card", "Card"), ("check", "Check")], string="Payment Mode", default="card"
    )
    oca_payment_terminal_id = fields.Char(
        string="Terminal Identifier",
        help=("The identifier of the terminal as known by the hardware proxy. "),
    )
    oca_fast_payment = fields.Boolean(
        string="Fast Payment",
        default=True,
    )

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        fields.extend(
            [
                "oca_payment_terminal_mode",
                "oca_payment_terminal_id",
                "oca_fast_payment",
            ]
        )
        return fields
