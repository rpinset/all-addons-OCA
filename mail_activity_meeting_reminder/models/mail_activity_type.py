# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailActivityType(models.Model):

    _inherit = "mail.activity.type"

    default_alarm_ids = fields.Many2many("calendar.alarm")
