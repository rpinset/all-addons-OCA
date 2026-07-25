# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    @api.model
    def _get_multicompany_reporting_currency_key(self) -> str:
        return "base_multicompany_reporting_currency.multicompany_reporting_currency"

    def init(self, force=False):
        # OVERRIDE: if missing, create the system parameter for key
        # ``base_multicompany_reporting_currency.multicompany_reporting_currency``
        # (will be EUR by default)
        res = super().init(force=force)
        key = self._get_multicompany_reporting_currency_key()
        if not self.search([("key", "=", key)]):
            self.set_param(key, str(self.env.ref("base.EUR").id))
        return res

    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE: recompute the multicompany reporting currency if needed
        params = super().create(vals_list)
        if params._check_multicompany_reporting_currency_needs_update():
            self._update_multicompany_reporting_currency()
        return params

    def write(self, vals):
        # OVERRIDE: recompute the multicompany reporting currency if needed
        res = super().write(vals)
        needs_update = self._check_multicompany_reporting_currency_needs_update()
        if {"key", "value"}.intersection(vals) and needs_update:
            self._update_multicompany_reporting_currency()
        return res

    def unlink(self):
        # OVERRIDE: recompute the multicompany reporting currency if needed
        needs_update = self._check_multicompany_reporting_currency_needs_update()
        res = super().unlink()
        if needs_update:
            self._update_multicompany_reporting_currency()
        return res

    def _check_multicompany_reporting_currency_needs_update(self) -> bool:
        return self._get_multicompany_reporting_currency_key() in self.mapped("key")

    @api.model
    def _update_multicompany_reporting_currency(self):
        mixin = self.env["multicompany.reporting.currency.mixin"]
        mixin._update_multicompany_reporting_currency()
