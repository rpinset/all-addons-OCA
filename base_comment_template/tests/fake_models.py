# Copyright 2017 LasLabs Inc.
# Copyright 2018 ACSONE
# Copyright 2018 Camptocamp
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import models


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = ["res.users", "comment.template"]
    _teardown_no_delete = True
