# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.orm.model_classes import add_to_registry
from odoo.tools.misc import mute_logger

from odoo.addons.base.tests.common import BaseCommon


class Common(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Setup ``fake.model`` for testing
        from .fake_models import FakeModel

        add_to_registry(cls.registry, FakeModel)
        cls.registry._setup_models__(cls.env.cr, ["fake.model"])
        cls.registry.init_models(cls.env.cr, ["fake.model"], {"models_to_check": 1})

    @classmethod
    def tearDownClass(cls):
        cls.registry.__delitem__("fake.model")
        super().tearDownClass()

    @mute_logger(
        "odoo.addons.base_multicompany_reporting_currency.models.multicompany_reporting_currency_mixin"
    )
    def _set_multicompany_reporting_currency_param(self, currency_id):
        self.env["ir.config_parameter"].sudo().set_param(
            "base_multicompany_reporting_currency.multicompany_reporting_currency",
            currency_id,
        )

    def _test_multicompany_reporting_currency(self, currency_id, valid=True):
        self._set_multicompany_reporting_currency_param(currency_id)
        mcrc_mixin = self.env["multicompany.reporting.currency.mixin"]
        getter = mcrc_mixin._get_multicompany_reporting_currency_from_sys_param
        if valid:
            expected_currency = self.env["res.currency"].browse(currency_id)
            with self.assertNoLogs(level="WARNING"):
                multicompany_reporting_currency = getter()
        else:
            expected_currency = self.env.company.currency_id
            with self.assertLogs(level="WARNING") as log_catcher:
                multicompany_reporting_currency = getter()
            self.assertEqual(
                log_catcher.records[0].message,
                "Could not get multicompany reporting currency from system parameters,"
                f" using user's company currency '{self.env.company.currency_id.name}'",
            )
        self.assertEqual(multicompany_reporting_currency, expected_currency)
