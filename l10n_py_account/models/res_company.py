# l10n_py_account/models/res_company.py

from odoo import models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _localization_use_documents(self):
        """Activar uso de document types para empresas de Paraguay"""
        self.ensure_one()
        if self.account_fiscal_country_id.code == "PY":
            return True
        return super()._localization_use_documents()
