# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models

from ..models.res_users import check_authentication


class CommentWizard(models.TransientModel):
    _inherit = "comment.wizard"

    def add_comment(self):
        if any(review.require_authentication for review in self.review_ids):
            return self._add_comment_with_identity_check()
        return super().add_comment()

    @check_authentication
    def _add_comment_with_identity_check(self):
        return super().add_comment()
