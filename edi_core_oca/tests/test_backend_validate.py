# Copyright 2020 ACSONE
# @author: Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64

from odoo_test_helper import FakeModelLoader

from ..exceptions import EDIValidationError
from .common import EDIBackendCommonTestCase


class EDIBackendTestValidateCase(EDIBackendCommonTestCase):
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
        self.exchange_type_in.receive_model_id = self.model
        self.exchange_type_in.process_model_id = self.model
        self.exchange_type_in.input_validate_model_id = self.model
        vals = {
            "model": self.partner._name,
            "res_id": self.partner.id,
            "exchange_file": base64.b64encode(b"1234"),
        }
        self.record_in = self.backend.create_record("test_csv_input", vals)
        vals.pop("exchange_file")
        self.record_out = self.backend.create_record("test_csv_output", vals)
        self.ExecutionAbstractModel.reset_faked("input_validate")
        self.ExecutionAbstractModel.reset_faked("receive")
        self.ExecutionAbstractModel.reset_faked("generate")
        self.ExecutionAbstractModel.reset_faked("output_validate")

    def tearDown(self):
        self.loader.restore_registry()
        super().tearDown()

    def test_receive_validate_record(self):
        self.record_in.write({"edi_exchange_state": "input_pending"})
        self.backend.exchange_receive(self.record_in)
        self.assertTrue(
            self.ExecutionAbstractModel.check_called_for(
                self.record_in, "input_validate"
            )
        )
        self.assertRecordValues(
            self.record_in, [{"edi_exchange_state": "input_received"}]
        )

    def test_receive_validate_record_error(self):
        self.record_in.write({"edi_exchange_state": "input_pending"})
        exc = EDIValidationError("Data seems wrong!")
        self.backend.with_context(test_break_input_validate=exc).exchange_receive(
            self.record_in
        )
        self.assertTrue(
            self.ExecutionAbstractModel.check_called_for(
                self.record_in, "input_validate"
            )
        )
        self.assertRecordValues(
            self.record_in,
            [
                {
                    "edi_exchange_state": "validate_error",
                    "exchange_error": "Data seems wrong!",
                }
            ],
        )
        self.assertIn("Data seems wrong!", self.record_in.exchange_error_traceback)

    def test_receive_validate_record_error_triggers_notify_error(self):
        self.record_in.write({"edi_exchange_state": "input_pending"})
        exc = EDIValidationError("Data seems wrong!")
        conf = self._make_global_error_conf(self.record_in.type_id)
        self.backend.with_context(test_break_input_validate=exc).exchange_receive(
            self.record_in
        )
        # The error event must fire so downstream notifications (e.g.
        # edi_notification_oca activities) are triggered.
        self.assertEqual(conf.description, "error-event-fired")

    def test_generate_validate_record(self):
        self.record_out.write({"edi_exchange_state": "new"})
        self.backend.exchange_generate(self.record_out)
        self.assertTrue(
            self.ExecutionAbstractModel.check_called_for(
                self.record_out, "output_validate"
            )
        )
        self.assertRecordValues(
            self.record_out, [{"edi_exchange_state": "output_pending"}]
        )

    def test_generate_validate_record_error(self):
        self.record_out.write({"edi_exchange_state": "new"})
        exc = EDIValidationError("Data seems wrong!")
        self.backend.with_context(test_break_output_validate=exc).exchange_generate(
            self.record_out
        )
        self.assertTrue(
            self.ExecutionAbstractModel.check_called_for(
                self.record_out, "output_validate"
            )
        )
        self.assertRecordValues(
            self.record_out,
            [
                {
                    "edi_exchange_state": "validate_error",
                    "exchange_error": "Data seems wrong!",
                }
            ],
        )
        self.assertIn("Data seems wrong!", self.record_out.exchange_error_traceback)

    def test_generate_validate_record_error_triggers_notify_error(self):
        self.record_out.write({"edi_exchange_state": "new"})
        exc = EDIValidationError("Data seems wrong!")
        conf = self._make_global_error_conf(self.record_out.type_id)
        self.backend.with_context(test_break_output_validate=exc).exchange_generate(
            self.record_out
        )
        # The error event must fire so downstream notifications (e.g.
        # edi_notification_oca activities) are triggered.
        self.assertEqual(conf.description, "error-event-fired")

    def test_validate_record_error_regenerate(self):
        self.record_out.write({"edi_exchange_state": "new"})
        exc = EDIValidationError("Data seems wrong!")
        self.backend.with_context(test_break_output_validate=exc).exchange_generate(
            self.record_out
        )
        self.assertRecordValues(
            self.record_out,
            [
                {
                    "edi_exchange_state": "validate_error",
                }
            ],
        )
        self.record_out.with_context(fake_output="yeah!").action_regenerate()
        self.assertEqual(self.record_out._get_file_content(), "yeah!")
        self.assertRecordValues(
            self.record_out,
            [
                {
                    "edi_exchange_state": "output_pending",
                }
            ],
        )
