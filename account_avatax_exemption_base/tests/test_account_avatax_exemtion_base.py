from odoo.tests.common import TransactionCase


class TestResPartnerExemption(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.env["res.partner"].create({"name": "Test Partner"})
        self.business_type = self.env["res.partner.exemption.business.type"].create(
            {"name": "Retail", "avatax_id": "BT001"}
        )
        self.other_business_type = self.env[
            "res.partner.exemption.business.type"
        ].create({"name": "Wholesale", "avatax_id": "BT002"})
        self.exemption_type = self.env["res.partner.exemption.type"].create(
            {"name": "Resale", "business_type": self.business_type.id}
        )
        self.exemption = self.env["res.partner.exemption"].create(
            {"partner_id": self.partner.id, "exemption_type": self.exemption_type.id}
        )

    def test_exemption_creation(self):
        self.assertEqual(self.exemption.exemption_type, self.exemption_type)
        self.exemption_type.business_type = self.other_business_type
        self.exemption.onchange_exemption_type()
        self.assertEqual(self.exemption.business_type, self.other_business_type)
