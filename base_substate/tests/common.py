# Copyright 2025 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo_test_helper import FakeModelLoader

from odoo.addons.base.tests.common import BaseCommon


class CommonBaseSubstate(BaseCommon):
    def setUp(self):
        super().setUp()
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()
        from .sale_test import (
            BaseSubstateType,
            LineTest,
            SaleTest,
        )

        self.loader.update_registry(
            (
                SaleTest,
                LineTest,
                BaseSubstateType,
            )
        )

        self.sale_test_model = self.env[SaleTest._name]
        self.sale_line_test_model = self.env[LineTest._name]

        models = self.env["ir.model"].search(
            [
                (
                    "model",
                    "in",
                    ["base.substate.test.sale", "base.substate.test.sale.line"],
                )
            ]
        )
        for model in models:
            # Access record:
            self.env["ir.model.access"].create(
                {
                    "name": f"access {model.name}",
                    "model_id": model.id,
                    "perm_read": 1,
                    "perm_write": 1,
                    "perm_create": 1,
                    "perm_unlink": 1,
                }
            )

    def tearDown(self):
        self.loader.restore_registry()
        super().tearDown()
