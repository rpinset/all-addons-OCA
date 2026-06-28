from odoo.tests.common import TransactionCase


class TestAgreement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.agreement_1 = cls.env["agreement"].create(
            {"code": "AGR-001", "name": "Agreement"}
        )
        cls.agreement_2 = cls.env["agreement"].create(
            {"code": "AGR-002", "name": "Other Agreement"}
        )
        cls.project_1 = cls.env["project.project"].create(
            {"name": "Project #1", "agreement_id": cls.agreement_1.id}
        )
        cls.project_2 = cls.env["project.project"].create(
            {"name": "Project #2", "agreement_id": cls.agreement_2.id}
        )
        cls.task_1 = cls.env["project.task"].create(
            {"name": "Task #1", "project_id": cls.project_1.id}
        )
        cls.task_2 = cls.env["project.task"].create(
            {"name": "Task #2", "project_id": cls.project_2.id}
        )

    def _create_project(self, agreement):
        return self.env["project.project"].create(
            {"name": f"Project ({agreement.name})", "agreement_id": agreement.id}
        )

    def _create_task(self, project):
        return self.env["project.task"].create(
            {"name": "Task", "project_id": project.id}
        )

    def _create_tasks(self, project, task_count=2):
        tasks = self.env["project.task"]
        for _ in range(task_count):
            tasks |= self._create_task(project)
        return tasks

    def test_agreement_task_count(self):
        self.assertEqual(self.agreement_1.task_count, 1)

    def test_task_count_increases_on_task_creation(self):
        agreement_1_count = self.agreement_1.task_count
        agreement_2_count = self.agreement_2.task_count
        self._create_task(self.project_1)
        self.assertEqual(self.agreement_1.task_count, agreement_1_count + 1)
        self.assertEqual(self.agreement_2.task_count, agreement_2_count)

    def test_task_count_decreases_on_task_deletion(self):
        task_to_delete = self._create_task(self.project_1)
        agreement_1_count = self.agreement_1.task_count
        agreement_2_count = self.agreement_2.task_count
        task_to_delete.unlink()
        self.assertEqual(self.agreement_1.task_count, agreement_1_count - 1)
        self.assertEqual(self.agreement_2.task_count, agreement_2_count)

    def test_task_count_increases_on_project_agreement_change(self):
        extra_project = self._create_project(self.agreement_2)
        self._create_tasks(extra_project, task_count=2)
        project_task_count = len(extra_project.tasks)
        agreement_1_count = self.agreement_1.task_count
        agreement_2_count = self.agreement_2.task_count
        extra_project.agreement_id = self.agreement_1
        self.assertEqual(
            self.agreement_1.task_count, agreement_1_count + project_task_count
        )
        self.assertEqual(
            self.agreement_2.task_count, agreement_2_count - project_task_count
        )

    def test_task_count_decreases_on_project_agreement_change(self):
        extra_project = self._create_project(self.agreement_1)
        self._create_tasks(extra_project, task_count=2)
        project_task_count = len(extra_project.tasks)
        agreement_1_count = self.agreement_1.task_count
        agreement_2_count = self.agreement_2.task_count
        extra_project.agreement_id = self.agreement_2
        self.assertEqual(
            self.agreement_1.task_count, agreement_1_count - project_task_count
        )
        self.assertEqual(
            self.agreement_2.task_count, agreement_2_count + project_task_count
        )
