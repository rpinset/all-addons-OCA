# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command
from odoo.exceptions import ValidationError

from odoo.addons.base.tests.common import BaseCommon


class TestModule(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set tracking_disable in context
        cls.test_company = cls._create_company(name="Other company")
        cls.main_company = cls.env.company
        cls.demo_user = cls._create_new_internal_user(
            login="internal.user@test.odoo.com",
            company_ids=[
                Command.link(cls.main_company.id),
                Command.link(cls.test_company.id),
            ],
        )

    # Test Section
    def test_01_disable_without_user(self):
        self.test_company.active = False

    def test_02_disable_with_user(self):
        self.demo_user.company_id = self.test_company.id
        with self.assertRaises(ValidationError):
            self.test_company.active = False

    def test_03_disable_current_company(self):
        with self.assertRaises(ValidationError):
            self.main_company.active = False
