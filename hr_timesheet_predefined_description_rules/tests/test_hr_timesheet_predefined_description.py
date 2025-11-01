# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form, TransactionCase


class TestTimesheetPredefinedDescription(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Description = cls.env["timesheet.predefined.description"]
        cls.base_description = cls.Description.create(
            {
                "name": "Base Description",
                "allow_free_text": True,
            }
        )

    def test_onchange_disables_fields_when_allow_free_text_is_false(self):
        description = self.base_description.copy(
            {
                "free_text_required": True,
                "append_free_text_to_name": True,
            }
        )
        with Form(description) as form:
            form.allow_free_text = False
            self.assertFalse(form.free_text_required)
            self.assertFalse(form.append_free_text_to_name)

    def test_free_text_required_stays_true_if_enabled(self):
        description = self.base_description.copy(
            {
                "free_text_required": True,
            }
        )
        self.assertTrue(description.free_text_required)

    def test_append_free_text_to_name_stays_true_if_enabled(self):
        description = self.base_description.copy(
            {
                "append_free_text_to_name": True,
            }
        )
        self.assertTrue(description.append_free_text_to_name)
