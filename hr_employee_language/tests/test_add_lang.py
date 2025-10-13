from odoo.tests.common import TransactionCase


class TestAddLanguage(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestAddLanguage, cls).setUpClass()

    def test_add_lang(self):
        lang_list = self.env["res.lang"].search([("active", "in", (True, False))])
        lang_old = lang_list[0].code
        selection = self.env["hr.employee.language"]._get_selection()
        selection_ck = any(map(lambda t: lang_old in t, selection))
        # Test if a old lang is present
        self.assertEqual(selection_ck, True, "Old language is present")

        self.env["res.lang"].create({"code": "xx_XX", "name": "Foo"})
        selection = self.env["hr.employee.language"]._get_selection()
        selection_ck = any(map(lambda t: "xx_XX" in t, selection))
        # Test if a new lang is present
        self.assertEqual(selection_ck, True, "New language is present")
