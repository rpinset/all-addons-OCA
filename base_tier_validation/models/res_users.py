# Copyright 2019 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models, modules
from odoo.exceptions import AccessError
from odoo.fields import Domain

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = "res.users"

    review_ids = fields.Many2many(
        string="Reviews", comodel_name="tier.review", copy=False
    )

    @api.model
    def review_user_count(self):
        user_reviews = {}
        user = self.env.user
        user.review_ids._update_review_status()
        domain = (
            Domain("status", "=", "pending")
            & Domain("can_review", "=", True)
            & Domain("id", "in", user.review_ids.ids)
        )
        review_groups = self.env["tier.review"]._read_group(
            domain=domain,
            groupby=["model"],
            aggregates=["id:recordset"],
        )
        for model, tier_review in review_groups:
            Model = self.env[model]
            # Skip Models not having Tier Validation enabled (example: was unistalled)
            if tier_review and hasattr(Model, "can_review"):
                records_domain = (
                    Domain("id", "in", tier_review.mapped("res_id"))
                    & Domain("validation_status", "!=", "rejected")
                    & Domain("can_review", "=", True)
                )
                try:
                    records = (
                        Model.with_user(user)
                        .with_context(active_test=False)
                        .search(records_domain)
                    )
                except AccessError:
                    # The user is a reviewer on records of a model whose
                    # ir.model.access does not grant them read access (e.g.
                    # a tier definition pointing at account.move while the
                    # reviewer has no accounting group). Skip silently so
                    # the systray keeps working; the reviewer cannot act on
                    # these reviews anyway without read access.
                    _logger.debug(
                        "User %s has no read access to %s; skipping in systray.",
                        user.login,
                        model,
                    )
                    continue
                # Excludes any cancelled records depending on the structure of the model
                if Model._state_field in Model._fields:
                    records = records.filtered(
                        lambda x: x[x._state_field] != x._cancel_state
                    )
                if records:
                    user_reviews[model] = {
                        "id": records[0].id,
                        "name": Model._description,
                        "model": model,
                        "active_field": "active" in Model._fields,
                        "icon": modules.module.get_module_icon(Model._original_module),
                        "type": "tier_review",
                        "pending_count": len(records),
                    }
        return list(user_reviews.values())
