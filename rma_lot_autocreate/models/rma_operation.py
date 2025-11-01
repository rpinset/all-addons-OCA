# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class RmaOperation(models.Model):

    _inherit = "rma.operation"

    auto_create_lot = fields.Boolean(
        string="Auto-create Lot/Serial on Confirm",
        help=(
            "If enabled, and the product is tracked and no lot/serial is set on the RMA, "
            "a new lot/serial will be created at confirmation."
        ),
    )
    lot_sequence_id = fields.Many2one(
        "ir.sequence",
        string="Lot/Serial Name Sequence",
        domain=[("code", "like", "rma.lot%")],
        help="Sequence used to generate names for auto-created lots/serials.",
    )
    lot_expiration_days = fields.Integer(
        string="Lot Expiration (days)",
        help="If set, the lot expiration date will be set to "
        "Confirm Date + this many days.",
    )
    lot_removal_days_before_expiration = fields.Integer(
        string="Removal Days Before Expiration",
        help="If set, the lot removal date will be expiration date minus this many days."
        " Requires an expiration to be configured.",
    )

    @api.constrains("auto_create_lot", "lot_sequence_id")
    def _check_lot_sequence_required(self):
        for rec in self:
            if rec.auto_create_lot and not rec.lot_sequence_id:
                raise ValidationError(
                    _(
                        "You must set a Lot/Serial Name Sequence when Auto-create "
                        "Lot/Serial is enabled."
                    )
                )

    @api.constrains("lot_expiration_days", "lot_removal_days_before_expiration")
    def _check_days(self):
        for rec in self:
            if rec.lot_expiration_days < 0:
                raise ValidationError(
                    _("Expiration days must be greater than or equal to 0.")
                )
            if rec.lot_removal_days_before_expiration < 0:
                raise ValidationError(
                    _(
                        "Removal days before expiration must be greater than or equal to 0."
                    )
                )
            if rec.lot_removal_days_before_expiration and rec.lot_expiration_days == 0:
                raise ValidationError(
                    _(
                        "To set a removal date before expiration, you must configure "
                        "a positive expiration (days)."
                    )
                )
