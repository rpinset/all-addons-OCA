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
            # Skip Models not having Tier Validation enabled (example: was unistalled)
            if not tier_review or model not in self.env:
                continue
            Model = self.env[model]
            if hasattr(Model, "can_review"):
                records_domain = Domain(
                    "id", "in", tier_review.mapped("res_id")
                ) & Domain("validation_status", "!=", "rejected")
                # Excludes any cancelled records depending on the structure of
                # the model. Let PostgreSQL do it whenever the state field is a
                # real column -- which it is on every model that stores its
                # state -- and keep the Python pass only as the fallback for
                # models whose state field is computed and not stored.
                state_field = Model._fields.get(Model._state_field)
                state_in_db = state_field is not None and state_field.store
                if state_in_db:
                    records_domain &= Domain(
                        Model._state_field, "!=", Model._cancel_state
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
                # ``can_review`` is deliberately *not* part of ``records_domain``.
                # Its search method re-searches the reviewer's whole backlog on
                # this model and then evaluates the field in Python over all of
                # it, so putting it in the domain made the systray cost grow
                # with the backlog -- on every call, for every reviewer. The
                # candidate set is already narrowed to the pending reviews found
                # above, so evaluate the field on those records instead: same
                # answer, one prefetched batch instead of a second search.
                records = records.filtered("can_review")
                if not state_in_db and Model._state_field in Model._fields:
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
