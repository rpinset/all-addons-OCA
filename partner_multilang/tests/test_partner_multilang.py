# Copyright 2026 OCA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("-at_install", "post_install")
class TestPartnerMultilang(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure we have an active bg_BG language for translation checks
        cls.lang_bg = cls.env.ref("base.lang_bg", raise_if_not_found=False)
        if not cls.lang_bg:
            cls.lang_bg = cls.env["res.lang"].create(
                {
                    "name": "Bulgarian",
                    "code": "bg_BG",
                    "iso_code": "bg",
                    "direction": "ltr",
                    "date_format": "%m/%d/%Y",
                    "time_format": "%H:%M:%S",
                    "thousands_sep": ",",
                    "decimal_point": ".",
                    "active": True,
                }
            )
        else:
            cls.lang_bg.write({"active": True})

    def test_complete_name_multilanguage_translations(self):
        partner = self.env["res.partner"].create({"name": "Acme"})

        if self.lang_bg:
            partner.with_context(lang="bg_BG").write({"name": "Акме"})

        partner._update_complete_name_multilanguage()

        self.assertEqual(
            partner.with_context(lang="en_US").complete_name_multilanguage, "Acme"
        )
        if self.lang_bg:
            self.assertEqual(
                partner.with_context(lang="bg_BG").complete_name_multilanguage, "Акме"
            )

    def test_strip_lang_suffix_in_domain(self):
        model = self.env["res.partner"]
        domain = [("name.en_US", "ilike", "Ac")]
        cleaned = model._strip_lang_suffix_in_domain(domain)
        self.assertEqual(cleaned, [("name", "ilike", "Ac")])
