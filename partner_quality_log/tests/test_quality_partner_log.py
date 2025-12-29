# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import fields
from odoo.tests.common import TransactionCase


class TestQualityPartnerLog(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create(
            {
                "name": "Partner test",
            }
        )

    def test_add_quality_partner_log(self):
        self.assertFalse(self.partner.qualification_log_ids)
        self.partner.price_quality = "3_good"
        self.assertEqual(len(self.partner.qualification_log_ids), 1)
        self.assertEqual(self.partner.qualification_log_ids.price_quality, "3_good")
        self.assertEqual(
            self.partner.qualification_log_ids.service_quality, "2_regular"
        )
        self.assertEqual(
            self.partner.qualification_log_ids.attention_quality, "2_regular"
        )
        self.assertEqual(self.partner.qualification_log_ids.partner_quality, 7)
        self.assertEqual(
            self.partner.qualification_log_ids.qualification_date, date.today()
        )
        self.partner.service_quality = "3_good"
        self.assertEqual(len(self.partner.qualification_log_ids), 2)
        self.assertEqual(self.partner.qualification_log_ids[-1].price_quality, "3_good")
        self.assertEqual(
            self.partner.qualification_log_ids[-1].service_quality, "3_good"
        )
        self.assertEqual(
            self.partner.qualification_log_ids[-1].attention_quality, "2_regular"
        )
        self.assertEqual(self.partner.qualification_log_ids[-1].partner_quality, 8)
        self.assertEqual(
            self.partner.qualification_log_ids[-1].qualification_date, date.today()
        )
        self.partner.attention_quality = "3_good"
        self.assertEqual(len(self.partner.qualification_log_ids), 3)
        self.assertEqual(self.partner.qualification_log_ids[-1].price_quality, "3_good")
        self.assertEqual(
            self.partner.qualification_log_ids[-1].service_quality, "3_good"
        )
        self.assertEqual(
            self.partner.qualification_log_ids[-1].attention_quality, "3_good"
        )
        self.assertEqual(self.partner.qualification_log_ids[-1].partner_quality, 9)
        self.assertEqual(
            self.partner.qualification_log_ids[-1].qualification_date, date.today()
        )

    def test_no_add_quality_partner_log(self):
        self.assertFalse(self.partner.qualification_log_ids)
        self.partner.name = "New name"
        self.assertFalse(self.partner.qualification_log_ids)

    def test_depends_quality(self):
        self.assertEqual(self.partner.price_quality, "2_regular")
        self.assertEqual(self.partner.service_quality, "2_regular")
        self.assertEqual(self.partner.attention_quality, "2_regular")
        self.partner.write(
            {
                "price_quality": "3_good",
                "service_quality": "3_good",
                "attention_quality": "3_good",
            }
        )
        self.assertEqual(self.partner.price_quality, "3_good")
        self.assertEqual(self.partner.service_quality, "3_good")
        self.assertEqual(self.partner.attention_quality, "3_good")
        self.assertEqual(self.partner.partner_quality, 9)
        today = fields.Date.today()
        self.assertEqual(self.partner.qualification_date, today)
