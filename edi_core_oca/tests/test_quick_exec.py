# Copyright 2022 Camptocamp SA
# @author: Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from unittest import mock

from odoo_test_helper import FakeModelLoader

from odoo.tools import mute_logger

from .common import EDIBackendCommonTestCase

LOGGERS = (
    "odoo.addons.edi_core_oca.models.edi_backend",
    "odoo.addons.queue_job.delay",
    "odoo.addons.edi_exchange_template_oca.models.edi_backend",
)


class EDIQuickExecTestCase(EDIBackendCommonTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner2 = cls.env.ref("base.res_partner_10")
        cls.partner3 = cls.env.ref("base.res_partner_12")

    def setUp(self):
        super().setUp()
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()
        from .fake_models import EdiTestExecution

        self.loader.update_registry((EdiTestExecution,))
        self.ExecutionAbstractModel = self.env["edi.framework.test.execution"]
        self.model = self.env["ir.model"].search(
            [("model", "=", "edi.framework.test.execution")]
        )
        self.exchange_type_out.generate_model_id = self.model
        self.exchange_type_out.send_model_id = self.model
        self.exchange_type_out.output_validate_model_id = self.model
        self.exchange_type_in.generate_model_id = self.model
        self.exchange_type_in.process_model_id = self.model
        self.exchange_type_in.input_validate_model_id = self.model
        self.ExecutionAbstractModel.reset_faked("generate")
        self.ExecutionAbstractModel.reset_faked("send")
        self.ExecutionAbstractModel.reset_faked("check")
        self.ExecutionAbstractModel.reset_faked("process")

    def tearDown(self):
        self.loader.restore_registry()
        super().tearDown()

    @mute_logger(*LOGGERS)
    def test_quick_exec_on_create_no_call(self):
        vals = {
            "model": self.partner._name,
            "res_id": self.partner.id,
        }
        model = self.env["edi.exchange.record"]
        # quick exec is off, we should not get any call
        with mock.patch.object(type(model), "_execute_next_action") as mocked:
            record0 = self.backend.create_record("test_csv_output", vals)
            mocked.assert_not_called()
            self.assertEqual(record0.edi_exchange_state, "new")
        # enabled but bypassed
        self.exchange_type_out.exchange_file_auto_generate = True
        self.exchange_type_out.quick_exec = True
        with mock.patch.object(type(model), "_execute_next_action") as mocked:
            record0 = self.backend.with_context(
                edi__skip_quick_exec=True
            ).create_record("test_csv_output", vals)
            # quick exec is off, we should not get any call
            mocked.assert_not_called()
            self.assertEqual(record0.edi_exchange_state, "new")

    @mute_logger(*LOGGERS)
    def test_quick_exec_on_create_out(self):
        self.exchange_type_out.exchange_file_auto_generate = True
        self.exchange_type_out.quick_exec = True
        vals = {
            "model": self.partner._name,
            "res_id": self.partner.id,
        }
        record0 = self.backend.create_record("test_csv_output", vals)
        # File generated and sent!
        self.assertEqual(record0.edi_exchange_state, "output_sent")
        self.assertTrue(
            self.ExecutionAbstractModel.check_called_for(record0, "generate")
        )
        self.assertEqual(
            record0._get_file_content(), self.ExecutionAbstractModel._call_key(record0)
        )

    @mute_logger(*LOGGERS)
    def test_quick_exec_on_create_in(self):
        self.exchange_type_in.quick_exec = True
        vals = {
            "model": self.partner._name,
            "res_id": self.partner.id,
            "exchange_file": base64.b64encode(b"1234"),
            "edi_exchange_state": "input_received",
        }
        record0 = self.backend.create_record("test_csv_input", vals)
        self.assertEqual(record0.edi_exchange_state, "input_processed")
        self.assertTrue(
            self.ExecutionAbstractModel.check_called_for(record0, "process")
        )

    @mute_logger(*LOGGERS)
    def test_quick_exec_on_retry(self):
        self.exchange_type_in.quick_exec = True
        vals = {
            "model": self.partner._name,
            "res_id": self.partner.id,
            "edi_exchange_state": "input_processed_error",
            "exchange_file": base64.b64encode(b"1234"),
        }
        record0 = self.backend.with_context(edi__skip_quick_exec=True).create_record(
            "test_csv_input", vals
        )
        self.assertEqual(record0.edi_exchange_state, "input_processed_error")
        self.assertTrue(record0.retryable)
        # get record w/ a clean context
        record0 = self.backend.exchange_record_model.browse(record0.id)
        record0.action_retry()
        # The file has been rolled back and processed right away
        self.assertEqual(record0.edi_exchange_state, "input_processed")
        self.assertTrue(
            self.ExecutionAbstractModel.check_called_for(record0, "process")
        )
