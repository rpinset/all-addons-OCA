# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    # NOTE: Field defined in `agreement_helpdesk_mgmt`, make it computed
    agreement_id = fields.Many2one(
        compute="_compute_agreement_id",
        store=True,
        readonly=False,
    )

    @api.depends("sale_order_ids.agreement_id")
    def _compute_agreement_id(self):
        # pylint: disable=missing-return
        if hasattr(super(), "_compute_agreement_id"):
            super()._compute_agreement_id()
        for ticket in self:
            if (
                not ticket.agreement_id
                and len(agreement := ticket.sale_order_ids.agreement_id) == 1
            ):
                ticket.agreement_id = agreement

    @api.constrains("sale_order_ids", "agreement_id")
    def _check_unique_agreement(self):
        for ticket in self:
            agreements = ticket.mapped("sale_order_ids.agreement_id")
            if len(agreements) > 1:
                raise ValidationError(
                    self.env._(
                        "Ticket '%s' cannot have multiple different agreements.",
                        ticket.name,
                    )
                )
