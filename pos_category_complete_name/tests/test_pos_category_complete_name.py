# Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestPosCategoryCompleteName(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.PosCategory = cls.env["pos.category"]

    def test_complete_name(self):
        main_category = self.PosCategory.create({"name": "Main Category"})
        self.assertEqual(main_category.complete_name, "Main Category")

        new_categoy = self.PosCategory.create(
            {"name": "New Category", "parent_id": main_category.id}
        )
        self.assertEqual(new_categoy.complete_name, "Main Category / New Category")
