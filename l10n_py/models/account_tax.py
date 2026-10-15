from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    l10n_py_iva_affectation = fields.Selection(
        selection=[
            ("1", "Gravado IVA"),
            ("2", "Exonerado (Art. 100 Ley 6380/2019)"),
            ("3", "Exento"),
            ("4", "Gravado parcial"),
        ],
        string="Afectación IVA (SIFEN)",
        # Sin default: un impuesto existente (upgrade de base en producción)
        # debe quedar falsy para que _l10n_py_infer_affectation() haga la
        # retrocompatibilidad (amount 0 -> exento). Un default "1" marcaría
        # el impuesto Exento existente como Gravado y el fallback nunca
        # dispararía. Los impuestos del chart template traen el valor por CSV.
        help="Forma de afectación del IVA (iAfecIVA) para el DE SIFEN. "
        "Exportación usa Exonerado (2).",
    )
