# Copyright 2020 ACSONE
# @author: Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from freezegun import freeze_time
from odoo_test_helper import FakeModelLoader

from odoo.addons.edi_core_oca.exceptions import EDINotImplementedError

from .common import EDIBackendCommonTestCase


class EDIBackendTestCaseBase(EDIBackendCommonTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.default_record = cls.backend.create_record(
            "test_csv_input",
            {"model": cls.partner._name, "res_id": cls.partner.id},
        )

    def setUp(self):
        super().setUp()
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()
        from .fake_models import EdiTestExecution

        self.loader.update_registry((EdiTestExecution,))
        self.ExecutionAbstractModel = self.env["edi.framework.test.execution"]
        self.model = self.env["ir.model"]._get("edi.framework.test.execution")
        self.exchange_type_in.receive_model_id = self.model
        self.exchange_type_in.process_model_id = self.model
        self.exchange_type_in.input_validate_model_id = self.model

    def tearDown(self):
        self.loader.restore_registry()
        super().tearDown()

    @freeze_time("2020-10-21 10:00:00")
    def test_create_record(self):
        self.env.user.tz = None  # Have no timezone used in generated filename
        vals = {
            "model": self.partner._name,
            "res_id": self.partner.id,
        }
        record = self.backend.create_record("test_csv_input", vals)
        expected = {
            "type_id": self.exchange_type_in.id,
            "edi_exchange_state": "new",
            "exchange_filename": "EDI_EXC_TEST-test_csv_"
            "input-2020-10-21-10-00-00.csv",
        }
        self.assertRecordValues(record, [expected])
        self.assertEqual(record.record, self.partner)
        self.assertEqual(record.edi_exchange_state, "new")

    def test_action_view_exchanges(self):
        # Just testing is not broken
        self.assertTrue(self.backend.action_view_exchanges())

    def test_action_view_exchange_types(self):
        # Just testing is not broken
        self.assertTrue(self.backend.action_view_exchange_types())

    def _test_get_handler(self, user=None):
        backend = self.backend
        if user:
            backend = self.backend.with_user(user)
        vals = {
            "model": self.partner._name,
            "res_id": self.partner.id,
        }
        record = backend.create_record("test_csv_input", vals)
        for action in ["receive", "input_validate", "process"]:
            self.assertEqual(
                str(backend._get_exec_handler(record, action)),
                str(getattr(self.ExecutionAbstractModel, action)),
            )

    def test_get_handler_admin(self):
        self._test_get_handler()

    def test_get_handler_avg_user(self):
        user = (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            .create({"name": "Test User EDI", "login": "test_edi_perm_user"})
        )
        self._test_get_handler(user=user)

    def test_get_handler_no_handler(self):
        self.exchange_type_in.process_model_id = False
        self.exchange_type_in.input_validate_model_id = False
        self.exchange_type_in.receive_model_id = False
        vals = {
            "model": self.partner._name,
            "res_id": self.partner.id,
        }
        record = self.backend.create_record("test_csv_input", vals)
        for action in ["receive", "input_validate", "process"]:
            with self.assertRaises(EDINotImplementedError):
                self.backend._get_exec_handler(record, action)

    # ---- conf / env_ctx resolution ------------------------------------------

    def test_get_conf_for_record(self):
        """`_get_conf_for_record` returns the action conf, or {} when missing."""
        self.exchange_type_in.advanced_settings_edit = (
            "execution_model:\n"
            "  receive:\n"
            "    env_ctx:\n"
            "      foo: bar\n"
            "    other_key: 1\n"
        )
        record = self.default_record
        # Action declared -> its conf
        self.assertEqual(
            self.backend._get_conf_for_record(record, "receive"),
            {"env_ctx": {"foo": "bar"}, "other_key": 1},
        )
        # Action not declared -> empty
        self.assertEqual(self.backend._get_conf_for_record(record, "process"), {})

    def test_get_record_env_ctx(self):
        """`_get_record_env_ctx` returns env_ctx for the action, else {}."""
        self.exchange_type_in.advanced_settings_edit = (
            "execution_model:\n"
            "  receive:\n"
            "    env_ctx:\n"
            "      foo: bar\n"
            "      flag: true\n"
            "  process:\n"
            "    other_key: 1\n"
        )
        record = self.default_record
        # Action with env_ctx -> mapping
        self.assertEqual(
            self.backend._get_record_env_ctx(record, "receive"),
            {"foo": "bar", "flag": True},
        )
        # Action present but no env_ctx -> empty
        self.assertEqual(self.backend._get_record_env_ctx(record, "process"), {})

    def test_get_exec_handler_propagates_env_ctx(self):
        """The handler returned by `_get_exec_handler` carries env_ctx keys."""
        self.exchange_type_in.advanced_settings_edit = (
            "execution_model:\n"
            "  receive:\n"
            "    env_ctx:\n"
            "      edi_test_marker: hello\n"
            "      edi_test_flag: true\n"
        )
        record = self.default_record
        handler = self.backend._get_exec_handler(record, "receive")
        ctx = handler.__self__.env.context
        self.assertEqual(ctx.get("edi_test_marker"), "hello")
        self.assertEqual(ctx.get("edi_test_flag"), True)
        # Action without env_ctx -> handler context not polluted
        handler_proc = self.backend._get_exec_handler(record, "process")
        self.assertNotIn("edi_test_marker", handler_proc.__self__.env.context)
