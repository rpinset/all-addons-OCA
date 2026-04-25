# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ProjectTask(models.Model):
    _name = "project.task"
    _inherit = ["project.task", "edi.exchange.consumer.mixin"]
