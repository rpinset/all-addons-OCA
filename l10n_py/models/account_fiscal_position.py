from odoo import fields, models


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    l10n_py_is_export = fields.Boolean(
        string="Exportación (PY)",
        help="Marca la posición fiscal de ventas de exportación (IVA "
        "exonerado, Art. 100 Ley 6380/2019). Usada para la detección y "
        "el ranking automático en lugar del nombre traducible.",
    )
