from odoo import fields, models


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    l10n_py_is_export = fields.Boolean(
        string="Exportación (PY)",
        help="Marca la posición fiscal de ventas de exportación (IVA "
        "exonerado, Art. 100 Ley 6380/2019). Usada para la detección y "
        "el ranking automático en lugar del nombre traducible.",
    )

    def _get_fpos_ranking_functions(self, partner):
        if self.env.company.country_id.code != "PY":
            return super()._get_fpos_ranking_functions(partner)
        # Ranking por el marcador l10n_py_is_export (campo booleano seteado
        # en el CSV del chart template), no por nombre: el nombre de una
        # posición fiscal es traducible/renombrable.
        # Contrato del core (account/models/partner.py): un valor falsy FILTRA
        # la posición, no baja su ranking — por eso el patrón neutro: una
        # posición no-export queda neutra (True), la de exportación puntúa 2
        # con socio del exterior y se filtra con socio paraguayo o sin país
        # (la dirección de entrega puede no tenerlo).
        return [
            (
                "l10n_py_export",
                lambda fpos: (
                    not fpos.l10n_py_is_export
                    or (partner.country_id and partner.country_id.code != "PY" and 2)
                ),
            ),
        ] + super()._get_fpos_ranking_functions(partner)
