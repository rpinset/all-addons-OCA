from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCalendarEventType(TransactionCase):
    def test_default_company_id(self):
        event_type = self.env["calendar.event.type"].create(
            {
                "name": "NAME",
            }
        )
        self.assertEqual(event_type.company_id, self.env.company)
