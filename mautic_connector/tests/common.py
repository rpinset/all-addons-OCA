# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class MauticTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend = cls.env["mautic.backend"].create(
            {
                "name": "Test Backend",
                "api_url": "https://mautic.test",
                "client_id": "test-client-id",
                "client_secret": "test-client-secret",
                "access_token": "test-access-token",
                "refresh_token": "test-refresh-token",
                "token_expires_at": fields.Datetime.now() + timedelta(hours=1),
            }
        )
