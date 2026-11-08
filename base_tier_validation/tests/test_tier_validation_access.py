# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import AccessError
from odoo.tests import new_test_user, tagged

from .common import CommonTierValidation


@tagged("post_install", "-at_install")
class TierValidationAccess(CommonTierValidation):
    def test_portal_and_public_cannot_read_reviews(self):
        self.test_record.with_user(self.test_user_2).request_validation()
        self.assertTrue(self.test_record.review_ids)
        portal = new_test_user(self.env, login="tv_portal", groups="base.group_portal")
        public = self.env.ref("base.public_user")
        for user in (portal, public):
            for model in ("tier.review", "tier.definition"):
                with self.assertRaises(AccessError):
                    self.env[model].with_user(user).search([])
