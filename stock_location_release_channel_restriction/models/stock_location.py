# Copyright 2024 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models

RELEASE_RESTRICTION = [
    (
        "mixed",
        "Movements of different release channels are allowed into the location",
    ),
    (
        "same",
        "Only movements of the same release channel are allowed into the location",
    ),
]


class StockLocation(models.Model):

    _inherit = "stock.location"

    release_channel_restriction = fields.Selection(
        selection=RELEASE_RESTRICTION,
        help="If 'same' is selected the system will prevent to put "
        "items of different release channels into the same location.",
        index=True,
        compute="_compute_release_channel_restriction",
        store=True,
        recursive=True,
    )

    parent_release_channel_restriction = fields.Selection(
        string="Parent Location Release Channel Restriction",
        store=True,
        readonly=True,
        related="location_id.release_channel_restriction",
        recursive=True,
    )

    specific_release_channel_restriction = fields.Selection(
        selection=RELEASE_RESTRICTION,
        default=False,
        help="If specified the restriction specified will apply to "
        "the current location and all its children",
    )
    release_channel_restriction_in_move = fields.Boolean(
        string="Release Channel Restriction For Incoming Moves",
        help="Check this box if you want to take into account all pending incoming movements"
        " to restrict the future movements to be in the same release channel.",
    )

    @api.model
    def _selection_release_channel_restriction(self):
        return [
            (
                "mixed",
                _(
                    "Movements of different release channels are allowed into the location"
                ),
            ),
            (
                "same",
                _(
                    "Only movements of the same release channel are allowed into the location"
                ),
            ),
        ]

    @api.depends(
        "specific_release_channel_restriction", "parent_release_channel_restriction"
    )
    def _compute_release_channel_restriction(self):
        default_value = "mixed"
        for rec in self:
            rec.release_channel_restriction = (
                rec.specific_release_channel_restriction
                or rec.parent_release_channel_restriction
                or default_value
            )
