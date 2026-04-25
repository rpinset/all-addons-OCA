# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import tempfile
from unittest.mock import patch

from odoo.fields import Date
from odoo.tools import mute_logger

from odoo.addons.base.tests.common import TransactionCase


class TestVcpRules(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._tmp_dir = tempfile.TemporaryDirectory(prefix="vcp-git")
        cls.env["ir.config_parameter"].sudo().set_param(
            "vcp_management.source_code_local_path", cls._tmp_dir.name
        )
        cls.addClassCleanup(cls._tmp_dir.cleanup)
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
        # disable updates to avoid unwanted side effects during tests
        cls.env["vcp.platform"].search([]).write(
            {"scheduled_information_update": False}
        )
        cls.env["vcp.repository"].search([]).write(
            {"scheduled_information_update": False, "scheduled_branch_update": False}
        )
        # be sure some expected values are set otherwise homepage may fail
        cls.platform = cls.env["vcp.platform"].create(
            {
                "name": "oca",
                "short_description": "OCA",
                "description": "OCA",
                "host_id": cls.host.id,
                "scheduled_information_update": True,
            }
        )

    def test_repository_update_no_definition(self):
        self.env["vcp.repository"].create(
            {
                "name": "test_repo",
                "description": "Test Repository",
                "platform_id": self.platform.id,
                "scheduled_information_update": True,
                "from_date": Date.today(),
            }
        )
        with (
            self.assertRaises(AttributeError),
            mute_logger("odoo.addons.vcp_management.models.vcp_platform"),
        ):
            self.env["vcp.repository"]._cron_update_platforms()

    def test_platform_branch_update_no_definition(self):
        self.env["vcp.repository"].create(
            {
                "name": "test_repo",
                "description": "Test Repository",
                "platform_id": self.platform.id,
                "scheduled_branch_update": True,
                "from_date": Date.today(),
            }
        )
        with (
            self.assertRaises(AttributeError),
            mute_logger("odoo.addons.vcp_management.models.vcp_platform"),
        ):
            self.env["vcp.repository"]._cron_update_branches(limit=1)

    def test_platform_update_no_definition(self):
        with (
            self.assertRaises(AttributeError),
            mute_logger("odoo.addons.vcp_management.models.vcp_platform"),
        ):
            self.env["vcp.platform"]._cron_update_platforms()

    def test_repository_branch_rules_check_definition(self):
        def dummy_update_information(oself, *args, **kwargs):
            if oself.repository_ids:
                return
            oself.env["vcp.repository"].create(
                {
                    "name": "test_repo",
                    "description": "Test Repository",
                    "platform_id": oself.id,
                    "scheduled_information_update": True,
                    "scheduled_branch_update": True,
                    "from_date": Date.today(),
                }
            )

        self.assertFalse(self.platform.repository_ids)
        with patch(
            "odoo.addons.vcp_management.models.vcp_platform.VcpPlatform._update_information_dummy",
            dummy_update_information,
            create=True,
        ):
            self.env["vcp.platform"]._cron_update_platforms()
            self.assertTrue(self.platform.repository_ids)

        def dummy_repository_update_information(oself, *args, **kwargs):
            if oself.request_ids:
                return
            oself.env["vcp.request"].create(
                {
                    "external_id": 1,
                    "name": "Test PR",
                    "repository_id": oself.id,
                    "user_id": oself.env["vcp.user"]
                    .create(
                        {
                            "name": "Test User",
                            "external_id": "testuser",
                            "host_id": oself.platform_id.host_id.id,
                        }
                    )
                    .id,
                    "created_at": Date.today(),
                }
            )

        repository = self.platform.repository_ids[0]
        self.assertTrue(repository)
        self.assertFalse(repository.request_ids)

        with patch(
            "odoo.addons.vcp_management.models.vcp_repository.VcpRepository._update_information_dummy",
            dummy_repository_update_information,
            create=True,
        ):
            self.env["vcp.repository"]._cron_update_repositories(limit=1)
        repository.invalidate_recordset()
        self.assertTrue(repository.request_ids)
        self.assertFalse(repository.branch_ids)

        def dummy_repository_update_branches(oself, *args, **kwargs):
            if oself.branch_ids:
                return
            oself.env["vcp.repository.branch"].create(
                {
                    "branch_id": oself.platform_id._get_branch("main"),
                    "repository_id": oself.id,
                }
            )

        with patch(
            "odoo.addons.vcp_management.models.vcp_repository.VcpRepository._update_branches_dummy",
            dummy_repository_update_branches,
            create=True,
        ):
            self.env["vcp.repository"]._cron_update_branches(limit=1)

        self.assertTrue(repository.branch_ids)
        self.assertEqual(repository.branch_ids.branch_id.name, "main")
