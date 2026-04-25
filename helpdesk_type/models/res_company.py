from odoo import fields, models


class Company(models.Model):
    _inherit = "res.company"

    helpdesk_mgmt_portal_type = fields.Boolean(
        string="Show type in portal form",
        help="Select type in Helpdesk portal",
    )
    helpdesk_mgmt_portal_type_id_required = fields.Boolean(
        string="Required Type field in Helpdesk portal",
    )
