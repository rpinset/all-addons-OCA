# Copyright 2026 ForgeFlow S.L.
#   (http://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from freezegun import freeze_time

from odoo import fields
from odoo.tests.common import TransactionCase

# ``is_absent`` is only true while the current time is inside the leave, and
# ``hr.leave`` narrows a full day leave to the working schedule of the employee
# (08:00-17:00 in the timezone of the company calendar). The tests that need an
# absent employee freeze the clock inside that window, otherwise the result
# depends on the time of the day at which they happen to run.
WORKING_HOUR = "2023-05-15 10:00:00"


class TestNotifyEmployeeLeave(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        internal_group = cls.env.ref("base.group_user")
        partner_manager_group = cls.env.ref("base.group_partner_manager")

        cls.user = cls.env["res.users"].create(
            {
                "name": "Test User",
                "login": "test_user",
                "email": "test@example.com",
                "notification_type": "inbox",
                "group_ids": [(4, internal_group.id), (4, partner_manager_group.id)],
            }
        )

        cls.absent_user = cls.env["res.users"].create(
            {
                "name": "Absent User",
                "login": "absent_user",
                "email": "absent@example.com",
                "notification_type": "inbox",
                "group_ids": [(4, internal_group.id)],
            }
        )

        cls.partner = cls.absent_user.partner_id

        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Absent Employee",
                "user_id": cls.absent_user.id,
            }
        )

        cls.leave_type = cls.env["hr.leave.type"].create(
            {
                "name": "Test Leave",
                "leave_validation_type": "no_validation",
                "requires_allocation": False,
            }
        )

        cls.record = cls.env["res.partner"].create({"name": "Test Record"})

    def _create_validated_leave(self):
        today = fields.Date.today()
        leave = (
            self.env["hr.leave"]
            .with_context(skip_absence_notification=True)
            .create(
                {
                    "holiday_status_id": self.leave_type.id,
                    "employee_id": self.employee.id,
                    "request_date_from": today - timedelta(days=1),
                    "request_date_to": today + timedelta(days=1),
                }
            )
        )
        leave.sudo()._action_validate()
        return leave

    def test_no_notify_when_user_not_absent(self):
        self.record.with_user(self.user).message_post(
            body="Test message", partner_ids=[self.partner.id]
        )

        self.assertNotIn(self.user, self.employee.absence_notified_user_ids)

    @freeze_time(WORKING_HOUR)
    def test_notify_when_user_absent(self):
        self._create_validated_leave()

        self.record.with_user(self.user).message_post(
            body="Test message", partner_ids=[self.partner.id]
        )

        self.assertIn(self.user, self.employee.absence_notified_user_ids)
        self.assertEqual(self.employee.absence_notified_date, fields.Date.today())

    @freeze_time(WORKING_HOUR)
    def test_only_one_notification_per_day(self):
        self._create_validated_leave()

        self.record.with_user(self.user).message_post(
            body="Test message 1", partner_ids=[self.partner.id]
        )

        self.record.with_user(self.user).message_post(
            body="Test message 2", partner_ids=[self.partner.id]
        )

        notified_users = self.employee.absence_notified_user_ids
        self.assertEqual(len(notified_users), 1)
        self.assertIn(self.user, notified_users)
        self.assertEqual(self.employee.absence_notified_date, fields.Date.today())
