# Copyright 2021 ACSONE SA/NV (<http://acsone.eu>)
# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import odoo.tests.common as common
from odoo.exceptions import ValidationError
from odoo.tools import mute_logger


class TestProductCode(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Catetories hierarchy
        # A
        #   AA
        #   AB
        #       ABA
        #           ABAA
        #           ABAB
        #       ABB
        #           ABBA
        #           ABBB
        vals = {
            "name": "A",
            "code": "A",
            "child_id": [
                (
                    0,
                    0,
                    {
                        "name": "AA",
                        "code": "AA",
                    },
                ),
                (
                    0,
                    0,
                    {
                        "name": "AB",
                        "code": "AB",
                        "child_id": [
                            (
                                0,
                                0,
                                {
                                    "name": "ABA",
                                    "code": "ABA",
                                    "child_id": [
                                        (0, 0, {"name": "ABAA", "code": "ABAA"}),
                                        (0, 0, {"name": "ABAB", "code": "ABAB"}),
                                    ],
                                },
                            ),
                            (
                                0,
                                0,
                                {
                                    "name": "ABB",
                                    "code": "ABB",
                                    "child_id": [
                                        (0, 0, {"name": "ABBA", "code": "ABBA"}),
                                        (0, 0, {"name": "ABBB", "code": "ABBB"}),
                                    ],
                                },
                            ),
                        ],
                    },
                ),
            ],
        }
        cls.category = cls.env["product.category"].create(vals)

    @mute_logger("odoo.sql_db")
    def test_category_code_unique_no_restriction(self):
        # Create
        self.env["product.category"].create({"name": "Test", "code": "A"})
        categories = self.env["product.category"].search([("code", "=", "A")])
        self.assertTrue(len(categories) > 1)
        # Write
        self.env["product.category"].search([("code", "=", "AA")]).write({"code": "AB"})
        categories = self.env["product.category"].search([("code", "=", "AB")])
        self.assertTrue(len(categories) > 1)

    @mute_logger("odoo.sql_db")
    def test_category_code_unique_whole_system(self):
        config = self.env["res.config.settings"].create({})
        config.write({"product_cat_code_unique_restriction": "system"})
        config.execute()
        # Create
        with self.assertRaises(ValidationError):
            self.env["product.category"].create({"name": "Test", "code": "AB"})
        categories = self.env["product.category"].search([("code", "=", "AB")])
        self.assertTrue(len(categories) == 1)
        with self.assertRaises(ValidationError):
            self.env["product.category"].search([("code", "=", "AA")]).write(
                {"code": "AB"}
            )
        categories = self.env["product.category"].search([("code", "=", "AB")])
        self.assertTrue(len(categories) == 1)

    @mute_logger("odoo.sql_db")
    def test_category_code_unique_parent_children(self):
        config = self.env["res.config.settings"].create({})
        config.write({"product_cat_code_unique_restriction": "direct"})
        config.execute()

        # Create
        cat = self.env["product.category"].search([("code", "=", "AB")])
        with self.assertRaises(ValidationError):
            self.env["product.category"].create(
                {
                    "name": "Test",
                    "code": cat.code,
                    "parent_id": cat.id,
                }
            )
        with self.assertRaises(ValidationError):
            cat.write({"child_id": [(0, 0, {"name": "Test", "code": cat.code})]})
        categories = self.env["product.category"].search([("code", "=", cat.code)])
        self.assertTrue(len(categories) == 1)
        last_cat = self.env["product.category"].search([("code", "=", "ABBB")], limit=1)

        # Write
        child_cat = self.env["product.category"].search(
            [("parent_id", "=", cat.id)], limit=1
        )
        with self.assertRaises(ValidationError):
            child_cat.write({"code": cat.code})
        with self.assertRaises(ValidationError):
            child_cat.child_id[0].write({"code": child_cat.code})
        categories = self.env["product.category"].search([("code", "=", cat.code)])
        self.assertTrue(len(categories) == 1)
        last_cat.write({"code": cat.code})
        categories = self.env["product.category"].search([("code", "=", cat.code)])
        self.assertTrue(len(categories) == 2)

    @mute_logger("odoo.sql_db")
    def test_category_code_unique_hierarchy(self):
        config = self.env["res.config.settings"].create({})
        config.write({"product_cat_code_unique_restriction": "hierarchy"})
        config.execute()

        # Create
        cat = self.env["product.category"].search([("code", "=", "AB")])
        last_cat = self.env["product.category"].search([("code", "=", "ABBB")], limit=1)
        with self.assertRaises(ValidationError):
            self.env["product.category"].create(
                {
                    "name": "Test",
                    "code": cat.code,
                    "parent_id": last_cat.id,
                }
            )
        categories = self.env["product.category"].search([("code", "=", cat.code)])
        self.assertTrue(len(categories) == 1)

        # Write
        with self.assertRaises(ValidationError):
            last_cat.write({"code": cat.code})
        categories = self.env["product.category"].search([("code", "=", cat.code)])
        self.assertTrue(len(categories) == 1)

    @mute_logger("odoo.sql_db")
    def test_category_code_unique_system_param(self):
        cat_a = self.env["product.category"].search([("code", "=", "AA")], limit=1)
        cat_b = self.env["product.category"].search([("code", "=", "AB")], limit=1)
        cat_b.write({"code": cat_a.code})
        categories = self.env["product.category"].search([("code", "=", cat_a.code)])
        self.assertTrue(len(categories) == 2)
        config = self.env["res.config.settings"].create({})
        with self.assertRaises(ValidationError):
            config.write({"product_cat_code_unique_restriction": "system"})
        config.execute()
        categories = self.env["product.category"].search([("code", "=", cat_a.code)])
        self.assertTrue(len(categories) == 2)
        self.assertFalse(
            self.env["ir.config_parameter"].get_param(
                "product_code_unique.product_code_unique_restriction"
            )
        )
        self.assertFalse(
            self.env["ir.config_parameter"].get_param(
                "product_code_unique.product_code_unique_restriction"
            )
        )
        cat_b.write({"code": "B"})
        config.write({"product_cat_code_unique_restriction": "system"})
        config.execute()
        param = self.env["ir.config_parameter"].get_param(
            "product_code_unique.product_code_unique_restriction"
        )
        self.assertEqual(param, "system")

    @mute_logger("odoo.sql_db")
    def test_category_code_unique_parent_children_param(self):
        cat = self.env["product.category"].search([("code", "=", "A")], limit=1)
        child_cat = self.env["product.category"].search(
            [("parent_id", "=", cat.id)], limit=1
        )
        child_cat.write({"code": cat.code})
        categories = self.env["product.category"].search([("code", "=", cat.code)])
        self.assertTrue(len(categories) == 2)
        config = self.env["res.config.settings"].create({})
        with self.assertRaises(ValidationError):
            config.write({"product_cat_code_unique_restriction": "direct"})
        config.execute()
        categories = self.env["product.category"].search([("code", "=", cat.code)])
        self.assertTrue(len(categories) == 2)
        self.assertFalse(
            self.env["ir.config_parameter"].get_param(
                "product_code_unique.product_code_unique_restriction"
            )
        )
        child_cat.write({"code": "B"})
        config.write({"product_cat_code_unique_restriction": "direct"})
        config.execute()
        param = self.env["ir.config_parameter"].get_param(
            "product_code_unique.product_code_unique_restriction"
        )
        self.assertEqual(param, "direct")

    @mute_logger("odoo.sql_db")
    def test_category_code_unique_hierarchy_param(self):
        cat = self.env["product.category"].search([("code", "=", "AB")], limit=1)
        last_cat = self.env["product.category"].search([("code", "=", "ABBB")], limit=1)
        last_cat.write({"code": cat.code})
        categories = self.env["product.category"].search([("code", "=", cat.code)])
        self.assertTrue(len(categories) == 2)
        config = self.env["res.config.settings"].create({})
        with self.assertRaises(ValidationError):
            config.write({"product_cat_code_unique_restriction": "hierarchy"})
        config.execute()
        categories = self.env["product.category"].search([("code", "=", cat.code)])
        self.assertTrue(len(categories) == 2)
        self.assertFalse(
            self.env["ir.config_parameter"].get_param(
                "product_code_unique.product_code_unique_restriction"
            )
        )
        last_cat.write({"code": "B"})
        config.write({"product_cat_code_unique_restriction": "hierarchy"})
        config.execute()
        param = self.env["ir.config_parameter"].get_param(
            "product_code_unique.product_code_unique_restriction"
        )
        self.assertEqual(param, "hierarchy")
