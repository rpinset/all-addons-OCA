# Copyright 2025 Patryk Pyczko (APSL-Nagarro)<ppyczko@apsl.net>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"

    @api.model
    def _get_compatible_acquirers(self, *args, website_id=None, **kwargs):
        """
        Override to filter acquirers based on the partner's allowed acquirers.

        This method first fetches acquirers based on general criteria, then
        filters them by the partner's allowed acquirers list.

        :param int website_id: The provided website, as a `website` id
        :return: The filtered list of compatible acquirers.
        :rtype: recordset of `payment.acquirer`
        """
        acquirers = super()._get_compatible_acquirers(
            *args, website_id=website_id, **kwargs
        )

        allowed_acquirers = self.env.user.partner_id.allowed_acquirer_ids
        return (
            acquirers.filtered(lambda acq: acq in allowed_acquirers)
            if allowed_acquirers
            else acquirers
        )
