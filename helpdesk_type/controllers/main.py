import odoo.http as http
from odoo.http import request

from odoo.addons.helpdesk_mgmt.controllers.main import HelpdeskTicketController


class HelpdeskTicketControllerTypes(HelpdeskTicketController):
    def _get_types(self):
        return (
            http.request.env["helpdesk.ticket.type"]
            .with_company(request.env.company.id)
            .search([("active", "=", True), ("show_in_portal", "=", True)])
            if http.request.env.user.company_id.helpdesk_mgmt_portal_type
            else False
        )

    @http.route("/new/ticket", type="http", auth="user", website=True)
    def create_new_ticket(self, **kw):
        company = request.env.company
        response = super().create_new_ticket(**kw)
        response.qcontext["types"] = self._get_types()
        response.qcontext["ticket_type_id_required"] = (
            company.helpdesk_mgmt_portal_type_id_required
        )
        return response

    def _prepare_submit_ticket_vals(self, **kw):
        vals = super()._prepare_submit_ticket_vals(**kw)
        type_id = kw.get("type")
        if not type_id:
            return vals
        ticket_type = http.request.env["helpdesk.ticket.type"].search(
            [("id", "=", int(type_id)), ("show_in_portal", "=", True)]
        )
        vals["type_id"] = ticket_type.id
        return vals
