# Copyright 2023-2024 Tecnativa - Víctor Martínez
# Copyright 2025 - APSL-Nagarro - Miquel Alzanillas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import new_test_user

from odoo.addons.base.tests.common import BaseCommon


class TestAgreementSignOca(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.template = cls.env.ref(
            "agreement_sign_oca.sign_oca_template_agreement_legal_demo"
        )
        cls.model_agreement = cls.env.ref("agreement.model_agreement")
        cls.user_a = new_test_user(
            cls.env,
            login="test-user-a",
            groups="{},{},{}".format(
                "agreement_legal.group_agreement_manager",
                "sign_oca.sign_oca_group_user",
                "base.group_partner_manager",
            ),
        )
        # Create a partner for the test agreement
        cls.partner_a = cls.env["res.partner"].create(
            {"name": "Test Partner A", "email": "partner.a@test.com"}
        )
        cls.subpartner_a = cls.env["res.partner"].create(
            {
                "name": "SubPartner A",
                "email": "sub.partner.a@test.com",
                "parent_id": cls.partner_a.id,
            }
        )
        cls.company_signatory_person = cls.env["res.partner"].create(
            {
                "name": "Company Signatory",
                "email": "company.signer@test.com",
                "parent_id": cls.env.company.partner_id.id,
            }
        )
        cls.user_company = new_test_user(
            cls.env,
            login="test-user-company-signatory",
            partner_id=cls.company_signatory_person.id,
            groups="base.group_no_one",
        )
        # Set a default to make it compatible with hr_maintenance
        cls.agreement_model = cls.env["agreement"].with_context(
            default_agreement_assign_to="other"
        )
        cls.agreement_a = cls.agreement_model.with_user(cls.user_a).create(
            {
                "name": "Test agreement A",
                "assigned_user_id": cls.user_a.id,
                "partner_id": cls.partner_a.id,  # Assign partner
                "partner_contact_id": cls.subpartner_a.id,
                "company_contact_id": cls.company_signatory_person.id,
            }
        )
        cls.user_b = new_test_user(
            cls.env,
            login="test-user-b",
            groups="{},{},{}".format(
                "agreement_legal.group_agreement_manager",
                "sign_oca.sign_oca_group_user",
                "base.group_partner_manager",
            ),
        )
        cls.partner_b = cls.env["res.partner"].create(
            {"name": "Test Partner B", "email": "partner.b@test.com"}
        )
        cls.subpartner_b = cls.env["res.partner"].create(
            {
                "name": "SubPartner B",
                "email": "sub.partner.b@test.com",
                "parent_id": cls.partner_b.id,
            }
        )
        cls.agreement_b = cls.agreement_model.with_user(cls.user_b).create(
            {
                "name": "Test agreement B",
                "assigned_user_id": cls.user_b.id,
                "partner_id": cls.partner_b.id,
                "partner_contact_id": cls.subpartner_b.id,
                "company_contact_id": cls.company_signatory_person.id,
            }
        )
        cls.active_stage = cls.env["agreement.stage"].create(
            {"name": "Active", "stage_type": "agreement"}
        )
        cls.company.agreement_sign_oca_signed_stage_id = cls.active_stage.id

    def test_action_send_for_signature(self):
        """Test the action to send an agreement for signature (success case)."""
        self.assertEqual(self.agreement_a.sign_request_count, 0)
        action = self.agreement_a.action_send_for_signature()
        self.sign_request = self.env["sign.oca.request"].browse(action["res_id"])
        self.assertEqual(self.agreement_a.sign_request_count, 1)
        self.assertEqual(
            self.sign_request.id, self.sign_request.agreement_id.sign_request_ids.id
        )
        self.assertEqual(action["views"][0][1], "form")
        sign_request = self.agreement_a.sign_request_ids
        self.assertTrue(sign_request)
        self.assertEqual(sign_request.name, self.agreement_a.name)
        self.assertTrue(sign_request.data)
        self.assertEqual(len(sign_request.signer_ids), 2)
        self.assertIn(self.subpartner_a, sign_request.signer_ids.mapped("partner_id"))
        self.assertIn(
            self.company_signatory_person, sign_request.signer_ids.mapped("partner_id")
        )

    def test_action_send_for_signature_no_partner(self):
        """Test that the action raises an error if the agreement has no partner."""
        agreement_no_partner = self.agreement_model.create(
            {
                "name": "Test agreement no partner",
            }
        )
        with self.assertRaises(
            UserError, msg="The agreement must have an assigned contact (counterparty)."
        ):
            agreement_no_partner.action_send_for_signature()

    def test_action_send_for_signature_no_partner_email(self):
        """Test that the action raises an error if the partner has no email."""
        self.agreement_a.partner_contact_id.email = False
        with self.assertRaises(
            UserError,
            msg="""The agreement's counterparty contact
            does not have an email configured.""",
        ):
            self.agreement_a.action_send_for_signature()
        # Restore email for other tests
        self.agreement_a.partner_contact_id.email = "partner.a@test.com"
        # Test missing contact
        self.agreement_a.partner_contact_id = False
        with self.assertRaises(ValidationError):
            self.agreement_a.action_send_for_signature()

    def test_action_send_signed_request(self):
        """Test that when a request is signed, the agreement is updated."""
        dummy_pdf_content = base64.b64encode(b"This is a signed PDF.")
        customer_role = self.env.ref("sign_oca.sign_role_customer")
        company_signer_role = self.env.ref("agreement_sign_oca.role_agreement_signer")
        sign_request = self.env["sign.oca.request"].create(
            {
                "data": dummy_pdf_content,
                "name": "Signed Agreement A.pdf",
                "record_ref": f"agreement,{self.agreement_a.id}",
                "state": "0_sent",
                "signer_ids": [
                    (
                        0,
                        0,
                        {
                            "role_id": customer_role.id,
                            "partner_id": self.subpartner_a.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "role_id": company_signer_role.id,
                            "partner_id": self.company_signatory_person.id,
                        },
                    ),
                ],
            }
        )
        # Simulate signing
        for signer in sign_request.signer_ids:
            signer.signed_on = "2023-01-01 12:00:00"
        sign_request.state = "2_signed"
        self.assertNotEqual(self.agreement_a.stage_id, self.active_stage)
        sign_request.action_send_signed_request()
        self.assertEqual(self.agreement_a.stage_id, self.active_stage)
        self.assertEqual(self.agreement_a.signed_contract, dummy_pdf_content)
        self.assertEqual(self.agreement_a.signed_contract_filename, sign_request.name)
        self.assertTrue(self.agreement_a.partner_signed_date)
        self.assertEqual(self.agreement_a.partner_signed_user_id, self.subpartner_a)
        self.assertTrue(self.agreement_a.company_signed_date)
        self.assertEqual(self.agreement_a.company_signed_user_id, self.user_company)

    def test_action_send_signed_request_state_not_signed(self):
        """Test that agreement is not updated if request is not signed."""
        sign_request = self.env["sign.oca.request"].create(
            {
                "data": base64.b64encode(b"PDF content"),
                "name": "Test.pdf",
                "record_ref": f"agreement,{self.agreement_a.id}",
                "state": "0_sent",  # Not signed
            }
        )
        original_stage = self.agreement_a.stage_id
        sign_request.action_send_signed_request()
        self.assertEqual(self.agreement_a.stage_id, original_stage)
        self.assertFalse(self.agreement_a.signed_contract)

    def test_action_send_signed_request_no_agreement(self):
        """Test that nothing happens if request has no agreement."""
        sign_request = self.env["sign.oca.request"].create(
            {
                "data": base64.b64encode(b"PDF content"),
                "name": "Test.pdf",
                "record_ref": False,  # No agreement
                "state": "2_signed",
            }
        )
        # This should not raise an error and not modify any agreement
        sign_request.action_send_signed_request()
        # Check that agreement_a is untouched
        self.assertFalse(self.agreement_a.signed_contract)

    def test_action_send_signed_request_no_data(self):
        """Test that agreement is not updated if request has no data."""
        sign_request = self.env["sign.oca.request"].create(
            {
                "data": False,  # No data
                "name": "Test.pdf",
                "record_ref": f"agreement,{self.agreement_a.id}",
                "state": "2_signed",
            }
        )
        original_stage = self.agreement_a.stage_id
        sign_request.action_send_signed_request()
        self.assertEqual(self.agreement_a.stage_id, original_stage)
        self.assertFalse(self.agreement_a.signed_contract)

    def test_action_send_signed_request_company_signer_no_user(self):
        """Test when company signer partner has no user."""
        company_signer_no_user = self.env["res.partner"].create(
            {
                "name": "Company Signer No User",
                "email": "signer.no.user@test.com",
                "parent_id": self.env.company.partner_id.id,
            }
        )
        self.assertFalse(company_signer_no_user.user_ids)
        dummy_pdf_content = base64.b64encode(b"This is a signed PDF.")
        customer_role = self.env.ref("sign_oca.sign_role_customer")
        company_signer_role = self.env.ref("agreement_sign_oca.role_agreement_signer")
        sign_request = self.env["sign.oca.request"].create(
            {
                "data": dummy_pdf_content,
                "name": "Signed Agreement A.pdf",
                "record_ref": f"agreement,{self.agreement_a.id}",
                "state": "0_sent",
                "signer_ids": [
                    (
                        0,
                        0,
                        {
                            "role_id": customer_role.id,
                            "partner_id": self.subpartner_a.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "role_id": company_signer_role.id,
                            "partner_id": company_signer_no_user.id,
                        },
                    ),
                ],
            }
        )
        # Simulate signing
        for signer in sign_request.signer_ids:
            signer.signed_on = "2023-01-01 12:00:00"
        sign_request.state = "2_signed"
        sign_request.action_send_signed_request()
        self.assertEqual(self.agreement_a.stage_id, self.active_stage)
        self.assertEqual(self.agreement_a.signed_contract, dummy_pdf_content)
        self.assertTrue(self.agreement_a.partner_signed_date)
        self.assertEqual(self.agreement_a.partner_signed_user_id, self.subpartner_a)
        self.assertTrue(self.agreement_a.company_signed_date)
        # company_signed_user_id should not be set
        self.assertFalse(self.agreement_a.company_signed_user_id)

    def test_action_send_signed_request_only_customer_signer(self):
        """Test when there is only a customer signer."""
        dummy_pdf_content = base64.b64encode(b"This is a signed PDF.")
        customer_role = self.env.ref("sign_oca.sign_role_customer")
        sign_request = self.env["sign.oca.request"].create(
            {
                "data": dummy_pdf_content,
                "name": "Signed Agreement B.pdf",
                "record_ref": f"agreement,{self.agreement_b.id}",
                "state": "0_sent",
                "signer_ids": [
                    (
                        0,
                        0,
                        {
                            "role_id": customer_role.id,
                            "partner_id": self.subpartner_b.id,
                        },
                    ),
                ],
            }
        )
        # Simulate signing
        for signer in sign_request.signer_ids:
            signer.signed_on = "2023-01-01 12:00:00"
        sign_request.state = "2_signed"
        sign_request.action_send_signed_request()
        self.assertEqual(self.agreement_b.stage_id, self.active_stage)
        self.assertEqual(self.agreement_b.signed_contract, dummy_pdf_content)
        self.assertTrue(self.agreement_b.partner_signed_date)
        self.assertEqual(self.agreement_b.partner_signed_user_id, self.subpartner_b)
        # Company fields should not be set
        self.assertFalse(self.agreement_b.company_signed_date)
        self.assertFalse(self.agreement_b.company_signed_user_id)
