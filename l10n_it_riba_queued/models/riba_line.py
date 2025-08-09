# Copyright 2025 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class RiBaLine(models.Model):
    _inherit = "riba.distinta.line"

    def riba_line_settlement(self, date=None):
        if self.env.context.get("l10n_it_riba_async_single_process"):
            for line in self:
                super(RiBaLine, line).with_delay().riba_line_settlement(date=date)
            result = None
        else:
            result = super().riba_line_settlement(date=date)
        return result
