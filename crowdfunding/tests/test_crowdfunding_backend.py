import odoo
import odoo.tests


class TestCrowdfundingBackend(odoo.tests.HttpCase):
    def test_create_non_multicompany(self):
        """
        Test that creating challenges works without multicompany group
        """
        self.env.user.groups_id -= self.env.ref("base.group_multi_company")
        with odoo.tests.Form(self.env["crowdfunding.challenge"]) as form:
            form.name = "testchallenge"
            challenge = form.save()
        self.assertTrue(challenge.exists())
