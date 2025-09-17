# Copyright (C) 2014 Savoir-faire Linux. All Rights Reserved.
# Copyright 2016-2019 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    def setUp(self):
        super().setUp()

    def test_create_from_user(self):
        user = self.env["res.users"].create(
            {
                "login": "test-hr_employee_firstname_partner_firstname",
                "firstname": "FirstName1 Firstname2",
                "lastname": "LastName1 LastName2",
            }
        )
        user.action_create_employee()
        self.assertEqual(user.employee_ids.firstname, "FirstName1 Firstname2")
        self.assertEqual(user.employee_ids.lastname, "LastName1 LastName2")
