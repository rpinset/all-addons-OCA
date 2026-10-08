# Copyright 2021 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    approver_id = fields.Many2one(
        "res.users",
        string="Responsible for Approval",
        compute="_compute_approver_id",
        readonly=False,
        store=True,
    )

    @api.depends("partner_id")
    def _compute_approver_id(self):
        for rec in self:
            if rec.approver_id:
                # assign a value in any case
                rec.approver_id = rec.approver_id
            elif rec.partner_id.approver_id:
                rec.approver_id = rec.partner_id.approver_id
            else:
                rec.approver_id = False

    def _get_under_validation_exceptions(self):
        # `made_sequence_gap` is a technical field that account.move recomputes
        # as a side effect (date -> highest_name -> name -> _update_sequence_made_gap).
        # In v19 this recompute can be flushed while the move is under validation,
        # so it must be allowed to avoid blocking unrelated technical writes.
        return super()._get_under_validation_exceptions() + ["made_sequence_gap"]

    def _post(self, soft=True):
        for move in self:
            require_approver_in_vendor_bills = (
                move.company_id.require_approver_in_vendor_bills
            )
            if (
                move.is_purchase_document(include_receipts=True)
                and require_approver_in_vendor_bills
                and not move.approver_id
            ):
                raise UserError(
                    self.env._(
                        "It is mandatory to indicate a Responsible for"
                        " Approval (in %s)",
                        move.name,
                    )
                )
        return super()._post(soft)
