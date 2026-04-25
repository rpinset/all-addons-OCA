from odoo.tests import tagged

from odoo.addons.point_of_sale.tests.test_frontend import TestPointOfSaleHttpCommon


@tagged("post_install", "-at_install")
class TestPosSupplierInfoVisibility(TestPointOfSaleHttpCommon):
    def _create_user(self, login, groups):
        return (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "name": login,
                    "login": login,
                    "email": f"{login}@example.com",
                    "groups_id": [(6, 0, groups)],
                }
            )
        )

    def test_supplier_section_hidden_for_non_manager(self):
        base_user = self.env.ref("base.group_user").id
        pos_user_group = self.env.ref("point_of_sale.group_pos_user").id
        user = self._create_user("pos_cashier_test", [base_user, pos_user_group])

        self.start_tour(
            "/pos/ui?config_id=%d" % self.main_pos_config.id,
            "pos_supplier_info_hidden_for_non_manager",
            login=user.login,
        )

    def test_supplier_section_visible_for_manager(self):
        base_user = self.env.ref("base.group_user").id
        pos_manager = self.env.ref("point_of_sale.group_pos_manager").id
        user = self._create_user("pos_manager_test", [base_user, pos_manager])

        self.start_tour(
            "/pos/ui?config_id=%d" % self.main_pos_config.id,
            "pos_supplier_info_visible_for_manager",
            login=user.login,
        )
