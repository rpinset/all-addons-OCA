# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailActivity(models.Model):

    _inherit = "mail.activity"

    filter_internal_user = fields.Boolean(
        string="Assign to internal user only",
        default=True,
    )
