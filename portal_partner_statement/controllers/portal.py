# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, exceptions, http
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal


class PortalPartnerStatement(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        # If there are no partner statements to be shown
        # hide the page in user's home
        allowed_partner_statements = self._prepare_partner_statements_values()[
            "report_names_dict"
        ]
        values["partner_statement_allowed"] = bool(allowed_partner_statements)
        return values

    def _is_partner_statement_allowed(self, report_name, raise_if_not_allowed=False):
        partner = request.env.user.partner_id
        is_commercial_partner = partner == partner.commercial_partner_id
        allowed = is_commercial_partner
        if not allowed and raise_if_not_allowed:
            raise exceptions.AccessError(
                _(
                    "You do not have access to this Partner Statement, "
                    "please request it to your commercial partner",
                )
            )

        base_group = request.env.ref("account.group_account_invoice").sudo()
        if report_name == "outstanding_statement":
            report_group = request.env.ref(
                "partner_statement.group_outstanding_statement"
            )
            allowed &= report_group in base_group.implied_ids

        if not allowed and raise_if_not_allowed:
            raise exceptions.AccessError(
                _(
                    "You do not have access to this Partner Statement, "
                    "please request it to your Administrator",
                )
            )
        return allowed

    def _prepare_partner_statements_values(self):
        values = {
            "page_name": "partner_statements",
            "report_names_dict": dict(),
        }
        report_names_dict = values["report_names_dict"]
        if self._is_partner_statement_allowed("outstanding_statement"):
            report_names_dict["outstanding_statement"] = _("Outstanding Statement")
        return values

    @http.route(
        [
            "/my/partner_statements",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_partner_statements(self):
        values = self._prepare_partner_statements_values()
        return request.render(
            "portal_partner_statement.portal_my_partner_statements", values
        )

    def _get_report_action_ref(self, report_name, report_type):
        report_name_to_report_action = {
            (
                "outstanding_statement",
                "html",
            ): "action_print_outstanding_statement_html",
            ("outstanding_statement", "pdf"): "action_print_outstanding_statement",
        }
        report_ref = report_name_to_report_action.get((report_name, report_type))
        return f"partner_statement.{report_ref}"

    @http.route(
        [
            "/my/partner_statements/download",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_download_partner_statement(self, report_name, report_type, data=None):
        if data is None:
            data = {}

        self._is_partner_statement_allowed(
            report_name,
            raise_if_not_allowed=True,
        )

        report_action_ref = self._get_report_action_ref(report_name, report_type)
        partner = request.env.user.partner_id
        return self._show_report(
            model=partner,
            report_type=report_type,
            report_ref=report_action_ref,
        )
