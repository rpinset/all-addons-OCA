import json

from odoo.addons.base.tests.common import BaseCommon


class TestMailTemplateDomain(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_company = cls.env["res.partner"].create(
            {"name": "Test company partner", "is_company": True}
        )
        cls.partner_individual = cls.env["res.partner"].create(
            {"name": "Test individual partner", "is_company": False}
        )
        model_id = cls.env["ir.model"]._get("res.partner").id
        cls.template_no_domain = cls.env["mail.template"].create(
            {
                "name": "Template no domain",
                "model_id": model_id,
            }
        )
        cls.template_company = cls.env["mail.template"].create(
            {
                "name": "Template company",
                "model_id": model_id,
                "filter_model": True,
                "filter_domain": "[('is_company', '=', True)]",
            }
        )
        cls.template_no_match = cls.env["mail.template"].create(
            {
                "name": "Template no match",
                "model_id": model_id,
                "filter_model": True,
                "filter_domain": "[('id', '<', 0)]",
            }
        )

    def _search_templates(self, records):
        composer = self.env["mail.compose.message"].create(
            {
                "model": records._name,
                "res_ids": json.dumps(records.ids),
                "composition_mode": "comment",
            }
        )
        return self.env["mail.template"].search(composer.domain_template_id)

    def test_templates_partner_company(self):
        templates = self._search_templates(self.partner_company)
        self.assertIn(self.template_no_domain, templates)
        self.assertIn(self.template_company, templates)
        self.assertNotIn(self.template_no_match, templates)

    def test_templates_partner_individual(self):
        templates = self._search_templates(self.partner_individual)
        self.assertIn(self.template_no_domain, templates)
        self.assertNotIn(self.template_company, templates)
        self.assertNotIn(self.template_no_match, templates)

    def test_template_domain_all_records_match(self):
        """Template appears only when ALL selected records match the domain."""
        partner_company2 = self.env["res.partner"].create(
            {"name": "Test company 2", "is_company": True}
        )
        templates = self._search_templates(self.partner_company | partner_company2)
        self.assertIn(self.template_company, templates)
        self.assertIn(self.template_no_domain, templates)
        self.assertNotIn(self.template_no_match, templates)

    def test_template_domain_not_all_records_match(self):
        """Template hidden when at least one selected record does not match."""
        templates = self._search_templates(
            self.partner_company | self.partner_individual
        )
        self.assertNotIn(self.template_company, templates)
        self.assertIn(self.template_no_domain, templates)
        self.assertNotIn(self.template_no_match, templates)
