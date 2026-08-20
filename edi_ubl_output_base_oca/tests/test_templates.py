# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo.tests.common import TransactionCase
from odoo.tools import DotDict

NS = {
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
}


class TestUblOutputBaseTemplates(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "ACME Vendor",
                "street": "Foo street 1",
                "street2": "Suite 2",
                "city": "Lausanne",
                "zip": "1000",
                "country_id": cls.env.ref("base.ch").id,
            }
        )

    def _render(self, template, values):
        return self.env["ir.qweb"]._render(template, values)

    def test_party_minimal(self):
        party = DotDict(name="ACME Vendor", identifiers=[], endpoint={})
        xml = self._render(
            "edi_ubl_output_base_oca.qweb_tmpl_ubl_party", {"party": party}
        )
        root = etree.fromstring(
            f"<root xmlns:cac='{NS['cac']}' xmlns:cbc='{NS['cbc']}'>{xml}</root>"
        )
        self.assertIsNone(root.find(".//cbc:EndpointID", NS))
        self.assertIsNone(root.find(".//cac:PartyIdentification", NS))
        self.assertEqual(root.find(".//cac:PartyName/cbc:Name", NS).text, "ACME Vendor")

    def test_party_with_endpoint_and_identifiers(self):
        party = DotDict(
            name="ACME Vendor",
            identifiers=[
                DotDict(attrs={"schemeID": "0088"}, value="8591234567894"),
            ],
            endpoint=DotDict(attrs={"schemeID": "0088"}, value="8591234567894"),
        )
        xml = self._render(
            "edi_ubl_output_base_oca.qweb_tmpl_ubl_party", {"party": party}
        )
        root = etree.fromstring(
            f"<root xmlns:cac='{NS['cac']}' xmlns:cbc='{NS['cbc']}'>{xml}</root>"
        )
        endpoint = root.find(".//cbc:EndpointID", NS)
        self.assertEqual(endpoint.text, "8591234567894")
        self.assertEqual(endpoint.get("schemeID"), "0088")
        identification = root.find(".//cac:PartyIdentification/cbc:ID", NS)
        self.assertEqual(identification.text, "8591234567894")

    def test_address(self):
        xml = self._render(
            "edi_ubl_output_base_oca.qweb_tmpl_ubl_address", {"partner": self.partner}
        )
        root = etree.fromstring(
            f"<root xmlns:cac='{NS['cac']}' xmlns:cbc='{NS['cbc']}'>{xml}</root>"
        )
        self.assertEqual(root.find("cbc:StreetName", NS).text, "Foo street 1")
        self.assertEqual(root.find("cbc:CityName", NS).text, "Lausanne")
        self.assertEqual(root.find("cbc:PostalZone", NS).text, "1000")
        self.assertEqual(root.find("cac:AddressLine/cbc:Line", NS).text, "Suite 2")
        # `t-field` renders the Many2one's default display (name), not
        # `.code` - pre-existing behavior carried over as-is from
        # edi_sale_ubl_output_oca, not something to fix as part of this split.
        self.assertEqual(
            root.find("cac:Country/cbc:IdentificationCode", NS).text, "Switzerland"
        )
