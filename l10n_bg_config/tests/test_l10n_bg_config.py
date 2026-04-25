# Copyright 2026 OCA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import base64

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from ..models.l10n_bg_config_mixin import generate_encryption_keys, prepare_zip_payload


@tagged("-at_install", "post_install")
class TestL10nBGConfig(TransactionCase):
    def test_prepare_zip_payload_password_toggle(self):
        company = self.env.company
        partner = company.partner_id
        partner.l10n_bg_uic = "123456789"

        payload = prepare_zip_payload(files_report={"dummy": b""}, company=company)
        self.assertIn("password", payload, "Password expected when api key invalid")

        api_key = "APIKEY123"
        crypt_key = base64.b64encode(
            generate_encryption_keys(partner.l10n_bg_uic, api_key)
        )
        partner.l10n_bg_key = api_key
        partner.l10n_bg_crypt_key = crypt_key

        payload_valid = prepare_zip_payload(
            files_report={"dummy": b""}, company=company
        )
        self.assertNotIn(
            "password", payload_valid, "Password not expected when api key valid"
        )

    def test_get_view_hides_bg_fields_for_non_bg_company(self):
        other_company = self.env["res.company"].create(
            {
                "name": "Non BG Co",
                "chart_template": "us",  # anything different from 'bg'
            }
        )
        partner_model = self.env["res.partner"].with_company(other_company)
        view = partner_model.get_view(view_type="form")
        arch = (
            view["arch"].decode()
            if isinstance(view["arch"], (bytes | bytearray))
            else view["arch"]
        )

        self.assertIn("l10n_bg_key", arch)
        # fields with l10n_bg* should be invisible for non-BG companies
        self.assertIn('invisible="True"', arch)
