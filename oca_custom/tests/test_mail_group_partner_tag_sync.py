from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestMailGroupPartnerTagSync(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.Tag = cls.env["res.partner.category"].sudo()
        cls.Partner = cls.env["res.partner"].sudo()
        cls.Group = cls.env["mail.group"].sudo()
        cls.Member = cls.env["mail.group.member"].sudo()

        cls.tag = cls.Tag.create({"name": "Board"})
        cls.other_tag = cls.Tag.create({"name": "Other"})

        cls.partner_tagged = cls.Partner.create(
            {
                "name": "Alice",
                "email": "alice@example.com",
                "category_id": [(4, cls.tag.id)],
            }
        )
        cls.partner_untagged = cls.Partner.create(
            {"name": "Partner 1", "email": "test@example.com"}
        )

    def _create_group(self, name, tag=None):
        vals = {
            "name": name,
            "alias_name": name.lower().replace(" ", "_"),
        }
        if tag:
            vals["partner_tag_id"] = tag.id
        return self.Group.create(vals)

    def test_mail_group_action_sync_adds_and_removes(self):
        """action_sync_members_from_tag must:
        - add partners having the tag
        - remove partners that do not have the tag
        """
        group = self._create_group("Board Group", tag=self.tag)

        # Manually add an untagged member -> should be removed by sync
        self.Member.create(
            {"mail_group_id": group.id, "partner_id": self.partner_untagged.id}
        )

        group.action_sync_members_from_tag()

        self.assertEqual(
            self.Member.search_count(
                [
                    ("mail_group_id", "=", group.id),
                    ("partner_id", "=", self.partner_tagged.id),
                ]
            ),
            1,
            "Tagged partner must be a member after sync.",
        )
        self.assertEqual(
            self.Member.search_count(
                [
                    ("mail_group_id", "=", group.id),
                    ("partner_id", "=", self.partner_untagged.id),
                ]
            ),
            0,
            "Untagged partner must be removed by sync.",
        )

    def test_mail_group_write_partner_tag_id_triggers_sync(self):
        """Writing partner_tag_id on mail.group should trigger a sync after write()."""
        group = self._create_group("Config Group", tag=None)

        # Add Partner 1 manually; when tag is set, sync should remove him
        self.Member.create(
            {"mail_group_id": group.id, "partner_id": self.partner_untagged.id}
        )

        group.write({"partner_tag_id": self.tag.id})

        self.assertEqual(
            self.Member.search_count(
                [
                    ("mail_group_id", "=", group.id),
                    ("partner_id", "=", self.partner_tagged.id),
                ]
            ),
            1,
            "Tagged partner must be added when partner_tag_id is configured.",
        )
        self.assertEqual(
            self.Member.search_count(
                [
                    ("mail_group_id", "=", group.id),
                    ("partner_id", "=", self.partner_untagged.id),
                ]
            ),
            0,
            "Non-tagged member must be removed when partner_tag_id is configured.",
        )

    def test_partner_tag_add_remove_updates_group_membership(self):
        """Partner tag delta must add/remove mail.group.member rows."""
        group = self._create_group("Delta Group", tag=self.tag)

        # Initially Partner 1 is not tagged -> not a member
        self.assertEqual(
            self.Member.search_count(
                [
                    ("mail_group_id", "=", group.id),
                    ("partner_id", "=", self.partner_untagged.id),
                ]
            ),
            0,
        )

        # Add tag -> must become member (res.partner.write hook)
        self.partner_untagged.write({"category_id": [(4, self.tag.id)]})
        self.assertEqual(
            self.Member.search_count(
                [
                    ("mail_group_id", "=", group.id),
                    ("partner_id", "=", self.partner_untagged.id),
                ]
            ),
            1,
            "Adding the tag to partner must add them to the configured group.",
        )

        # Remove tag -> must be removed from group
        self.partner_untagged.write({"category_id": [(3, self.tag.id)]})
        self.assertEqual(
            self.Member.search_count(
                [
                    ("mail_group_id", "=", group.id),
                    ("partner_id", "=", self.partner_untagged.id),
                ]
            ),
            0,
            "Removing the tag from partner must remove them from the configured group.",
        )

    def test_partner_write_no_duplicate_memberships(self):
        """Repeated writes that do not change tags must not create duplicate members."""
        group = self._create_group("No Dups Group", tag=self.tag)

        # Add tag once -> member created
        self.partner_untagged.write({"category_id": [(4, self.tag.id)]})
        self.assertEqual(
            self.Member.search_count(
                [
                    ("mail_group_id", "=", group.id),
                    ("partner_id", "=", self.partner_untagged.id),
                ]
            ),
            1,
        )

        # Write same tag again (no change) -> must still be exactly 1 membership
        self.partner_untagged.write({"category_id": [(4, self.tag.id)]})
        self.assertEqual(
            self.Member.search_count(
                [
                    ("mail_group_id", "=", group.id),
                    ("partner_id", "=", self.partner_untagged.id),
                ]
            ),
            1,
            "Re-applying same tag must not duplicate mail.group.member.",
        )

        # Write unrelated field -> must still be 1 membership
        self.partner_untagged.write({"name": "Partner 1 Updated"})
        self.assertEqual(
            self.Member.search_count(
                [
                    ("mail_group_id", "=", group.id),
                    ("partner_id", "=", self.partner_untagged.id),
                ]
            ),
            1,
            "Unrelated partner writes must not affect membership count.",
        )

    def test_partner_create_with_tag_creates_membership(self):
        """Partner create override should add membership when created with the tag."""
        group = self._create_group("Create Group", tag=self.tag)

        new_partner = self.Partner.create(
            {
                "name": "Partner 2",
                "email": "test_2@example.com",
                "category_id": [(6, 0, [self.tag.id])],
            }
        )

        self.assertEqual(
            self.Member.search_count(
                [("mail_group_id", "=", group.id), ("partner_id", "=", new_partner.id)]
            ),
            1,
            "Creating a tagged partner must create group membership.",
        )
