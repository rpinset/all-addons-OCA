# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class ContributorsController(CustomerPortal):
    @http.route(
        [
            "/vcp",
            "/vcp/<string:vcp>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def contributors_vcp(self, vcp=None):
        values = self._prepare_portal_layout_values()
        values.update(self._prepare_home_portal_values([]))
        if vcp is None:
            vcps = request.env["vcp.platform"].search([])
            return request.render(
                "vcp_portal.vcp_platforms_template",
                {"vcps": vcps, **values},
            )
        vcp_id = (
            request.env["vcp.platform"]
            .sudo()
            .search([("name", "=ilike", vcp)], limit=1)
            .id
        )
        return request.render(
            "vcp_portal.vcp_platform_template",
            {"vcp": vcp_id, **values},
        )

    def _get_field(self, kind):
        if kind == "contributors":
            return "user_id"
        elif kind == "organizations":
            return "organization_id"
        elif kind == "repositories":
            return "repository_id"
        return False

    @http.route(["/vcp-fetch"], type="json", auth="user", readonly=True)
    def fetch_vcp_data(self, vcp_id, year, month, kind, period, **values):
        vcp = request.env["vcp.platform"].browse(vcp_id).exists()
        if not vcp:
            return []
        start, end = vcp._get_dates(year, month, period, **values)
        data = vcp._generate_data(start, end, self._get_field(kind), kind, **values)
        return {
            "columns": vcp._get_vcp_columns(kind),
            "data": vcp._improve_vcp_data(data, kind, **values),
        }
