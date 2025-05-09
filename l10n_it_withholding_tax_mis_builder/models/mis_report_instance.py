# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import models


class MisReportInstance(models.Model):
    _inherit = "mis.report.instance"

    def _compute_matrix(self):
        return super(
            MisReportInstance, self.with_context(inject_withholding_tax_amounts=True)
        )._compute_matrix()
