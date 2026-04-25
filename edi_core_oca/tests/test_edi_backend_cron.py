# Copyright 2020 ACSONE
# @author: Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo_test_helper import FakeModelLoader

from odoo.tools import mute_logger

from .common import EDIBackendCommonTestCase

LOGGERS = (
    "odoo.addons.edi_core_oca.models.edi_backend",
    "odoo.addons.queue_job.delay",
    "odoo.addons.edi_exchange_template_oca.models.edi_backend",
)


class EDIBackendTestCronCase(EDIBackendCommonTestCase):
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
        self.partner2 = self.env.ref("base.res_partner_10")
        self.partner3 = self.env.ref("base.res_partner_12")
        self.record1 = self.backend.create_record(
            "test_csv_output", {"model": self.partner._name, "res_id": self.partner.id}
        )
        self.record2 = self.backend.create_record(
            "test_csv_output", {"model": self.partner._name, "res_id": self.partner2.id}
        )
        self.record3 = self.backend.create_record(
            "test_csv_output", {"model": self.partner._name, "res_id": self.partner3.id}
        )
        self.records = self.record1 + self.record1 + self.record3
        self.ExecutionAbstractModel.reset_faked("generate")
        self.ExecutionAbstractModel.reset_faked("send")
        self.ExecutionAbstractModel.reset_faked("check")

    def tearDown(self):
        self.loader.restore_registry()
        super().tearDown()

    @mute_logger(*LOGGERS)
    def test_exchange_generate_new_no_auto(self):
        # No content ready to be sent, no auto-generate, nothing happens
        for rec in self.records:
            self.assertEqual(rec.edi_exchange_state, "new")
        self.backend._cron_check_output_exchange_sync()
        for rec in self.records:
            self.assertEqual(rec.edi_exchange_state, "new")

    @mute_logger(*LOGGERS)
    def test_exchange_generate_new_auto_skip_send(self):
        self.exchange_type_out.exchange_file_auto_generate = True
        # No content ready to be sent, will get the content but not send it
        for rec in self.records:
            self.assertEqual(rec.edi_exchange_state, "new")
        self.backend._cron_check_output_exchange_sync(skip_send=True)
        for rec in self.records:
            self.assertEqual(rec.edi_exchange_state, "output_pending")
            self.assertTrue(
                self.ExecutionAbstractModel.check_called_for(rec, "generate")
            )
            self.assertEqual(
                rec._get_file_content(), self.ExecutionAbstractModel._call_key(rec)
            )
            # TODO: test better?
            self.assertFalse(rec.ack_exchange_id)

    def _test_generate_new_auto_send(self, records):
        for rec in records:
            self.assertEqual(rec.edi_exchange_state, "output_sent")
            self.assertTrue(
                self.ExecutionAbstractModel.check_called_for(rec, "generate")
            )
            self.assertEqual(
                rec._get_file_content(), self.ExecutionAbstractModel._call_key(rec)
            )
            self.assertTrue(self.ExecutionAbstractModel.check_called_for(rec, "send"))

    @mute_logger(*LOGGERS)
    def test_exchange_generate_new_auto_send(self):
        self.exchange_type_out.exchange_file_auto_generate = True
        # No content ready to be sent, will get the content and send it
        for rec in self.records:
            self.assertEqual(rec.edi_exchange_state, "new")
        self.backend._cron_check_output_exchange_sync()
        self._test_generate_new_auto_send(self.records)

    @mute_logger(*LOGGERS)
    def test_exchange_generate_new_quick_exec_skip_cron(self):
        self.exchange_type_out.exchange_file_auto_generate = True
        self.exchange_type_out.quick_exec = True
        for rec in self.records:
            self.assertEqual(rec.edi_exchange_state, "new")
        # Records w/ quick exec should be skipped by the cron
        self.backend._cron_check_output_exchange_sync()
        for rec in self.records:
            self.assertEqual(rec.edi_exchange_state, "new")

    @mute_logger(*LOGGERS)
    def test_exchange_generate_output_ready_auto_send(self):
        # No content ready to be sent, will get the content and send it
        self.exchange_type_out.check_model_id = self.model
        for rec in self.records:
            self.assertEqual(rec.edi_exchange_state, "new")
        self.record1._set_file_content("READY")
        self.record1.edi_exchange_state = "output_sent"
        self.backend.with_context(
            fake_update_values={"edi_exchange_state": "output_sent_and_processed"}
        )._cron_check_output_exchange_sync(skip_sent=False)
        for rec in self.records - self.record1:
            self.assertEqual(rec.edi_exchange_state, "new")
        self.assertEqual(self.record1.edi_exchange_state, "output_sent_and_processed")
        self.assertTrue(
            self.ExecutionAbstractModel.check_not_called_for(self.record1, "generate")
        )
        self.assertTrue(
            self.ExecutionAbstractModel.check_not_called_for(self.record1, "send")
        )
        self.assertTrue(
            self.ExecutionAbstractModel.check_called_for(self.record1, "check")
        )
