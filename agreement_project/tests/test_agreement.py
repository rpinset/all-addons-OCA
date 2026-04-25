from odoo.tests.common import TransactionCase


class TestAgreement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.task_id = cls.env.ref("project.project_1_task_1")
        cls.agreement_id = cls.env.ref("agreement.market1")
        cls.agreement_id2 = cls.env.ref("agreement.market2")
        cls.project_id = cls.env.ref("project.project_project_3")

    def test_agreement(self):
        self.task_id.agreement_id = self.agreement_id
        self.agreement_id._compute_task_count()
        self.assertEqual(self.agreement_id.task_count, 1)
        self.project_id.agreement_id = self.agreement_id2
        self.assertIn(self.project_id, self.agreement_id2.project_ids)
