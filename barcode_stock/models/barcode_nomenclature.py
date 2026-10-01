# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class BarcodeNomenclature(models.Model):
    _inherit = "barcode.nomenclature"

    @api.model
    def parse_barcode_scanner_barcode(self, barcode):
        # A company may run its own nomenclature (a custom one, or the GS1
        # one); reading it the way the core does keeps the scanner and the
        # back office decoding the same barcode alike.
        nomenclature = self.env.company.nomenclature_id or self.env.ref(
            "barcodes.default_barcode_nomenclature"
        )
        parsed = nomenclature.parse_barcode(barcode)
        return {
            "type": "ean",
            "product": parsed.get("code"),
            "qty": parsed.get("value", 1),
        }
