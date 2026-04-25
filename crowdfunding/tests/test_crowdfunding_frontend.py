import odoo
import odoo.tests


@odoo.tests.tagged("-at_install", "post_install")
class TestCrowdfundingFrontend(odoo.tests.HttpCase):
    def test_pledge_not_logged_in(self):
        """
        Test pledging for a challenge without being logged in
        """
        challenge = self.env.ref("crowdfunding.demo_challenge")
        self.start_tour("/", "crowdfunding_frontend_us")
        self.assertEqual(challenge.pledged_amount_total, 4242)
        self.assertEqual(
            challenge.invoice_ids.partner_id.name,
            "Firstname Lastname",
        )

    def test_pledge_not_logged_in_nl(self):
        """
        Test filling in NL-specific values for the partner form
        """
        self.start_tour("/", "crowdfunding_frontend_nl")
