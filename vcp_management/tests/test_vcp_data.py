# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo.fields import Date

from odoo.addons.base.tests.common import TransactionCase


class TestVcpPartner(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.host_type = cls.env["vcp.host.type"].create(
            {
                "name": "Dummy",
                "code": "dummy",
                "code_kind": "dummy",
            }
        )
        cls.host = cls.env["vcp.host"].create(
            {
                "name": "Dummy Platform",
                "type_id": cls.host_type.id,
            }
        )
        # be sure some expected values are set otherwise homepage may fail
        date = Date.today()
        date = date - timedelta(days=date.day + 1)
        platform = cls.env["vcp.platform"].create(
            {
                "name": "oca",
                "short_description": "OCA",
                "description": "OCA",
                "host_id": cls.host.id,
            }
        )
        cls.repository = cls.env["vcp.repository"].create(
            {
                "name": "contributors-module",
                "description": "OCA/contributors-module",
                "platform_id": platform.id,
                "from_date": date,
            }
        )
        cls.partner_01 = cls.env["res.partner"].create(
            {
                "name": "Enric Tobella",
            }
        )
        user_01 = cls.env["vcp.user"].create(
            {
                "name": "Enric Tobella",
                "external_id": "etobella",
                "host_id": cls.host.id,
                "partner_id": cls.partner_01.id,
            }
        )
        cls.partner_02 = cls.env["res.partner"].create(
            {
                "name": "Luis Rodriguez",
            }
        )
        user_02 = cls.env["vcp.user"].create(
            {
                "name": "Luis Rodriguez",
                "external_id": "lrodriguez",
                "host_id": cls.host.id,
                "partner_id": cls.partner_02.id,
            }
        )
        cls.partner_03 = cls.env["res.partner"].create(
            {
                "name": "Jordi Ballester",
            }
        )
        user_03 = cls.env["vcp.user"].create(
            {
                "name": "Jordi Ballester",
                "external_id": "jballester",
                "host_id": cls.host.id,
                "partner_id": cls.partner_03.id,
            }
        )

        cls.partner_org_01 = cls.env["res.partner"].create(
            {
                "name": "Dixmit",
            }
        )
        org_01 = cls.env["vcp.organization"].create(
            {
                "name": "Dixmit",
                "external_id": "dixmit",
                "host_id": cls.host.id,
                "partner_id": cls.partner_org_01.id,
            }
        )
        cls.partner_org_02 = cls.env["res.partner"].create(
            {
                "name": "ForgeFlow",
            }
        )
        org_02 = cls.env["vcp.organization"].create(
            {
                "name": "ForgeFlow",
                "external_id": "forgeflow",
                "host_id": cls.host.id,
                "partner_id": cls.partner_org_02.id,
            }
        )
        pull_request_01 = cls.env["vcp.request"].create(
            {
                "external_id": 1,
                "name": "Test PR",
                "repository_id": cls.repository.id,
                "user_id": user_01.id,
                "organization_id": org_01.id,
                "created_at": date,
                "closed_at": date,
                "is_merged": True,
            }
        )
        cls.env["vcp.request"].create(
            {
                "external_id": 2,
                "name": "Test PR",
                "repository_id": cls.repository.id,
                "user_id": user_02.id,
                "organization_id": org_01.id,
                "created_at": date,
                "is_merged": False,
            }
        )
        cls.env["vcp.request"].create(
            {
                "external_id": 3,
                "name": "Test PR",
                "repository_id": cls.repository.id,
                "user_id": user_03.id,
                "organization_id": org_02.id,
                "created_at": date,
                "is_merged": False,
            }
        )
        cls.env["vcp.review"].create(
            {
                "external_id": 1,
                "body": "Test Review",
                "state": "APPROVED",
                "request_id": pull_request_01.id,
                "user_id": user_01.id,
                "submitted_at": date,
            }
        )
        cls.env["vcp.comment"].create(
            {
                "external_id": 1,
                "body": "Test Comment",
                "request_id": pull_request_01.id,
                "user_id": user_01.id,
                "created_at": date,
            }
        )

    def test_partner_request_count(self):
        self.assertEqual(self.partner_01.vcp_comments, 1)
        self.assertEqual(self.partner_01.vcp_created_requests, 1)
        self.assertEqual(self.partner_01.vcp_merged_requests, 1)
        self.assertEqual(self.partner_01.vcp_reviews, 1)
        self.assertEqual(self.partner_02.vcp_comments, 0)
        self.assertEqual(self.partner_02.vcp_created_requests, 1)
        self.assertEqual(self.partner_02.vcp_merged_requests, 0)
        self.assertEqual(self.partner_02.vcp_reviews, 0)
        self.assertEqual(self.partner_03.vcp_comments, 0)
        self.assertEqual(self.partner_03.vcp_created_requests, 1)
        self.assertEqual(self.partner_03.vcp_merged_requests, 0)
        self.assertEqual(self.partner_03.vcp_reviews, 0)
        self.assertEqual(self.partner_org_01.vcp_comments, 1)
        self.assertEqual(self.partner_org_01.vcp_created_requests, 2)
        self.assertEqual(self.partner_org_01.vcp_merged_requests, 1)
        self.assertEqual(self.partner_org_01.vcp_reviews, 1)
        self.assertEqual(self.partner_org_02.vcp_comments, 0)
        self.assertEqual(self.partner_org_02.vcp_created_requests, 1)
        self.assertEqual(self.partner_org_02.vcp_merged_requests, 0)
        self.assertEqual(self.partner_org_02.vcp_reviews, 0)

    def test_repository_data(self):
        self.assertEqual(self.repository.request_count, 3)
