# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestAttachExistingAttachment(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_obj = cls.env["res.partner"]
        cls.partner_01 = cls.partner_obj.create(
            {
                "name": "The Jackson Group",
                "is_company": True,
                "email": "jackson.group82@example.com",
            }
        )
        cls.partner_02 = cls.partner_obj.create(
            {
                "name": "Toni Rhodes",
                "function": "Managing Partner",
                "parent_id": cls.partner_01.id,
                "email": "toni.rhodes11@example.com",
            }
        )

    def test_send_email_attachment(self):
        ctx = self.env.context.copy()
        ctx.update(
            {
                "default_model": "res.partner",
                "default_res_ids": self.partner_01.ids,
                "default_composition_mode": "comment",
            }
        )
        mail_compose = self.env["mail.compose.message"]
        values = {
            "partner_ids": [Command.link(self.partner_02.id)],
            "composition_mode": "comment",
        }
        compose_id = mail_compose.with_context(**ctx).create(values)
        compose_id.autofollow_recipients = False
        compose_id.with_context(**ctx).action_send_mail()
        res = self.env["mail.followers"].search(
            [
                ("res_model", "=", "res.partner"),
                ("res_id", "=", self.partner_01.id),
                ("partner_id", "=", self.partner_02.id),
            ]
        )
        # I check if the recipient isn't a follower
        self.assertEqual(len(res.ids), 0)
        compose_id = mail_compose.with_context(**ctx).create(values)
        compose_id.autofollow_recipients = True
        compose_id.with_context(**ctx).action_send_mail()
        res = self.env["mail.followers"].search(
            [
                ("res_model", "=", "res.partner"),
                ("res_id", "=", self.partner_01.id),
                ("partner_id", "=", self.partner_02.id),
            ]
        )
        # I check if the recipient is a follower
        self.assertEqual(len(res.ids), 1)
