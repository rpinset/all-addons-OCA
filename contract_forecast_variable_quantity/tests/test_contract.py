# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.contract_forecast.tests.test_contract_line_forecast_period import (
    TestContractLineForecastPeriod,
)


class TestContract(TestContractLineForecastPeriod):
    def test_forecast_period_on_contract_line_update_12(self):
        self.acct_line.write({"qty_type": "fixed"})
        self.assertTrue(self.acct_line.forecast_period_ids)
        self.assertEqual(len(self.acct_line.forecast_period_ids), 12)
