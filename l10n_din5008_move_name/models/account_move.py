# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _compute_l10n_din5008_document_title(self):
        result = super()._compute_l10n_din5008_document_title()
        for record in self:
            if record.is_sale_document(include_receipts=True):
                record.l10n_din5008_document_title = (
                    f"{record.l10n_din5008_document_title} {record.name}"
                )
        return result
