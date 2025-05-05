# Copyright 2018-19 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo_test_helper import FakeModelLoader

from odoo.tests import common


class CommonTierValidation(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Remove this variable in v16 and put instead:
        # from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
        DISABLED_MAIL_CONTEXT = {
            "tracking_disable": True,
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .tier_validation_tester import (
            TierDefinition,
            TierValidationTester,
            TierValidationTester2,
        )

        cls.loader.update_registry(
            (TierValidationTester, TierValidationTester2, TierDefinition)
        )

        cls.test_model = cls.env[TierValidationTester._name]
        cls.test_model_2 = cls.env[TierValidationTester2._name]

        cls.tester_model = cls.env["ir.model"].search(
            [("model", "=", "tier.validation.tester")]
        )
        cls.tester_model_2 = cls.env["ir.model"].search(
            [("model", "=", "tier.validation.tester2")]
        )
        # Create a multi-company
        cls.main_company = cls.env.ref("base.main_company")
        cls.other_company = cls.env["res.company"].create({"name": "My Company"})

        # Access record:
        cls.env["ir.model.access"].create(
            {
                "name": "access.tester",
                "model_id": cls.tester_model.id,
                "perm_read": 1,
                "perm_write": 1,
                "perm_create": 1,
                "perm_unlink": 1,
            }
        )
        cls.env["ir.model.access"].create(
            {
                "name": "access.tester2",
                "model_id": cls.tester_model_2.id,
                "perm_read": 1,
                "perm_write": 1,
                "perm_create": 1,
                "perm_unlink": 1,
            }
        )

        # Create users:
        group_ids = cls.env.ref("base.group_system").ids
        cls.test_user_1 = cls.env["res.users"].create(
            {"name": "John", "login": "test1", "groups_id": [(6, 0, group_ids)]}
        )
        cls.test_user_2 = cls.env["res.users"].create(
            {"name": "Mike", "login": "test2"}
        )
        cls.test_user_3_multi_company = cls.env["res.users"].create(
            {
                "name": "Jane",
                "login": "test3",
                "email": "jane@mycompany.example.com",
                "company_ids": [(6, 0, [cls.main_company.id, cls.other_company.id])],
            }
        )

        # Create tier definitions:
        cls.tier_def_obj = cls.env["tier.definition"]
        cls.tier_definition = cls.tier_def_obj.create(
            {
                "model_id": cls.tester_model.id,
                "review_type": "individual",
                "reviewer_id": cls.test_user_1.id,
                "definition_domain": "[('test_field', '>', 1.0)]",
                "sequence": 30,
            }
        )

        cls.test_record = cls.test_model.create({"test_field": 2.5})
        cls.test_record_2 = cls.test_model_2.create({"test_field": 2.5})

        # Create definition for test 19, 20
        # Main company tier definition
        cls.tier_def_obj.create(
            {
                "model_id": cls.tester_model_2.id,
                "review_type": "individual",
                "reviewer_id": cls.test_user_1.id,
                "definition_domain": "[('test_field', '>=', 1.0)]",
                "approve_sequence": True,
                "sequence": 30,
                "name": "Definition for test 30 - sequence - user 1 - main company",
                "company_id": cls.main_company.id,
            }
        )
        cls.tier_def_obj.create(
            {
                "model_id": cls.tester_model_2.id,
                "review_type": "individual",
                "reviewer_id": cls.test_user_3_multi_company.id,
                "definition_domain": "[('test_field', '>=', 1.0)]",
                "approve_sequence": True,
                "sequence": 20,
                "name": "Definition for test 30 - sequence - user 3 - main company",
                "company_id": cls.main_company.id,
            }
        )
        # Other company tier definition
        cls.tier_def_obj.create(
            {
                "model_id": cls.tester_model_2.id,
                "review_type": "individual",
                "reviewer_id": cls.test_user_3_multi_company.id,
                "definition_domain": "[('test_field', '>=', 1.0)]",
                "approve_sequence": True,
                "sequence": 30,
                "name": "Definition for test 30 - sequence - user 3 - other company",
                "company_id": cls.other_company.id,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        return super(CommonTierValidation, cls).tearDownClass()
