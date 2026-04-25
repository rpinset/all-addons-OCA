# Copyright 2024 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import api, exceptions, fields, models
from odoo.http import request
from odoo.tools import date_utils

_logger = logging.getLogger(__name__)


class EndpointMixin(models.AbstractModel):
    _inherit = "endpoint.mixin"

    cache_policy = fields.Selection(
        selection=[
            ("day", "Daily"),
            ("week", "Weekly"),
            ("month", "Monthly"),
        ],
        default="day",
    )
    cache_att_count = fields.Integer(
        compute="_compute_cache_att_count", string="Cache count"
    )

    def _compute_cache_att_count(self):
        domain = [
            ("name", "like", "endpoint_cache%"),
            ("res_model", "=", self._name),
        ]
        data = self.env["ir.attachment"].read_group(domain, ["res_id"], ["res_id"])
        mapped_data = {m["res_id"]: m["res_id_count"] for m in data}
        for rec in self:
            rec.cache_att_count = mapped_data.get(rec.id, 0)

    def _endpoint_cache_make_name(self, ext, suffix=None):
        parts = [
            "endpoint_cache",
            self.env["ir.http"]._slugify_one(self.name).replace("-", "_"),
        ]
        if suffix:
            parts.append(suffix)
        if ext:
            parts.append(ext)
        return ".".join(parts)

    def _endpoint_cache_get(self, name):
        att = (
            self.env["ir.attachment"]
            .sudo()
            .search(self._endpoint_cache_get_domain(name), limit=1)
        )
        self._logger.debug("_endpoint_cache_get found att=%s", att.id)
        return att.raw

    def _endpoint_cache_get_domain(self, cache_name):
        now = fields.Datetime.now()
        from_datetime = date_utils.start_of(now, self.cache_policy)
        to_datetime = date_utils.end_of(now, self.cache_policy)
        return [
            ("name", "=", cache_name),
            ("res_model", "=", self._name),
            ("res_id", "=", self.id),
            ("create_date", ">=", from_datetime),
            ("create_date", "<=", to_datetime),
        ]

    def _endpoint_cache_store(self, name, raw_data, mimetype=None):
        self._logger.debug("_endpoint_cache_store store att=%s", name)
        if not name.startswith("endpoint_cache"):
            raise exceptions.UserError(
                self.env._("Cache name must start with 'endpoint_cache'")
            )
        return (
            self.env["ir.attachment"]
            .sudo()
            .create(
                {
                    "type": "binary",
                    "name": name,
                    "raw": raw_data,
                    "mimetype": mimetype,
                    "res_model": self._name,
                    "res_id": self.id,
                }
            )
        )

    @api.model
    def _endpoint_cache_gc_domain(self):
        now = fields.Datetime.now()
        gc_from = date_utils.subtract(now, days=32)
        return [
            ("name", "like", "endpoint_cache%"),
            ("res_model", "=", self._name),
            ("create_date", "<=", gc_from),
        ]

    @api.autovacuum
    def _endpoint_cache_gc(self):
        """Garbage collector for old caches"""
        domain = self._endpoint_cache_gc_domain()
        self._endpoint_cache_wipe(domain)

    def _endpoint_cache_wipe(self, domain):
        """Wipe cache attachments based on domain"""
        self.env["ir.attachment"].sudo().search(domain).unlink()
        _logger.debug("_endpoint_cache_wipe wiped domain=%s", domain)

    def action_view_cache_attachments(self):
        """Action to view cache attachments"""
        action = self.env["ir.actions.actions"]._for_xml_id("base.action_attachment")
        action["domain"] = self._endpoint_view_cache_domain()
        action["name"] = self.env._("Cache results")
        return action

    def _endpoint_view_cache_domain(self):
        return [
            ("name", "like", "endpoint_cache%"),
            ("res_model", "=", self._name),
            ("res_id", "=", self.id),
        ]

    def action_purge_cache_attachments(self):
        """Action to purge cache attachments"""
        domain = self._endpoint_view_cache_domain()
        self._endpoint_cache_wipe(domain)
        return {"type": "ir.actions.act_window_close"}

    def action_preheat_cache(self):
        domain = self._endpoint_view_cache_domain()
        self._endpoint_cache_wipe(domain)
        self._endpoint_cache_preheat()
        return {"type": "ir.actions.act_window_close"}

    def _endpoint_cache_preheat(self):
        """Preheat cache"""
        _logger.debug("_endpoint_cache_preheat work in progress")
        # We assume that the endpoint snippet is taking care
        # of handling the cache generation as recommended.
        # Hence, we can simply simulate a request to the endpoint
        # to get the cache re-generated.
        # NOTE: this might take some time.
        self._handle_request(request)
