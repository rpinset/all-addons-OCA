from odoo import models


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    def _get_fpos_validation_functions(self, partner):
        functions = super()._get_fpos_validation_functions(partner)
        if self.env.company.country_id.code != "PY":
            return functions
        # The export position never applies to a Paraguayan partner. It is
        # identified by the ``l10n_py_is_export`` marker (set in the chart
        # template CSV), not by its translatable name.
        return [
            *functions,
            lambda fpos: not fpos.l10n_py_is_export or partner.country_id.code != "PY",
        ]

    def _get_first_matching_fpos(self, partner):
        # Odoo 19.0 has no ranking functions anymore: the first match by
        # sequence wins. A foreign partner must get the export position even
        # when another auto-apply position without country has a lower
        # sequence, so the export positions are tried first.
        if self.env.company.country_id.code == "PY" and (
            partner.country_id.code != "PY"
        ):
            export = self.filtered("l10n_py_is_export")
            fpos = super(AccountFiscalPosition, export)._get_first_matching_fpos(
                partner
            )
            if fpos:
                return fpos
        return super()._get_first_matching_fpos(partner)
