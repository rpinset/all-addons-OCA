import odoo.tests
from odoo import fields


@odoo.tests.tagged("post_install", "-at_install")
class TestCrowdfundingScheduleFrontend(odoo.tests.HttpCase):
    def _dt(self, delta):
        return fields.Datetime.now() + delta

    def test_future_challenge(self):
        challenge = self.env.ref("crowdfunding_schedule.demo_challenge_future")

        response = self.url_open(challenge.website_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"This crowdfunding challenge is not yet active.",
            response.content,
        )
        self.assertIn(
            b"s_countdown",
            response.content,
        )

    def test_active_challenge(self):
        challenge = self.env.ref("crowdfunding_schedule.demo_challenge_active")

        response = self.url_open(challenge.website_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"s_countdown",
            response.content,
        )

    def test_expired_challenge(self):
        challenge = self.env.ref("crowdfunding_schedule.demo_challenge_expired")

        response = self.url_open(challenge.website_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"This crowdfunding challenge has ended.",
            response.content,
        )

    def test_payment_future_challenge(self):
        challenge = self.env.ref("crowdfunding_schedule.demo_challenge_future")

        response = self.url_open(f"/crowdfunding/{challenge.id}/pay")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Pledges are not available",
            response.content,
        )
        self.assertIn(
            b"This crowdfunding challenge has not started yet.",
            response.content,
        )

    def test_payment_expired_challenge(self):
        challenge = self.env.ref("crowdfunding_schedule.demo_challenge_expired")

        response = self.url_open(f"/crowdfunding/{challenge.id}/pay")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Pledges are not available",
            response.content,
        )
        self.assertIn(
            b"This crowdfunding challenge has already expired.",
            response.content,
        )
