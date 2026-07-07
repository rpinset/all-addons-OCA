# Copyright 2026 TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    signature = fields.Binary(
        copy=False,
        attachment=True,
        help="Signature received through the Field Service order.",
    )
    signed_by = fields.Char(
        copy=False,
        help="Name of the person that signed the Field Service order.",
    )
    signed_on = fields.Datetime(
        copy=False,
        help="Date and time the Field Service order was signed.",
    )

    @api.onchange("signature")
    def _onchange_signature(self):
        for order in self:
            if order.signature and not order.signed_on:
                order.signed_on = fields.Datetime.now()
