# © 2014-2016 Akretion (http://www.akretion.com)
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Quentin DUPONT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BaseDocumentLayout(models.TransientModel):
    _inherit = "base.document.layout"

    report_legal_description = fields.Char(
        related="company_id.report_legal_description", readonly=True
    )
