# Copyright 2026 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.tools.safe_eval import safe_eval

from odoo.addons.base.tests.common import BaseCommon


class Common(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.blacklisted_contact, cls.other_blacklisted_contact, cls.contact = cls.env[
            "mailing.contact"
        ].create(
            [
                {
                    "name": "Test other blacklisted contact",
                    "email": "blacklisted@b.c",
                },
                {
                    "name": "Test blacklisted contact",
                    "email": "blacklisted@b.c",
                },
                {
                    "name": "Test contact",
                    "email": "contact@b.c",
                },
            ],
        )
        cls.env["mail.blacklist"]._add(cls.blacklisted_contact.email)
        cls.env["mail.blacklist"]._add(cls.other_blacklisted_contact.email)

        cls.mailing_list = cls.env["mailing.list"].create(
            {
                "name": "Test Mailing List",
                "contact_ids": [
                    fields.Command.set(
                        (
                            cls.blacklisted_contact
                            + cls.other_blacklisted_contact
                            + cls.contact
                        ).ids
                    ),
                ],
            }
        )

        cls.wizard = (
            cls.env["mass_mailing_list_prune_blacklisted.wizard"]
            .with_context(
                active_ids=cls.mailing_list.ids,
            )
            .create({})
        )

        cls.mailing = cls.env["mailing.mailing"].create(
            {
                "subject": "Test Mailing",
                "contact_list_ids": [
                    fields.Command.set(cls.mailing_list.ids),
                ],
            }
        )

    @classmethod
    def _get_records_from_action(cls, action):
        context = safe_eval(action.get("context", "{}"))
        model = action["res_model"]
        return cls.env[model].with_context(**context).create([{}])
