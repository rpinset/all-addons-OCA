# Copyright 2025 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import ValidationError

from .test_partner_relation_common import TestPartnerRelationCommon


class TestPartnerContraint(TestPartnerRelationCommon):
    def test_change_partner_type(self):
        # Create relation between self.partner_02_company and self.partner_01_person
        self._create_company2person_relation()
        with self.assertRaises(ValidationError):
            self.partner_02_company.write({"is_company": False})
        with self.assertRaises(ValidationError):
            self.partner_01_person.write({"is_company": True})
        # Create a relation where the type does not matter.
        favorable_type = self.type_model.create(
            {
                "name": "looks favorable on",
                "name_inverse": "is looked on favorable by",
                "contact_type_left": False,
                "contact_type_right": False,
            }
        )
        # Create two persons and connect them.
        partner_shoe_shop = self.partner_model.create(
            {"name": "Test Jan Shoe Shop", "is_company": False, "ref": "SS01"}
        )
        partner_maria = self.partner_model.create(
            {"name": "Maria Montenelli", "is_company": False, "ref": "MM01"}
        )
        self.relation_model.create(
            {
                "left_partner_id": partner_shoe_shop.id,
                "right_partner_id": partner_maria.id,
                "type_id": favorable_type.id,
            }
        )
        # Should be possible to change partner type.
        partner_shoe_shop.write({"is_company": True})
        self.assertTrue(partner_shoe_shop.is_company)
