# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from logging import getLogger

from odoo import api, fields, models
from odoo.orm.domains import Domain
from odoo.tools.misc import OrderedSet

_logger = getLogger(__name__)


class MulticompanyReportingCurrencyMixin(models.AbstractModel):
    """Abstract mixin for models that use multicompany reporting currency"""

    _name = "multicompany.reporting.currency.mixin"
    _description = "Multicompany Reporting Currency Mixin"

    multicompany_reporting_currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self._get_default_multicompany_reporting_currency_id(),
        readonly=True,
    )

    @api.model
    def _get_default_multicompany_reporting_currency_id(self):
        # Default to the sys param multicompany reporting currency value
        return self._get_multicompany_reporting_currency_from_sys_param()

    @api.model
    def _get_multicompany_reporting_currency_from_sys_param(self):
        """Retrieves the currently configured multicompany reporting currency

        Hook method, can be overridden by inheriting models
        """
        currency = self.env["res.currency"]

        # We try to retrieve the multicompany reporting currency from the system params,
        # but ``get_param(key)`` will return either ``None`` or a ``str`` object; since
        # we cannot be 100% sure we'll be able to convert it to a ``res.currency``
        # record ID, we use the user's environmental company currency as fallback
        key = "base_multicompany_reporting_currency.multicompany_reporting_currency"
        if value := self.env["ir.config_parameter"].sudo().get_param(key, default=""):
            try:
                currency = currency.browse(int(value)).exists()
            except ValueError:  # pylint: disable=except-pass
                pass
        if not currency:
            currency = self.env.company.currency_id
            _logger.warning(
                "Could not get multicompany reporting currency from system"
                f" parameters, using user's company currency '{currency.name}'"
            )
        return currency

    @api.model
    def _update_multicompany_reporting_currency(self):
        """Updates the multicompany reporting currency on all inheriting models"""
        for model in self._get_multicompany_reporting_currency_inheriting_models():
            # We use the sudo-ed model because this is an automation, and we
            # cannot predict whether the current user has read/write access
            # on all inheriting models
            model = model.sudo()
            ctx = model._get_multicompany_reporting_currency_ctx_for_records_update()
            model = model.with_context(ctx)  # pylint: disable=context-overridden
            dom = model._get_multicompany_reporting_currency_domain_for_records_update()
            recs = model.search(dom)
            vals = model._get_multicompany_reporting_currency_vals_for_records_update()
            if recs and vals:
                recs.write(vals)

    @api.model
    def _get_multicompany_reporting_currency_inheriting_models(self):
        """Retrieves an ordered set of models that inherit from this mixin

        Hook method, can be overridden by inheriting models
        """
        inheriting_models: OrderedSet[models.BaseModel] = OrderedSet()

        def _add_models_recursively(model: models.BaseModel):
            for model_name in model._inherit_children:
                model = self.env.get(model_name)
                if model is not None and model not in inheriting_models:
                    inheriting_models.add(model)
                    _add_models_recursively(model)

        # NB: ``multicompany.reporting.currency.mixin`` is excluded from the end result
        _add_models_recursively(self.env["multicompany.reporting.currency.mixin"])
        return inheriting_models

    @api.model
    def _get_multicompany_reporting_currency_ctx_for_records_update(self):
        """Prepares a basic context to search/update records

        Hook method, can be overridden by inheriting models
        """
        # By default, search and update archived records too
        return dict(self.env.context, active_test=False)

    @api.model
    def _get_multicompany_reporting_currency_domain_for_records_update(self):
        """Prepares a basic domain to search records to update

        Hook method, can be overridden by inheriting models
        """
        currency = self._get_multicompany_reporting_currency_from_sys_param()
        return Domain([("multicompany_reporting_currency_id", "!=", currency.id)])

    @api.model
    def _get_multicompany_reporting_currency_vals_for_records_update(self):
        """Prepares basic record values for the update

        Hook method, can be overridden by inheriting models
        """
        currency = self._get_multicompany_reporting_currency_from_sys_param()
        return {"multicompany_reporting_currency_id": currency.id}
