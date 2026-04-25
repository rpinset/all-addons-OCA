# Copyright 2025 Binhex - Adasat Torres de León
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.tests import new_test_user, tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install")
class TestPosHRAccessRight(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.main_pos_config = cls.env.ref("point_of_sale.pos_config_main")
        cls.company_id = cls.env.ref("base.main_company")
        cls.env = cls.env(context={"company_id": cls.company_id.id})
        cls.admin = cls.env.ref("base.user_admin")
        cls.user = new_test_user(
            cls.env,
            name="Test User",
            login="test_user",
            groups="""base.group_user,pos_access_right.group_negative_qty,
            pos_access_right.group_discount""",
        )
        cls.user2 = new_test_user(
            cls.env,
            name="Test User 2",
            login="test_user_2",
            groups="""base.group_user,pos_access_right.group_change_unit_price,
            pos_access_right.group_multi_order""",
        )
        cls.user3 = new_test_user(
            cls.env,
            name="Test User 3",
            login="test_user_3",
            groups="""base.group_user,pos_access_right.group_delete_order,
            pos_access_right.group_payment""",
        )
        cls.emp = cls.env["hr.employee"].create(
            {
                "name": "Test Employee",
                "company_id": cls.company_id.id,
                "user_id": cls.user.id,
            }
        )
        cls.emp2 = cls.env["hr.employee"].create(
            {
                "name": "Test Employee 2",
                "company_id": cls.company_id.id,
                "user_id": cls.user2.id,
            }
        )
        cls.emp3 = cls.env["hr.employee"].create(
            {
                "name": "Test Employee 3",
                "company_id": cls.company_id.id,
                "user_id": cls.user3.id,
            }
        )
        cls.emp4 = cls.env["hr.employee"].create(
            {
                "name": "Test Employee 4",
                "company_id": cls.company_id.id,
            }
        )
        cls.main_pos_config.write(
            {
                "module_pos_hr": True,
                "employee_ids": [
                    Command.set([cls.emp.id, cls.emp2.id, cls.emp3.id, cls.emp4.id])
                ],
            }
        )
        cls.pos_session_id = cls.env["pos.session"].create(
            {"user_id": cls.admin.id, "config_id": cls.main_pos_config.id}
        )

    def test_get_pos_ui_hr_employee(self):
        values = self.pos_session_id._get_pos_ui_hr_employee(
            self.pos_session_id._loader_params_hr_employee()
        )
        self.assertTrue(values)
        self.assertEqual(len(values), 5)

        self.assertEqual(values[0]["hasGroupPayment"], True)
        self.assertEqual(values[1]["hasGroupPayment"], False)
        self.assertEqual(values[2]["hasGroupPayment"], False)
        self.assertEqual(values[3]["hasGroupPayment"], True)
        self.assertEqual(values[4]["hasGroupPayment"], True)

        self.assertEqual(values[0]["hasGroupDiscount"], True)
        self.assertEqual(values[1]["hasGroupDiscount"], True)
        self.assertEqual(values[2]["hasGroupDiscount"], False)
        self.assertEqual(values[3]["hasGroupDiscount"], False)
        self.assertEqual(values[4]["hasGroupDiscount"], True)

        self.assertEqual(values[0]["hasGroupNegativeQty"], True)
        self.assertEqual(values[1]["hasGroupNegativeQty"], True)
        self.assertEqual(values[2]["hasGroupNegativeQty"], False)
        self.assertEqual(values[3]["hasGroupNegativeQty"], False)
        self.assertEqual(values[4]["hasGroupNegativeQty"], True)

        self.assertEqual(values[0]["hasGroupPriceControl"], True)
        self.assertEqual(values[1]["hasGroupPriceControl"], False)
        self.assertEqual(values[2]["hasGroupPriceControl"], True)
        self.assertEqual(values[3]["hasGroupPriceControl"], False)
        self.assertEqual(values[4]["hasGroupPriceControl"], True)

        self.assertEqual(values[0]["hasGroupMultiOrder"], True)
        self.assertEqual(values[1]["hasGroupMultiOrder"], False)
        self.assertEqual(values[2]["hasGroupMultiOrder"], True)
        self.assertEqual(values[3]["hasGroupMultiOrder"], False)
        self.assertEqual(values[4]["hasGroupMultiOrder"], True)

        self.assertEqual(values[0]["hasGroupDeleteOrder"], True)
        self.assertEqual(values[1]["hasGroupDeleteOrder"], False)
        self.assertEqual(values[2]["hasGroupDeleteOrder"], False)
        self.assertEqual(values[3]["hasGroupDeleteOrder"], True)
        self.assertEqual(values[4]["hasGroupDeleteOrder"], True)
