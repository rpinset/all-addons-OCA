from odoo import api, models
from odoo.tools import email_normalize


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def _message_route_process(self, message, message_dict, routes):
        self.change_ticket_status_via_mail(routes, message_dict)
        return super()._message_route_process(message, message_dict, routes)

    def change_ticket_status_via_mail(self, routes, message_dict):
        if routes and routes[0][0] == "helpdesk.ticket":
            ticket_id = routes[0][1]
            email_from = message_dict.get("email_from")
            if email_from:
                email_from = email_normalize(email_from)

            ticket = self.env["helpdesk.ticket"].sudo().browse(int(ticket_id)).exists()
            user_id = routes[0][3]
            if ticket:
                if not (
                    ticket.team_id.autoupdate_ticket_stage
                    and ticket.stage_id in ticket.team_id.autopupdate_src_stage_ids
                ):
                    return None

                update_stage = False
                email_partner = False
                if ticket.partner_email == email_from:
                    update_stage = True

                ticket_partner = ticket.partner_id
                if user_id:
                    email_partner = (
                        self.env["res.users"]
                        .search([("id", "=", user_id)], limit=1)
                        .partner_id
                    )
                if email_partner and ticket_partner:
                    update_stage = email_partner.id == ticket_partner.id
                elif email_partner:
                    update_stage = email_partner.email == ticket.partner_email
                elif ticket_partner:
                    update_stage = ticket_partner.email == email_from

                if update_stage:
                    ticket.stage_id = ticket.team_id.autopupdate_dest_stage_id.id

        return None
