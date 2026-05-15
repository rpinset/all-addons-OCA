# Copyright 2020 Ecosoft (http://ecosoft.co.th)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.orm.model_classes import add_to_registry
from odoo.tests.common import tagged

from odoo.addons.base_tier_validation.tests.common import CommonTierValidation


@tagged("post_install", "-at_install")
class TierTierValidation(CommonTierValidation):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from .tier_validation_tester import TierValidationTester

        add_to_registry(cls.registry, TierValidationTester)
        cls.registry._setup_models__(cls.env.cr, ["tier.validation.tester"])
        cls.registry.init_models(
            cls.env.cr,
            ["tier.validation.tester"],
            {"models_to_check": True},
        )

    def _setup_tier_definitions(self):
        self.tier_def_obj.create(
            {
                "model_id": self.tester_model.id,
                "review_type": "individual",
                "reviewer_id": self.test_user_1.id,
                "definition_domain": "[('test_field', '>', 1.0)]",
                "sequence": 30,
            }
        )

    def test_1_auto_validation(self):
        # Create new test record
        test_record = self.test_model.create({"test_field": 2.5})
        # Create tier definitions
        self.tier_def_obj.create(
            {
                "model_id": self.tester_model.id,
                "review_type": "individual",
                "reviewer_id": self.test_user_1.id,
                "sequence": 20,
                "approve_sequence": True,
                "auto_validate": True,
            }
        )
        self.tier_def_obj.create(
            {
                "model_id": self.tester_model.id,
                "review_type": "individual",
                "reviewer_id": self.test_user_1.id,
                "sequence": 10,
                "approve_sequence": True,
                "auto_validate": True,
                "auto_validate_domain": "[('test_field', '>', 3)]",
            }
        )
        # Request validation
        reviews = test_record.with_user(self.test_user_2).request_validation()
        reviews._update_review_status()
        record = test_record.with_user(self.test_user_1)
        record.invalidate_recordset()
        # Auto validate, 1st tier, not auto validated
        self.tier_def_obj._cron_auto_tier_validation()
        self.assertEqual(
            record.review_ids.mapped("status"), ["pending", "waiting", "waiting"]
        )
        # Manual validate 2nd tier -> OK
        record.validate_tier()
        self.assertEqual(
            record.review_ids.mapped("status"), ["approved", "pending", "waiting"]
        )
        # Auto validate, 2nd tier -> OK
        self.tier_def_obj._cron_auto_tier_validation()
        self.assertEqual(
            record.review_ids.mapped("status"), ["approved", "approved", "pending"]
        )
        # Auto validate, 3rd tier -> Not pass validate domain
        self.tier_def_obj._cron_auto_tier_validation()
        self.assertEqual(
            record.review_ids.mapped("status"), ["approved", "approved", "pending"]
        )
        # Manual validate 3rd tier -> OK
        record.validate_tier()
        self.assertEqual(
            record.review_ids.mapped("status"), ["approved", "approved", "approved"]
        )

    def test_2_auto_validation_exception(self):
        # Create new test record
        test_record = self.test_model.create({"test_field": 2.5})
        # Create tier definitions
        self.tier_def_obj.create(
            {
                "model_id": self.tester_model.id,
                "review_type": "individual",
                "reviewer_group_id": self.test_group.id,
                "sequence": 20,
                "approve_sequence": True,
                "auto_validate": True,
            }
        )
        # Request validation
        reviews = test_record.with_user(self.test_user_2).request_validation()
        reviews._update_review_status()
        record = test_record.with_user(self.test_user_1)
        record.invalidate_recordset()
        # Auto validate, 1st tier, not auto validated
        with self.assertLogs(
            "odoo.addons.base_tier_validation_server_action.models.tier_definition",
            level="WARNING",
        ):
            self.tier_def_obj._cron_auto_tier_validation()
        self.assertEqual(record.review_ids.mapped("status"), ["pending", "waiting"])
        # Manual validate 2nd tier -> OK
        record.validate_tier()
        self.assertEqual(record.review_ids.mapped("status"), ["approved", "pending"])
        # Auto validate, 2nd tier -> Not OK, before len(reviewers) > 1
        with self.assertLogs(
            "odoo.addons.base_tier_validation_server_action.models.tier_definition",
            level="WARNING",
        ):
            self.tier_def_obj._cron_auto_tier_validation()
        self.assertEqual(record.review_ids.mapped("status"), ["approved", "pending"])

    def test_3_trigger_server_action(self):
        # Create new test record
        test_record = self.test_model.create({"test_field": 2.5})
        # Create server action
        server_action = self.env["ir.actions.server"].create(
            {
                "name": "Set test_bool = True",
                "model_id": self.tester_model.id,
                "state": "code",
                "code": "record.write({'test_bool': True})",
            }
        )
        # Create tier definitions
        self.tier_def_obj.create(
            {
                "model_id": self.tester_model.id,
                "review_type": "individual",
                "reviewer_id": self.test_user_1.id,
                "sequence": 20,
                "server_action_id": server_action.id,  # Server Action
            }
        )
        # Request validation
        reviews = test_record.with_user(self.test_user_2).request_validation()
        reviews._update_review_status()
        record = test_record.with_user(self.test_user_1)
        record.invalidate_recordset()
        record.validate_tier()
        self.assertTrue(record.test_bool)

    def test_4_trigger_rejected_server_action(self):
        # Create new test record
        test_record = self.test_model.create({"test_field": 2.5})
        # Create rejected server action
        rejected_server_action = self.env["ir.actions.server"].create(
            {
                "name": "Set test_bool = True",
                "model_id": self.tester_model.id,
                "state": "code",
                "code": "record.write({'test_bool': True})",
            }
        )
        # Create tier definitions
        self.tier_def_obj.create(
            {
                "model_id": self.tester_model.id,
                "review_type": "individual",
                "reviewer_id": self.test_user_1.id,
                "sequence": 20,
                "rejected_server_action_id": rejected_server_action.id,
            }
        )
        # Request rejection
        reviews = test_record.with_user(self.test_user_2).request_validation()
        reviews._update_review_status()
        record = test_record.with_user(self.test_user_1)
        record.invalidate_recordset()
        record.reject_tier()
        self.assertTrue(record.test_bool)
