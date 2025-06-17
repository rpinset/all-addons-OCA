from odoo import api, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    @api.depends("timesheet_ids.unit_amount", "timesheet_ids.time_type_id.non_billable")
    def _compute_total_hours(self):
        for record in self:
            record.total_hours = sum(
                line.unit_amount
                for line in record.timesheet_ids
                if not line.time_type_id.non_billable
            )
