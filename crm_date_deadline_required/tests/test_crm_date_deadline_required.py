# Copyright 2025 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestCRMDateDeadlineRequired(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_crm_date_deadline_required(self):
        """Check date_deadline required in opportunity"""
        # Check required in opportunity
        opportunity_form = Form(
            self.env["crm.lead"].with_context(default_type="opportunity")
        )
        opportunity_form.name = "Test Opportunity"
        with self.assertRaises(AssertionError):
            opportunity_form.save()
        opportunity_form.date_deadline = "2025-01-01"
        opportunity_form.save()
        # Check required in lead
        lead_form = Form(self.env["crm.lead"].with_context(default_type="lead"))
        lead_form.name = "Test Lead"
        lead_form.save()
