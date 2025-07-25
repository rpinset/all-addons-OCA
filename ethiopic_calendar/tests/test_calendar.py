##############################################################################
#
#    Copyright (C) 2016 Sucros Clear Information Technologies Plc.
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify it
#    under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo.tests.common import TransactionCase

from odoo.addons.ethiopic_calendar.models import ethiopic_calendar as etcal


class EthiopicCalendarTestCase(TransactionCase):
    def test_ethiopic_month_end(self):

        ed = etcal.ethiopic_date(2008, 9, 1)
        ed2 = etcal.ethiopic_month_end(ed)
        ed_expected = etcal.ethiopic_date(2008, 9, 30)
        self.assertEqual(ed2, ed_expected)

    def test_ethiopic_month_end_non_leapyear(self):

        ed = etcal.ethiopic_date(2008, 13, 1)
        ed2 = etcal.ethiopic_month_end(ed)
        ed_expected = etcal.ethiopic_date(2008, 13, 5)
        self.assertEqual(ed2, ed_expected)

    def test_ethiopic_month_end_leapyear(self):

        ed = etcal.ethiopic_date(2007, 13, 1)
        ed2 = etcal.ethiopic_month_end(ed)
        ed_expected = etcal.ethiopic_date(2007, 13, 6)
        self.assertEqual(ed2, ed_expected)

    def test_ethiopic_next_day(self):

        ed = etcal.ethiopic_date(2010, 6, 6)
        ed2 = etcal.ethiopic_next_day(ed)
        ed_expected = etcal.ethiopic_date(2010, 6, 7)
        self.assertEqual(ed2, ed_expected)

    def test_ethiopic_next_day_non_leapyer(self):

        ed = etcal.ethiopic_date(2012, 13, 5)
        ed2 = etcal.ethiopic_next_day(ed)
        ed_expected = etcal.ethiopic_date(2013, 1, 1)
        self.assertEqual(ed2, ed_expected)

    def test_ethiopic_next_day_leapyear(self):

        ed = etcal.ethiopic_date(2011, 13, 5)
        ed2 = etcal.ethiopic_next_day(ed)
        ed_expected = etcal.ethiopic_date(2011, 13, 6)
        self.assertEqual(ed2, ed_expected)

    def test_ethiopic_date_str(self):

        ed = etcal.ethiopic_date(2000, 1, 1)
        ed_str = etcal.ethiopic_date_str(ed)
        expected_str = "2000-01-01"
        self.assertEqual(ed_str, expected_str)

    def test_ethiopic_date_str2(self):

        ed = etcal.ethiopic_date(2000, 1, 10)
        ed_str = etcal.ethiopic_date_str(ed)
        expected_str = "2000-01-10"
        self.assertEqual(ed_str, expected_str)
