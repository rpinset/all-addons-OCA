from odoo import api, models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    @api.model
    def _message_route_process(self, message, message_dict, routes):
        # Change stage from mails coming from fetchmail
        if routes and routes[0][0] == "helpdesk.ticket":
            ticket_id = routes[0][1]
            ticket = self.env["helpdesk.ticket"].sudo().browse(int(ticket_id))
            if (
                ticket.team_id.autoupdate_ticket_stage
                and ticket.stage_id in ticket.team_id.autopupdate_src_stage_ids
            ):
                ticket.stage_id = ticket.team_id.autopupdate_dest_stage_id.id
        return super()._message_route_process(message, message_dict, routes)
