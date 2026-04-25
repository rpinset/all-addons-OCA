# Copyright 2023 Camptocamp SA
# @author: Simone Orsi <simahawk@gmail.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo_test_helper import FakeModelLoader

from odoo import exceptions

from odoo.addons.edi_core_oca.tests.common import EDIBackendCommonTestCase


class TestEDIState(EDIBackendCommonTestCase):
    def setUp(self):
        super().setUp()
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()
        from .fake_models import EDIStateConsumerFake

        self.loader.update_registry((EDIStateConsumerFake,))
        self.consumer_model = self.env[EDIStateConsumerFake._name]
        self.consumer_record = self.consumer_model.create(
            {
                "name": "State Test Consumer",
            }
        )
        # Suitable workflow
        self.wf1_ok = self.env["edi.state.workflow"].create(
            {
                "name": "WF1",
                "backend_type_id": self.backend.backend_type_id.id,
                "model_id": self.env["ir.model"]._get(self.consumer_record._name).id,
            }
        )
        for i in range(1, 4):
            self.env["edi.state"].create(
                {"name": f"OK {i}", "code": f"OK_{i}", "workflow_id": self.wf1_ok.id}
            )
        # Non suitable workflow
        self.wf2_ko = self.env["edi.state.workflow"].create(
            {
                "name": "WF2",
                "backend_type_id": self.backend.backend_type_id.id,
                "model_id": self.env["ir.model"]._get("res.partner").id,
            }
        )
        for i in range(1, 4):
            self.env["edi.state"].create(
                {"name": f"KO {i}", "code": f"KO_{i}", "workflow_id": self.wf2_ko.id}
            )
        self.exc_type = self._create_exchange_type(
            name="State test",
            code="state_test",
            direction="output",
            state_workflow_ids=[(6, 0, self.wf1_ok.ids)],
        )
        vals = {
            "model": self.consumer_record._name,
            "res_id": self.consumer_record.id,
        }
        record = self.backend.create_record("state_test", vals)
        self.consumer_record._edi_set_origin(record)

    def tearDown(self):
        self.loader.restore_registry()
        super().tearDown()

    def test_is_state_valid(self):
        self.assertTrue(self.wf1_ok.is_valid_for_model(self.consumer_model._name))
        self.assertFalse(self.wf1_ok.is_valid_for_model("res.partner"))
        self.assertFalse(self.wf2_ko.is_valid_for_model(self.consumer_model._name))
        self.assertTrue(self.wf2_ko.is_valid_for_model("res.partner"))

    def test_mixin_edi_set_state(self):
        self.assertFalse(self.consumer_record.edi_state_id)
        self.assertFalse(self.consumer_record.edi_state_workflow_id)
        for state in self.wf1_ok.state_ids:
            self.consumer_record._edi_set_state(state)
            self.assertEqual(self.consumer_record.edi_state_id, state)
        for state in self.wf2_ko.state_ids:
            with self.assertRaisesRegex(
                exceptions.UserError,
                rf"State {state.name} \[{state.code}\] not allowed",
            ):
                self.consumer_record._edi_set_state(state)
        self.assertEqual(
            self.consumer_record.edi_find_state(code="OK_1"), self.wf1_ok.state_ids[0]
        )

    def test_mixin_edi_set_state_no_origin_pass_gracefully(self):
        self.consumer_record.origin_exchange_record_id = False
        logger_name = "odoo.addons.edi_state_oca.models.edi_state_consumer_mixin"
        with self.assertLogs(logger_name, level="WARN") as logs:
            self.consumer_record._edi_set_state(self.wf1_ok.state_ids[0])
            err = (
                f"No exchange type given for "
                f"{self.consumer_record._name}#{self.consumer_record.id}"
            )
            self.assertIn(err, logs.output[0])

    def test_mixin_edi_find_state(self):
        with self.assertRaises(AssertionError):
            self.assertEqual(self.consumer_model.edi_find_state())
        self.assertEqual(
            self.consumer_record.edi_find_state(code="OK_1"), self.wf1_ok.state_ids[0]
        )
        self.wf1_ok.state_ids[1].is_default = True
        self.assertEqual(
            self.consumer_record.edi_find_state(default=True), self.wf1_ok.state_ids[1]
        )

    def test_check_is_default(self):
        self.wf2_ko.state_ids[0].is_default = True
        with self.assertRaisesRegex(
            exceptions.UserError, "Only one state per workflow"
        ):
            self.wf2_ko.state_ids[1].is_default = True

    def test_get_state(self):
        self.assertEqual(self.wf1_ok.get_state("OK_1"), self.wf1_ok.state_ids[0])
        self.assertEqual(self.wf1_ok.get_state("OK_2"), self.wf1_ok.state_ids[1])
        self.assertEqual(self.wf1_ok.get_state("OK_10"), self.wf1_ok.state_ids.browse())

    def test_get_state_for_model(self):
        self.assertEqual(
            self.exc_type.get_state_for_model(self.consumer_model._name, "OK_1"),
            self.wf1_ok.state_ids[0],
        )
        self.assertEqual(
            self.exc_type.get_state_for_model(self.consumer_model._name, "OK_2"),
            self.wf1_ok.state_ids[1],
        )
        self.assertEqual(
            self.exc_type.get_state_for_model("res.partner", "KO_2"),
            self.wf2_ko.state_ids.browse(),
        )
        self.exc_type.state_workflow_ids += self.wf2_ko
        self.assertEqual(
            self.exc_type.get_state_for_model("res.partner", "KO_2"),
            self.wf2_ko.state_ids[1],
        )

    def test_exc_type_one_wf_per_model(self):
        with self.assertRaisesRegex(
            exceptions.UserError, "Only one workflow per model is allowed"
        ):
            self.exc_type.state_workflow_ids += self.wf1_ok.copy()
