# Copyright 2021 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import Command
from odoo.tests import TransactionCase


class TestFleetVehicleInspectionTemplate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.inspection = cls.env["fleet.vehicle.inspection"]
        cls.inspection_item = cls.env["fleet.vehicle.inspection.item"]
        cls.inspection_template = cls.env["fleet.vehicle.inspection.template"]
        cls.brand = cls.env["fleet.vehicle.model.brand"].create({"name": "Test Brand"})
        cls.model = cls.env["fleet.vehicle.model"].create(
            {
                "name": "Test Model",
                "brand_id": cls.brand.id,
            }
        )
        cls.vehicle = cls.env["fleet.vehicle"].create(
            {
                "name": "Test Vehicle",
                "model_id": cls.model.id,
            }
        )

        cls.item_01 = cls.inspection_item.create({"name": "Lights"})

        cls.item_02 = cls.inspection_item.create({"name": "Mirrors"})

        cls.inspection_template_01 = cls.inspection_template.create(
            {
                "name": "TemplateTest_01",
                "inspection_template_line_ids": [
                    Command.create({"inspection_template_item_id": cls.item_01.id}),
                    Command.create({"inspection_template_item_id": cls.item_02.id}),
                ],
            }
        )

        cls.inspection_template_02 = cls.inspection_template.create(
            {
                "name": "TemplateTest_02",
                "inspection_template_line_ids": [
                    Command.create(
                        {
                            "inspection_template_item_id": cls.item_01.id,
                            "sequence": 11,
                        },
                    ),
                    Command.create(
                        {
                            "inspection_template_item_id": cls.item_02.id,
                            "sequence": 10,
                        },
                    ),
                ],
            }
        )

        cls.inspection = cls.inspection.create(
            {
                "vehicle_id": cls.vehicle.id,
                "inspection_template_id": cls.inspection_template_01.id,
            }
        )

    def test_fleet_vehicle_inspection(self):
        self.inspection._onchange_inspection_template_id()

        self.assertEqual(self.inspection.name, self.inspection_template_01.name)
        self.assertTrue(self.inspection.inspection_line_ids)

        self.inspection.inspection_template_id = self.inspection_template_02

        self.inspection._onchange_inspection_template_id()

        self.assertEqual(len(self.inspection.inspection_line_ids), 2)

        line_1 = self.inspection.inspection_line_ids.filtered(
            lambda linei: linei.inspection_item_id == self.item_01
        )
        self.assertEqual(line_1.sequence, 11)

        self.inspection.inspection_template_id = False

        self.inspection._onchange_inspection_template_id()

        self.assertEqual(self.inspection.name, self.inspection_template_02.name)
        self.assertNotEqual(self.inspection.name, self.inspection_template_01.name)

        self.assertTrue(self.inspection.inspection_line_ids)
        self.assertEqual(len(self.inspection.inspection_line_ids), 2)
