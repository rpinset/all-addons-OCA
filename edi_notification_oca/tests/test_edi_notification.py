# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


import base64

from odoo import Command
from odoo.tests.common import RecordCapturer

from odoo.addons.edi_core_oca.tests.common import EDIBackendCommonTestCase


class TestEDINotification(EDIBackendCommonTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_env()
        vals = {
            "model": cls.partner._name,
            "res_id": cls.partner.id,
            "exchange_file": base64.b64encode(b"1234"),
        }
        cls.record = cls.backend.create_record("test_csv_input", vals)
        cls.group_portal = cls.env.ref("base.group_portal")
        cls.user_a = cls._create_user("A")
        cls.user_b = cls._create_user("B")
        cls.user_c = cls._create_user("C")

    @classmethod
    def _create_user(cls, letter: str):
        return (
            cls.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "name": f"User {letter}",
                    "login": f"user_{letter}",
                    "group_ids": [Command.set([cls.group_portal.id])],
                }
            )
        )

    def _trigger_process_error(self, message="OOPS! Something went wrong :("):
        self.record.exchange_error = message
        self.record._notify_error("process_ko")

    def test_inverse_notify_on_process_error(self):
        self.exchange_type_in.notify_on_process_error = False
        # If we forgot to enable notify_on_process_error
        self.exchange_type_in.write(
            {
                "notify_on_process_error_groups_ids": [
                    Command.set([self.group_portal.id])
                ],
                "notify_on_process_error_users_ids": [Command.set([self.user_c.id])],
            }
        )
        # Make sure notify_on_process_error should be enabled
        self.assertTrue(self.exchange_type_in.notify_on_process_error)

    def test_dont_notify_on_process_error(self):
        self.exchange_type_in.notify_on_process_error = False
        with RecordCapturer(self.env["mail.activity"], []) as capture:
            self._trigger_process_error()
        self.assertIn("OOPS! Something went wrong :(", self.record.exchange_error)
        # We don't expect any notification
        self.assertEqual(len(capture.records), 0)

    def test_notify_on_process_error_to_group(self):
        self.exchange_type_in.write(
            {
                "notify_on_process_error": True,
                "notify_on_process_error_groups_ids": [
                    Command.set([self.group_portal.id])
                ],
            }
        )
        # Remove group on user C to test
        self.user_c.group_ids = [Command.clear()]
        with RecordCapturer(self.env["mail.activity"], []) as capture:
            # Send notification to all users in defined groups when error
            self._trigger_process_error()
        a_noti = capture.records.filtered(lambda x: x.user_id == self.user_a)
        self.assertEqual(len(a_noti), 1)
        self.assertEqual(
            a_noti.summary,
            f"EDI: Process error on record '{self.record.identifier}'.",
        )
        self.assertIn("OOPS! Something went wrong :(", a_noti.note)
        b_noti = capture.records.filtered(lambda x: x.user_id == self.user_b)
        self.assertEqual(len(b_noti), 1)
        self.assertEqual(
            b_noti.summary,
            f"EDI: Process error on record '{self.record.identifier}'.",
        )
        # We don't send notification to user C
        # because C is not belonging to the group_portal
        self.assertIn("OOPS! Something went wrong :(", b_noti.note)
        c_noti = capture.records.filtered(lambda x: x.user_id == self.user_c)
        self.assertEqual(len(c_noti), 0)

    def test_notify_on_process_error_to_users(self):
        self.exchange_type_in.write(
            {
                "notify_on_process_error": True,
                "notify_on_process_error_users_ids": [Command.set([self.user_c.id])],
            }
        )
        with RecordCapturer(self.env["mail.activity"], []) as capture:
            # Send notification to all users in defined users when error
            self._trigger_process_error()
        a_b_noti = capture.records.filtered(
            lambda x: x.user_id in (self.user_a | self.user_b)
        )
        self.assertEqual(len(a_b_noti), 0)
        c_noti = capture.records.filtered(lambda x: x.user_id == self.user_c)
        self.assertEqual(len(c_noti), 1)
        self.assertEqual(
            c_noti.summary,
            f"EDI: Process error on record '{self.record.identifier}'.",
        )
        self.assertIn("OOPS! Something went wrong :(", c_noti.note)

    def test_notify_on_process_error_to_groups_and_users(self):
        self.exchange_type_in.write(
            {
                "notify_on_process_error": True,
                "notify_on_process_error_groups_ids": [
                    Command.set([self.group_portal.id])
                ],
                "notify_on_process_error_users_ids": [Command.set([self.user_c.id])],
            }
        )
        # Remove group on user C to test
        self.user_c.group_ids = [Command.clear()]
        with RecordCapturer(self.env["mail.activity"], []) as capture:
            # Send notification to all users in defined users when error
            self._trigger_process_error()
        a_b_noti = capture.records.filtered(
            lambda x: x.user_id in (self.user_a | self.user_b)
        )
        self.assertEqual(len(a_b_noti), 2)
        # also send notification to user C
        c_noti = capture.records.filtered(lambda x: x.user_id == self.user_c)
        self.assertEqual(len(c_noti), 1)
