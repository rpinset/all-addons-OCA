# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import Command, fields
from odoo.tests.common import tagged, users

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
from odoo.addons.crm.tests import common as crm_common


@tagged("lead_manage")
class TestSupplierRelationshipManagement(crm_common.TestCrmCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.user_sales_salesman.group_ids |= cls.env.ref("purchase.group_purchase_user")
        cls.lead_1.write(
            {
                "user_id": cls.user_sales_salesman.id,
            }
        )
        cls.lead_2 = cls.env["crm.lead"].create(
            {
                "name": "Jimmy Choo Request",
                "type": "lead",
                "user_id": cls.user_sales_leads.id,
                "team_id": cls.sales_team_1.id,
                "partner_id": False,
                "contact_name": "Jimmy Choo",
                "email_from": "jimmy.choo@test.example.com",
                "lang_id": cls.lang_fr.id,
                "phone": "+1 202 555 9999",
                "country_id": cls.env.ref("base.us").id,
                "probability": 20,
            }
        )
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product",
                "list_price": 30.0,
                "standard_price": 30.0,
                "type": "consu",
                "uom_id": cls.uom_unit.id,
                "purchase_ok": True,
            }
        )

        cls._create_crm_purchase_orders(cls.lead_1, cls.contact_company)
        cls._create_crm_purchase_orders(
            cls.lead_2,
            cls.contact_company_1,
            prefix="OTHER",
        )

    @classmethod
    def _create_purchase_order(
        cls, lead, partner, qty, *, state="draft", name_suffix=""
    ):
        po = cls.env["purchase.order"].create(
            {
                "partner_id": partner.id,
                "opportunity_id": lead.id,
                "order_line": [
                    Command.create(
                        {
                            "name": f"{cls.product.name} {name_suffix}".strip(),
                            "product_id": cls.product.id,
                            "product_qty": qty,
                            "product_uom_id": cls.product.uom_id.id,
                            "price_unit": cls.product.list_price,
                            "date_planned": fields.Datetime.now(),
                        }
                    ),
                ],
            }
        )

        if state == "sent":
            po.write({"state": "sent"})
        elif state == "purchase":
            po.button_confirm()
        elif state == "cancel":
            po.button_cancel()

        return po

    @classmethod
    def _create_crm_purchase_orders(cls, lead, partner, prefix="MAIN"):
        cls.rfq_draft = cls._create_purchase_order(
            lead, partner, 1.0, state="draft", name_suffix=f"{prefix} RFQ DRAFT"
        )
        cls.rfq_sent = cls._create_purchase_order(
            lead, partner, 2.0, state="sent", name_suffix=f"{prefix} RFQ SENT"
        )
        cls.po_1 = cls._create_purchase_order(
            lead, partner, 3.0, state="purchase", name_suffix=f"{prefix} PO 1"
        )
        cls.po_2 = cls._create_purchase_order(
            lead, partner, 4.0, state="purchase", name_suffix=f"{prefix} PO 2"
        )
        cls.po_cancel = cls._create_purchase_order(
            lead, partner, 5.0, state="cancel", name_suffix=f"{prefix} PO CANCEL"
        )

    def test_00_lead_purchase_data(self):
        """Test that the lead's purchase data is correctly computed."""
        # RFQs: draft + sent
        self.assertEqual(self.lead_1.request_for_quotation_count, 2)

        # Purchase Orders: confirmed only (draft/sent/cancel excluded)
        self.assertEqual(self.lead_1.purchase_order_count, 2)

        expected_amount = self.po_1.amount_untaxed + self.po_2.amount_untaxed
        self.assertEqual(self.lead_1.purchase_amount_total, expected_amount)

    def test_01_lead_create_request_type_partner(self):
        """Test that a customer is created with specified type."""
        lead_customer = self.lead_1.with_user(self.env.user).copy(
            {
                "request_type": "customer",
            }
        )
        lead_supplier = self.lead_1.with_user(self.env.user).copy(
            {
                "request_type": "supplier",
            }
        )
        customer = lead_customer._create_customer()
        supplier = lead_supplier._create_customer()
        self.assertEqual(customer.supplier_rank, 0)
        self.assertEqual(customer.customer_rank, 1)
        self.assertEqual(supplier.supplier_rank, 1)
        self.assertEqual(supplier.customer_rank, 0)

    # N.B.: the following tests are adapted from the standard analogues in ``sale_crm``
    @users("user_sales_salesman")
    def test_02_lead_convert_to_rfq_create(self):
        """Test that a RFQ can be created from a lead."""
        # Perform initial tests, do not repeat them at each test
        lead = self.lead_1.with_user(self.env.user)
        self.assertEqual(lead.partner_id, self.env["res.partner"])
        new_partner = self.env["res.partner"].search(
            [("email_normalized", "=", "amy.wong@test.example.com")]
        )
        self.assertEqual(new_partner, self.env["res.partner"])

        # invoke wizard and apply it
        convert = (
            self.env["srm.rfq.partner"]
            .with_context(**{"active_model": "crm.lead", "active_id": lead.id})
            .create({})
        )

        self.assertEqual(convert.action, "create")
        self.assertEqual(convert.partner_id, self.env["res.partner"])

        action = convert.action_apply()

        # test lead update
        new_partner = self.env["res.partner"].search(
            [("email_normalized", "=", "amy.wong@test.example.com")]
        )
        self.assertEqual(lead.partner_id, new_partner)
        # test wizard action (does not create anything, just returns action)
        self.assertEqual(action["res_model"], "purchase.order")
        self.assertEqual(action["context"]["default_partner_id"], new_partner.id)
        self.assertEqual(action["context"]["default_opportunity_id"], lead.id)
        self.assertEqual(action["context"]["default_user_id"], lead.user_id.id)

    @users("user_sales_salesman")
    def test_03_lead_convert_to_rfq_exist(self):
        """Test taking only existing customer while converting."""
        lead = self.lead_1.with_user(self.env.user)
        # invoke wizard and apply it
        convert = (
            self.env["srm.rfq.partner"]
            .with_context(**{"active_model": "crm.lead", "active_id": lead.id})
            .create({"action": "exist"})
        )

        self.assertEqual(convert.action, "exist")
        self.assertEqual(convert.partner_id, self.env["res.partner"])

        action = convert.action_apply()

        # test lead update
        new_partner = self.env["res.partner"].search(
            [("email_normalized", "=", "amy.wong@test.example.com")]
        )
        self.assertEqual(new_partner, self.env["res.partner"])

        convert.write({"partner_id": self.contact_2.id})
        action = convert.action_apply()

        # test lead update
        new_partner = self.env["res.partner"].search(
            [("email_normalized", "=", "amy.wong@test.example.com")]
        )
        self.assertEqual(new_partner, self.env["res.partner"])
        self.assertEqual(lead.partner_id, self.contact_2)
        self.assertEqual(lead.email_from, self.contact_2.email)
        self.assertEqual(action["context"]["default_partner_id"], self.contact_2.id)
        self.assertEqual(action["context"]["default_opportunity_id"], lead.id)

    @users("user_sales_salesman")
    def test_04_lead_convert_to_rfq_false_match_create(self):
        lead = self.lead_1.with_user(self.env.user)

        # invoke wizard and apply it
        convert = (
            self.env["srm.rfq.partner"]
            .with_context(
                **{
                    "active_model": "crm.lead",
                    "active_id": lead.id,
                }
            )
            .create({"action": "create"})
        )

        convert.write({"partner_id": self.contact_2.id})

        self.assertEqual(convert.action, "create")

        # ignore matching partner and create a new one
        convert.action_apply()

        self.assertTrue(bool(lead.partner_id.id))
        self.assertNotEqual(lead.partner_id, self.contact_2)

    @users("user_sales_salesman")
    def test_05_lead_convert_to_rfq_nothing(self):
        """Test doing nothing about customer while converting"""
        lead = self.lead_1.with_user(self.env.user)

        # invoke wizard and apply it
        convert = (
            self.env["srm.rfq.partner"]
            .with_context(
                **{
                    "active_model": "crm.lead",
                    "active_id": lead.id,
                    "default_action": "nothing",
                }
            )
            .create({})
        )

        self.assertEqual(convert.action, "nothing")
        self.assertEqual(convert.partner_id, self.env["res.partner"])

        action = convert.action_apply()

        # test lead update
        new_partner = self.env["res.partner"].search(
            [("email_normalized", "=", "amy.wong@test.example.com")]
        )
        self.assertEqual(new_partner, self.env["res.partner"])
        self.assertEqual(lead.partner_id, self.env["res.partner"])
        self.assertEqual(action["context"]["default_partner_id"], False)
        self.assertEqual(action["context"]["default_opportunity_id"], lead.id)
