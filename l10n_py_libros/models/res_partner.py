# l10n_py_libros/models/res_partner.py

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_py_libro_electronic = fields.Boolean(
        string="Emite comprobante electrónico (DNIT)",
        company_dependent=True,
        default=False,
        help=(
            "Indica que este proveedor emite comprobante electrónico ante la "
            "DNIT: usado como valor por defecto (copiado, editable) del "
            "campo homónimo en la factura de compra, para excluirla del "
            "Registro de Compras (ya pre-cargado por el Marangatu)."
        ),
    )
