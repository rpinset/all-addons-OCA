# Copyright 2024 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo.fields import Command
from odoo.tests.common import TransactionCase


class TestHelpdeskMgmtProjectStage(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ticket_stage_progress = cls.env.ref(
            "helpdesk_mgmt.helpdesk_ticket_stage_in_progress"
        )
        cls.task_stage_progress = cls.env["project.task.type"].create(
            {
                "name": "stage in progress",
                "ticket_stage_ids": [Command.link(cls.ticket_stage_progress.id)],
            }
        )
        cls.ticket_stage_done = cls.env.ref("helpdesk_mgmt.helpdesk_ticket_stage_done")
        cls.task_stage_done = cls.env["project.task.type"].create(
            {
                "name": "stage done",
                "ticket_stage_ids": [Command.link(cls.ticket_stage_done.id)],
            }
        )
        cls.project = cls.env["project.project"].create(
            {
                "name": "Helpdesk project",
                "type_ids": [
                    Command.set((cls.task_stage_progress + cls.task_stage_done).ids)
                ],
            }
        )
        cls.task = cls.env["project.task"].create(
            {
                "name": "Ticket task",
                "project_id": cls.project.id,
                "stage_id": cls.task_stage_progress.id,
            }
        )
        cls.ticket = cls.env["helpdesk.ticket"].create(
            {
                "name": "Ticket",
                "project_id": cls.project.id,
                "description": "Change stage",
            }
        )
        cls.user = cls.env.ref("base.user_demo")

    def test_task_sync(self):
        """Test that configured stages stay in sync"""
        ticket = self.ticket.with_user(self.user)
        task = self.task.with_user(self.user)
        task.stage_id = self.task_stage_progress
        ticket.task_id = task
        task.stage_id = self.task_stage_done
        self.assertEqual(ticket.stage_id, self.ticket_stage_done)
        ticket.stage_id = self.ticket_stage_done
        self.assertEqual(task.stage_id, self.task_stage_done)
        ticket.stage_id = self.ticket_stage_progress
        self.assertEqual(task.stage_id, self.task_stage_progress)
        task.stage_id = False
        self.assertEqual(ticket.stage_id, self.ticket_stage_progress)
