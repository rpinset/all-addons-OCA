# Copyright 2024 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, models


class AccountTaxGroup(models.Model):
    _inherit = "account.tax.group"

    asign_type = fields.Selection(
        [
            ("reduced1", "Reduced 1"),
            ("reduced2", "Reduced 2"),
            ("special", "Special"),
            ("null", "Null"),
        ],
        string="a.sign Type",
        help=(
            "RKSV (a.sign) tax category used when computing the chained "
            "signature for Austrian POS receipts."
        ),
    )
