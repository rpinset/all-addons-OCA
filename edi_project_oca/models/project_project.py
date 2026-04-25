# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ["project.project", "edi.exchange.consumer.mixin"]
