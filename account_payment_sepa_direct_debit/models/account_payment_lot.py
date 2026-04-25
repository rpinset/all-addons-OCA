# Copyright 2025 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models


class AccountPaymentLot(models.Model):
    _inherit = "account.payment.lot"

    sequence_type = fields.Selection(
        [("RCUR", "Recurring"), ("FNAL", "Final"), ("OOFF", "One-Off")],
    )
    mandate_required = fields.Boolean(
        related="order_id.payment_method_id.mandate_required"
    )

    # mandate scheme is copied in local_instrument
    @api.model
    def _local_instrument_selection(self):
        res = super()._local_instrument_selection()
        res += [("CORE", _("CORE Mandate")), ("B2B", _("B2B Mandate"))]
        return res
