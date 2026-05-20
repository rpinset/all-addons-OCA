from roulier.carriers.laposte_fr.api import LAPOSTE_LABEL_FORMAT

from odoo import fields, models


class CarrierAccount(models.Model):
    _inherit = "carrier.account"

    laposte_fr_file_format = fields.Selection(
        [
            (file_format, file_format.replace("_", " "))
            for file_format in LAPOSTE_LABEL_FORMAT
        ],
        default=LAPOSTE_LABEL_FORMAT[0],
        string="Label format",
    )
