# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.helpdesk_mgmt_fieldservice.tests.test_helpdesk_ticket_fsm_order import (  # noqa: E501
    TestHelpdeskTicketFSMOrder,
)


class TestHelpdeskTicketFSMOrderProject(TestHelpdeskTicketFSMOrder):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env["project.project"].create({"name": "Test Project"})
        cls.task = cls.env["project.task"].create(
            {"name": "Test Task", "project_id": cls.project.id}
        )
        cls.ticket_1.write(
            {
                "project_id": cls.project.id,
                "task_id": cls.task.id,
            }
        )

    def test_helpdesk_ticket_fsm_order_propagation(self):
        fsm_orders = self._create_ticket_fsm_orders(self.ticket_1, 5)
        self.assertRecordValues(
            fsm_orders,
            [
                {
                    "project_id": self.ticket_1.project_id.id,
                    "project_task_id": self.ticket_1.task_id.id,
                }
                for _ in range(5)
            ],
        )
