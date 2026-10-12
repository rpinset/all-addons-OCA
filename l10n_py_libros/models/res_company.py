# l10n_py_libros/models/res_company.py

from odoo import fields, models
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_py_libro_iva_activo = fields.Boolean(
        string="Sujeto a IVA (Libros DNIT)", default=True
    )
    l10n_py_libro_ire_activo = fields.Boolean(
        string="Sujeto a IRE (Libros DNIT)", default=False
    )
    l10n_py_libro_irp_rsp_activo = fields.Boolean(
        string="Sujeto a IRP-RSP (Libros DNIT)", default=False
    )

    l10n_py_libro_nc_nd_direction = fields.Selection(
        selection=[("padrao", "Padrão (RG 12/24)"), ("invertida", "Invertida")],
        string="Dirección NC/ND (Libros DNIT)",
        required=True,
        default="padrao",
    )

    def write(self, vals):
        if "l10n_py_libro_nc_nd_direction" in vals:
            libro_model = self.env["l10n_py.libro"]
            for company in self:
                new_value = vals["l10n_py_libro_nc_nd_direction"]
                if new_value != company.l10n_py_libro_nc_nd_direction:
                    blocking = libro_model.search(
                        [
                            ("company_id", "=", company.id),
                            ("tipo_registro", "in", ("ventas", "compras")),
                            ("state", "in", ("generated", "confirmed")),
                        ],
                        limit=1,
                    )
                    if blocking:
                        raise UserError(
                            self.env._(
                                "Existem libros de Ventas/Compras já gerados. "
                                "Reabra-os antes de trocar a direção NC/ND, e "
                                "gere-os novamente depois."
                            )
                        )
        return super().write(vals)
