# Copyright 2026 Simone Rubino - PyTech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import Common


class TestPruneWizard(Common):
    def test_remove(self):
        """Blacklisted contacts are removed from mailing lists."""
        # Arrange
        blacklisted_contact = self.blacklisted_contact
        other_blacklisted_contact = self.other_blacklisted_contact
        contact = self.contact
        wizard = self.wizard
        mailing_lists = wizard.list_ids
        # pre-condition
        self.assertTrue(blacklisted_contact.is_blacklisted)
        self.assertTrue(other_blacklisted_contact.is_blacklisted)
        self.assertFalse(contact.is_blacklisted)
        self.assertIn(contact, mailing_lists.contact_ids)
        self.assertIn(blacklisted_contact, mailing_lists.contact_ids)
        self.assertIn(blacklisted_contact, wizard.blacklisted_contact_ids)
        self.assertIn(other_blacklisted_contact, mailing_lists.contact_ids)
        self.assertIn(other_blacklisted_contact, wizard.blacklisted_contact_ids)

        # Act
        wizard.remove_blacklisted_contacts()

        # Assert
        self.assertIn(contact, mailing_lists.contact_ids)
        self.assertNotIn(blacklisted_contact, mailing_lists.contact_ids)
        self.assertNotIn(other_blacklisted_contact, mailing_lists.contact_ids)
