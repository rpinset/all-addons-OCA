from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    helpdesk_mgmt_portal_type = fields.Boolean(
        related="company_id.helpdesk_mgmt_portal_type",
        readonly=False,
    )
    helpdesk_mgmt_portal_type_id_required = fields.Boolean(
        related="company_id.helpdesk_mgmt_portal_type_id_required",
        readonly=False,
    )
