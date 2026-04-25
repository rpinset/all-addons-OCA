# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestRepairCalendar(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.RepairOrder = cls.env["repair.order"]
        cls.IrConfig = cls.env["ir.config_parameter"].sudo()
        cls.IrConfig.set_param(
            "repair_scheduled_date_calendar_view.planned_duration_default", 1.0
        )

    def test_default_planned_duration(self):
        """Default planned_duration should be 1.0 (set in setUpClass)."""
        order = self.RepairOrder.create({"name": "Test Repair"})
        self.assertEqual(order.planned_duration, 1.0)

    def test_changed_default_duration(self):
        """planned_duration should follow updated config default."""
        self.IrConfig.set_param(
            "repair_scheduled_date_calendar_view.planned_duration_default", 2.5
        )
        order = self.RepairOrder.create({"name": "Repair 2"})
        self.assertEqual(order.planned_duration, 2.5)

    def test_manual_override_custom_value(self):
        """Explicit manual value must not be overwritten (e.g., 4.0)."""
        order = self.RepairOrder.create({"name": "Repair 3", "planned_duration": 4.0})
        self.assertEqual(order.planned_duration, 4.0)

    def test_manual_override_one_hour_is_preserved(self):
        """Explicit 1.0 should be preserved when not coming from calendar."""
        order = self.RepairOrder.create({"name": "Repair 1h", "planned_duration": 1.0})
        self.assertEqual(order.planned_duration, 1.0)

    def test_manual_override_twelve_hours_is_preserved(self):
        """Explicit 12.0 should be preserved when not coming from calendar."""
        order = self.RepairOrder.create(
            {"name": "Repair 12h", "planned_duration": 12.0}
        )
        self.assertEqual(order.planned_duration, 12.0)

    def test_schedule_date_is_set(self):
        """schedule_date should be set by core default on creation."""
        order = self.RepairOrder.create({"name": "Repair 4"})
        self.assertTrue(order.schedule_date)
        # Be tolerant to execution delays (no strict 'now' proximity needed)
        self.assertIsInstance(order.schedule_date, type(fields.Datetime.now()))
        # Optional: soft proximity check (generous tolerance)
        self.assertLessEqual(
            abs((order.schedule_date - fields.Datetime.now()).total_seconds()), 120
        )

    def test_negative_duration_raises(self):
        """Negative duration must raise ValidationError."""
        with self.assertRaises(ValidationError):
            self.RepairOrder.create({"name": "Repair 6", "planned_duration": -2.0})
