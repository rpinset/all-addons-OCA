# Copyright 2025 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class EndpointMixin(models.AbstractModel):
    _inherit = "endpoint.mixin"

    cache_preheat = fields.Boolean(
        string="Automatic cache pre-heat",
        help="If checked, cache will be pre-heated by a cron "
        "according to the selected policy. "
        "Cache generation will be done in a queue job.",
    )
    cache_preheat_ts = fields.Datetime(readonly=True, string="Last pre-heat on")

    @api.model
    def cron_endpoint_cache_preheat(self):
        """Cron job to preheat cache"""
        now = fields.Datetime.now()
        _logger.info("cron_endpoint_cache_preheat started")
        base_domain = [("cache_policy", "!=", False), ("cache_preheat", "=", True)]
        delta = {
            "day": fields.Datetime.subtract(now, days=1),
            "week": fields.Datetime.subtract(now, weeks=1),
            "month": fields.Datetime.subtract(now, months=1),
        }
        for policy in ("day", "week", "month"):
            domain = base_domain + [
                ("cache_policy", "=", policy),
                "|",
                (
                    "cache_preheat_ts",
                    "<=",
                    delta[policy].replace(hour=23, minute=59, second=59),
                ),
                ("cache_preheat_ts", "=", False),
            ]
            for rec in self.search(domain):
                rec.with_delay(
                    description=f"Pre-heat cache for endpoint {rec.route}"
                )._cron_endpoint_cache_preheat()
                _logger.info("cron_endpoint_cache_preheat preheated rec=%s", rec.id)
        _logger.info("cron_endpoint_cache_preheat finished")
        return True

    def _cron_endpoint_cache_preheat(self):
        """Preheat cache for cron"""
        self._endpoint_cache_preheat()
        self.cache_preheat_ts = fields.Datetime.now()

    def _endpoint_cache_wipe(self, domain):
        # pylint: disable=missing-return
        super()._endpoint_cache_wipe(domain)
        self.cache_preheat_ts = False

    def action_preheat_cache_async(self):
        self.action_purge_cache_attachments()
        self.with_delay(
            description=f"Pre-heat cache for endpoint {self.route}"
        )._cron_endpoint_cache_preheat()
        return {"type": "ir.actions.act_window_close"}
