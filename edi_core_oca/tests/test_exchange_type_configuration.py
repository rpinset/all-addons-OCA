# Copyright 2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo_test_helper import FakeModelLoader

from .common import EDIBackendCommonTestCase


class EDIBackendTestOutputCase(EDIBackendCommonTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        vals = {
            "model": cls.partner._name,
            "res_id": cls.partner.id,
        }
        cls.record = cls.backend.create_record("test_csv_output", vals)

    def setUp(self):
        super().setUp()
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()
        from .fake_models import EdiTestExecution, EdiTestExecutionExtra

        self.loader.update_registry((EdiTestExecution, EdiTestExecutionExtra))
        self.ExecutionAbstractModel = self.env["edi.framework.test.execution"]
        self.ExecutionAbstractModelExtra = self.env[
            "edi.framework.test.execution.extra"
        ]
        self.model = self.env["ir.model"].search(
            [("model", "=", "edi.framework.test.execution")]
        )
        self.exchange_type_out.generate_model_id = self.model
        self.exchange_type_out.send_model_id = self.model
        self.ExecutionAbstractModel.reset_faked("generate")
        self.ExecutionAbstractModelExtra.reset_faked("validate")

    def tearDown(self):
        self.loader.restore_registry()
        super().tearDown()

    def test_multiple_configuration(self):
        vals = {
            "model": self.partner._name,
            "res_id": self.partner.id,
        }
        record = self.backend.create_record("test_csv_output", vals)
        record.type_id.generate_model_id = self.env["ir.model"].search(
            [("model", "=", "edi.framework.test.execution.extra")]
        )
        record.action_exchange_generate()
        self.assertFalse(
            self.ExecutionAbstractModel.check_called_for(record, "generate")
        )
        self.assertTrue(
            self.ExecutionAbstractModelExtra.check_called_for(record, "generate")
        )
