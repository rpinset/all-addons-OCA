# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import datetime
from unittest.mock import patch

from odoo.addons.base.tests.common import BaseCommon


class TestAccountAnalyticLine(BaseCommon):
    @patch("odoo.addons.hr_holidays.models.hr_leave.HolidaysRequest.get_unusual_days")
    def test_get_unusual_days_with_date_range(self, patch_get_unusual_days):
        # arrange
        date_from = datetime(2024, 12, 23)
        date_to = datetime(2024, 12, 29)
        return_value = {
            "2024-12-23": False,
            "2024-12-24": False,
            "2024-12-25": True,
            "2024-12-26": True,
            "2024-12-27": False,
            "2024-12-28": True,
            "2024-12-29": True,
        }
        patch_get_unusual_days.return_value = return_value

        # act
        unusual_days = self.env["account.analytic.line"].get_unusual_days(
            date_from, date_to
        )

        # assert
        self.assertEqual(unusual_days, return_value)

    def test_get_unusual_days_empty_result(self):
        date_from = datetime(2024, 12, 16)
        date_to = datetime(2024, 12, 18)

        unusual_days = self.env["account.analytic.line"].get_unusual_days(
            date_from, date_to
        )
        self.assertEqual(
            unusual_days,
            {"2024-12-16": False, "2024-12-17": False, "2024-12-18": False},
        )
