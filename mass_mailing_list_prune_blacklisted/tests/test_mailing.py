# Copyright 2026 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import Common


class TestMailing(Common):
    def test_show_prune_wizard(self):
        """The wizard created from a Mailing is correct."""
        # Arrange
        blacklisted_contact = self.blacklisted_contact
        contact = self.contact
        mailing = self.mailing
        mailing_lists = mailing.contact_list_ids
        # pre-condition
        self.assertTrue(blacklisted_contact.is_blacklisted)
        self.assertFalse(contact.is_blacklisted)
        self.assertIn(contact, mailing_lists.contact_ids)
        self.assertIn(blacklisted_contact, mailing_lists.contact_ids)
        self.assertTrue(mailing.has_list_blacklisted_contacts)

        # Act
        wizard_action = mailing.show_prune_lists_wizard()

        # Assert
        wizard = self._get_records_from_action(wizard_action)
        self.assertEqual(wizard.list_ids, mailing_lists)
        self.assertIn(blacklisted_contact, wizard.blacklisted_contact_ids)
        self.assertNotIn(contact, wizard.blacklisted_contact_ids)
