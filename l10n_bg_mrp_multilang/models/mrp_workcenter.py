# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class MrpWorkcenter(models.Model):
    _inherit = "mrp.workcenter"

    name = fields.Char(translate=True)
