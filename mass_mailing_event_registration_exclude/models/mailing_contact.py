# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2020 Tecnativa - Alexandre D. Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MailingContact(models.Model):
    _name = "mailing.contact"
    _inherit = ["mailing.contact", "mailing.search.exclude.mixin"]
