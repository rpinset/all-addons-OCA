# Copyright 2025 Factor Libre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestProductLogisticsUomNetWeight(TransactionCase):
    """Test product_logistics_uom_net_weight module."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.weight_uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.weight_uom_g = cls.env.ref("uom.product_uom_gram")
        cls.env["ir.config_parameter"].set_param("product.weight_in_lbs", "0")

        # Create test products
        cls.product_simple = cls.env["product.product"].create(
            {
                "name": "Test Simple Product",
                "type": "product",
            }
        )

        cls.product_template = cls.env["product.template"].create(
            {
                "name": "Test Template Product",
                "type": "product",
            }
        )

        # Create attribute for variant testing
        cls.attribute = cls.env["product.attribute"].create(
            {
                "name": "Test Attribute",
                "display_type": "select",
            }
        )
        cls.value1 = cls.env["product.attribute.value"].create(
            {
                "name": "Value 1",
                "attribute_id": cls.attribute.id,
            }
        )
        cls.value2 = cls.env["product.attribute.value"].create(
            {
                "name": "Value 2",
                "attribute_id": cls.attribute.id,
            }
        )

    def test_01_product_net_weight_same_uom(self):
        """Test product_net_weight when using same UoM as system."""
        # Set weight UoM to kg (same as system)
        self.product_simple.weight_uom_id = self.weight_uom_kg
        self.product_simple.net_weight = 1.0  # 1 kg

        # product_net_weight should be same as net_weight
        self.assertEqual(self.product_simple.product_net_weight, 1.0)

        # Test inverse - set product_net_weight
        self.product_simple.product_net_weight = 2.0
        self.assertEqual(self.product_simple.net_weight, 2.0)

    def test_02_product_net_weight_different_uom(self):
        """Test product_net_weight conversion with different UoM."""
        # Set weight UoM to grams
        self.product_simple.weight_uom_id = self.weight_uom_g
        self.product_simple.net_weight = 1.0  # 1 kg in system

        # product_net_weight should be 1000g
        self.assertEqual(self.product_simple.product_net_weight, 1000.0)

        # Test inverse - set product_net_weight to 500g
        self.product_simple.product_net_weight = 500.0
        self.assertEqual(self.product_simple.net_weight, 0.5)  # 0.5 kg

    def test_03_template_net_weight_single_variant(self):
        """Test template net weight with single variant."""
        product = self.product_template.product_variant_ids[0]
        self.assertEqual(len(self.product_template.product_variant_ids), 1)

        # Set weight UoM and net weight on template
        self.product_template.weight_uom_id = self.weight_uom_g
        self.product_template.product_net_weight = 1000.0  # 1000g

        # Check template computes from variant
        self.assertEqual(product.product_net_weight, 1000.0)
        self.assertEqual(product.net_weight, 1.0)  # 1kg in system

    def test_04_template_net_weight_multiple_variants(self):
        """Test template net weight with multiple variants."""
        # Add attribute to create variants
        self.product_template.write(
            {
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": self.attribute.id,
                            "value_ids": [(6, 0, [self.value1.id, self.value2.id])],
                        },
                    )
                ]
            }
        )

        # Should have 2 variants now
        self.assertEqual(len(self.product_template.product_variant_ids), 2)

        # Template should have 0.0 for multiple variants
        self.assertEqual(self.product_template.product_net_weight, 0.0)

    def test_05_template_prepare_variant_values(self):
        """Test _prepare_variant_values method."""
        self.product_template.weight_uom_id = self.weight_uom_g
        self.product_template.product_net_weight = 500.0

        # Create empty combination recordset
        combination = self.env["product.template.attribute.value"]
        values = self.product_template._prepare_variant_values(combination)

        # Should include product_net_weight
        self.assertIn("product_net_weight", values)
        self.assertEqual(values["product_net_weight"], 500.0)

    def test_06_validation_fixed_different_uom(self):
        """Test that validation error is fixed with different UoM."""
        # This should NOT raise ValidationError anymore
        product = self.env["product.product"].create(
            {
                "name": "Test Validation Product",
                "weight_uom_id": self.weight_uom_g.id,
                "net_weight": 0.8,  # 0.8 kg = 800g in system UoM
                "weight": 1.0,  # 1 kg gross weight
            }
        )

        # Verify the product was created successfully
        self.assertTrue(product.id)
        self.assertEqual(product.net_weight, 0.8)
        self.assertEqual(product.weight, 1.0)
        self.assertEqual(product.product_net_weight, 800.0)  # 800g

    def test_07_validation_still_works_same_uom(self):
        """Test that validation still works correctly with same UoM."""
        # This SHOULD still raise ValidationError
        with self.assertRaises(ValidationError):
            self.env["product.product"].create(
                {
                    "name": "Test Invalid Product",
                    "weight_uom_id": self.weight_uom_kg.id,  # Same as system UoM
                    "net_weight": 1.2,  # 1.2 kg net
                    "weight": 1.0,  # 1 kg gross (invalid!)
                }
            )

    def test_08_product_form_integration(self):
        """Test product creation and field assignment."""
        # Create product with direct assignment (fields not in default view)
        product = self.env["product.product"].create(
            {
                "name": "Form Test Product",
                "weight_uom_id": self.weight_uom_g.id,
            }
        )

        # Set product_net_weight and check conversions
        product.product_net_weight = 750.0  # 750g

        # Check conversions
        self.assertEqual(product.product_net_weight, 750.0)
        self.assertEqual(product.net_weight, 0.75)  # 0.75 kg

    def test_09_template_form_integration(self):
        """Test template creation and field assignment."""
        # Create template with direct assignment
        template = self.env["product.template"].create(
            {
                "name": "Template Form Test",
                "weight_uom_id": self.weight_uom_g.id,
            }
        )

        # Set product_net_weight and check conversions
        template.product_net_weight = 900.0  # 900g

        # Check template and variant
        self.assertEqual(template.product_net_weight, 900.0)
        variant = template.product_variant_ids[0]
        self.assertEqual(variant.product_net_weight, 900.0)
        self.assertEqual(variant.net_weight, 0.9)  # 0.9 kg

    def test_10_edge_case_zero_values(self):
        """Test edge cases with zero values."""
        self.product_simple.weight_uom_id = self.weight_uom_g

        # Set product_net_weight to 0
        self.product_simple.product_net_weight = 0.0
        self.assertEqual(self.product_simple.net_weight, 0.0)

        # Set net_weight to 0
        self.product_simple.net_weight = 0.0
        self.assertEqual(self.product_simple.product_net_weight, 0.0)

    def test_11_compute_depends(self):
        """Test that compute dependencies work correctly."""
        product = self.product_simple
        product.weight_uom_id = self.weight_uom_g
        product.net_weight = 1.0

        initial_weight = product.product_net_weight
        self.assertEqual(initial_weight, 1000.0)

        # Change UoM - should trigger recompute
        product.weight_uom_id = self.weight_uom_kg
        new_weight = product.product_net_weight
        self.assertEqual(new_weight, 1.0)  # Same as net_weight now

        # Change net_weight - should trigger recompute
        product.net_weight = 2.0
        final_weight = product.product_net_weight
        self.assertEqual(final_weight, 2.0)
