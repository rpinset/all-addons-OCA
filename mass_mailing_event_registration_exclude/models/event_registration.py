# Copyright 2016 Tenativa - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class EventRegistration(models.Model):
    _name = "event.registration"
    _inherit = ["event.registration", "mailing.search.exclude.mixin"]
