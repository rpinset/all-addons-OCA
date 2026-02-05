# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

from .res_users import check_authentication


class TierValidation(models.AbstractModel):
    _inherit = "tier.validation"

    require_authentication = fields.Boolean(compute="_compute_require_authentication")

    def _compute_require_authentication(self):
        for rec in self:
            require_authentication = rec.review_ids.filtered(
                lambda r: r.status in ("waiting", "pending")
                and (self.env.user in r.reviewer_ids)
            ).mapped("require_authentication")
            rec.require_authentication = True in require_authentication

    def validate_tier(self):
        self.ensure_one()
        if not self.has_comment and self.require_authentication:
            return self._validate_tier_with_identity_check()
        return super().validate_tier()

    def reject_tier(self):
        self.ensure_one()
        if not self.has_comment and self.require_authentication:
            return self._reject_tier_with_identity_check()
        return super().reject_tier()

    @check_authentication
    def _validate_tier_with_identity_check(self):
        return super().validate_tier()

    @check_authentication
    def _reject_tier_with_identity_check(self):
        return super().reject_tier()
