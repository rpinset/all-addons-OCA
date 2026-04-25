# Copyright 2025 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.stock_release_channel.tests.common import ReleaseChannelCase


class TestReleaseChannelPartnerAddress(ReleaseChannelCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Setup countries and states
        cls.italy = cls.env.ref("base.it")
        cls.ancona = cls.env.ref("base.state_it_an")
        cls.roma = cls.env.ref("base.state_it_rm")

        # Prepare partners by country and state
        cls.partner = cls.env["res.partner"].create({"name": "Partner w/o Country"})
        cls.partner_it = cls.env["res.partner"].create(
            {"name": "Partner IT", "country_id": cls.italy.id}
        )
        cls.partner_it_an = cls.env["res.partner"].create(
            {
                "name": "Partner IT Ancona",
                "country_id": cls.italy.id,
                "state_id": cls.ancona.id,
            }
        )

        # Prepare channels by country and state
        # First, make sure all existing channels are archived (to avoid issues w/
        # preexisting records)
        cls.env["stock.release.channel"].search([]).action_archive()
        # Then, create a channel for each possible combination of country and state
        cls.channel = cls.env["stock.release.channel"].create(
            {
                "name": "Channel",
                "country_ids": [],
                "state_ids": [],
                "state": "open",
                "collect_pickings": True,
            }
        )
        cls.channel_it = cls.env["stock.release.channel"].create(
            {
                "name": "Channel IT",
                "country_ids": [(4, cls.italy.id)],
                "state_ids": [],
                "state": "open",
                "collect_pickings": True,
            }
        )
        cls.channel_uk = cls.env["stock.release.channel"].create(
            {
                # We create this to make sure it is *excluded* when searching channels
                # for pickings linked to ``partner_it`` and ``partner_it_an``
                "name": "Channel UK",
                "country_ids": [(4, cls.env.ref("base.uk").id)],
                "state_ids": [],
                "state": "open",
                "collect_pickings": True,
            }
        )
        cls.channel_it_an = cls.env["stock.release.channel"].create(
            {
                "name": "Channel IT - Ancona",
                "country_ids": [(4, cls.italy.id)],
                "state_ids": [(4, cls.ancona.id)],
                "state": "open",
                "collect_pickings": True,
            }
        )
        cls.channel_it_rm = cls.env["stock.release.channel"].create(
            {
                # We create this to make sure it is *excluded* when searching channels
                # for pickings linked to ``partner_it_an``
                "name": "Channel IT - Roma",
                "country_ids": [(4, cls.italy.id)],
                "state_ids": [(4, cls.roma.id)],
                "state": "open",
                "collect_pickings": True,
            }
        )
        cls.channel_it_an_rm = cls.env["stock.release.channel"].create(
            {
                # We create this to make sure it is *included* when searching channels
                # for pickings linked to ``partner_it_an``
                "name": "Channel IT - Ancona+Roma",
                "country_ids": [(4, cls.italy.id)],
                "state_ids": [(4, cls.ancona.id), (4, cls.roma.id)],
                "state": "open",
                "collect_pickings": True,
            }
        )
        cls.all_channels = (
            cls.channel
            + cls.channel_it
            + cls.channel_it_an
            + cls.channel_it_rm
            + cls.channel_it_an_rm
            + cls.channel_uk
        )

    def test_picking_find_release_channel_match_by_address_no_country_no_state(self):
        move = self._create_single_move(self.product1, 5)
        move.picking_id.partner_id = self.partner
        self.assertEqual(
            move.picking_id._find_release_channel_possible_candidate(),
            self.channel,
        )

    def test_picking_find_release_channel_match_by_address_country_no_state(self):
        move = self._create_single_move(self.product1, 5)
        move.picking_id.partner_id = self.partner_it
        self.assertEqual(
            move.picking_id._find_release_channel_possible_candidate(),
            self.channel + self.channel_it,
        )

    def test_picking_find_release_channel_match_by_address_country_and_state(self):
        move = self._create_single_move(self.product1, 5)
        move.picking_id.partner_id = self.partner_it_an
        self.assertEqual(
            move.picking_id._find_release_channel_possible_candidate(),
            self.all_channels - (self.channel_uk + self.channel_it_rm),
        )
