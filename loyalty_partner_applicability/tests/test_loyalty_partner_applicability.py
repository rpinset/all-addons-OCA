# Copyright 2025 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import TestLoyaltyPartnerApplicabilityCase


class TestLoyaltyPartnerApplicability(TestLoyaltyPartnerApplicabilityCase):
    def _assertCheckValidPartner(self, program, partner, expected):
        self.assertEqual(
            program._is_partner_valid(partner),
            expected,
            f"Partner {partner.name} should be {'valid' if expected else 'invalid'} "
            f"for program {program.name} (_is_partner_valid)",
        )
        domain = program._get_partner_domain(partner)
        is_valid = partner.search_count(domain) > 0
        self.assertEqual(
            is_valid,
            expected,
            f"Partner {partner.name} should be {'valid' if expected else 'invalid'} "
            f"for program {program.name} (_get_partner_domain)",
        )

    def test_program_no_restriction(self):
        program = self.program_no_restriction
        self.assertFalse(program._is_coupon_sharing_allowed())
        self.assertFalse(program._is_coupon_sharing_allowed())
        self._assertCheckValidPartner(program, self.partner1, True)
        self._assertCheckValidPartner(program, self.partner2, True)
        self._assertCheckValidPartner(program, self.partner3, True)

    def test_restriction_on_partner_ids(self):
        program = self.program_restricted_to_partner_ids
        self.assertFalse(program._is_coupon_sharing_allowed())
        self._assertCheckValidPartner(program, self.partner1, True)
        self._assertCheckValidPartner(program, self.partner2, False)
        self._assertCheckValidPartner(program, self.partner3, False)

    def test_restriction_on_partner_domain(self):
        program = self.program_restricted_to_partner_domain
        self.assertFalse(program._is_coupon_sharing_allowed())
        self._assertCheckValidPartner(program, self.partner1, False)
        self._assertCheckValidPartner(program, self.partner2, True)
        self._assertCheckValidPartner(program, self.partner3, False)

    def test_restriction_on_partner_domain_and_partner_ids(self):
        program = self.program_restricted_to_partner_domain_and_partner_ids
        self.assertFalse(program._is_coupon_sharing_allowed())
        self._assertCheckValidPartner(program, self.partner1, True)
        self._assertCheckValidPartner(program, self.partner2, True)
        self._assertCheckValidPartner(program, self.partner3, False)

    def test_partner_valid_when_partner_domain_empty(self):
        program = self.env["loyalty.program"].create(
            {
                "name": "Without explicit restrictions",
                "partner_ids": [(6, 0, [])],
                "partner_domain": "",
            }
        )
        partner = self.partner1
        self.assertTrue(program._is_partner_valid(partner))

    def test_partner_not_valid_but_coupon_sharing_allowed(self):
        self.env["ir.config_parameter"].set_param("allow_coupon_sharing", "True")
        partner = self.partner3
        program = self.program_restricted_to_partner_ids
        result = program._is_partner_valid(partner)
        self.assertFalse(result)
