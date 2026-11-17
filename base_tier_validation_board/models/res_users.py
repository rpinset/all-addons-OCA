# Copyright 2026 OCA / @bosd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Users(models.Model):
    _inherit = "res.users"

    @api.model
    def tier_review_dashboard_action(self):
        """Expose the Tier Reviews dashboard as the destination of the
        systray's "Show all reviews" footer link.

        The base module ships ``tier_review_dashboard_action`` as a stub
        returning ``False`` so the systray omits the link when no
        dashboard module is installed. When this module is installed,
        we point the link at the all-reviews kanban gated by
        ``group_show_tier_review_board``.
        """
        action = self.env.ref(
            "base_tier_validation_board.open_boards_tier_reviews",
            raise_if_not_found=False,
        )
        if not action:
            return False
        # Only expose the link to users who can actually see the
        # dashboard menu in the first place. Otherwise the link would
        # take them to an action that immediately errors with an
        # AccessError.
        if not self.env.user.has_group(
            "base_tier_validation_board.group_show_tier_review_board"
        ):
            return False
        return action.read()[0]
