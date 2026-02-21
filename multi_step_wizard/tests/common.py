# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo_test_helper import FakeModelLoader

from odoo.tests import common


class CommonTestMultiStepWizard(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()
        from .multi_step_wizard_test import MultiStepWizardTest

        self.loader.update_registry((MultiStepWizardTest,))

    def tearDown(self):
        self.loader.restore_registry()
        return super().tearDownClass()
