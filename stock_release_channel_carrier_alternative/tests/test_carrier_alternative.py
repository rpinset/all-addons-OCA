# Copyright 2025 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Command

from odoo.addons.queue_job.job import identity_exact
from odoo.addons.queue_job.tests.common import trap_jobs
from odoo.addons.stock_available_to_promise_release_carrier_alternative.tests.common import (  # noqa: E501
    DeliveryCarrierAlternativeCommon,
)


class TestStockReleaseChannelCarrierAlternative(DeliveryCarrierAlternativeCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.default_channel = cls.env.ref(
            "stock_release_channel.stock_release_channel_default"
        )
        cls.default_channel.picking_type_ids = [
            Command.set(cls.delivery.picking_type_id.ids)
        ]
        cls.wh.delivery_route_id.no_backorder_at_release = False
        # create route
        cls.the_poste_route = cls.wh.delivery_route_id.copy({"name": "The poste route"})
        delivery_rule = cls.the_poste_route.rule_ids.filtered(
            lambda r: r.location_dest_id
            == cls.env.ref("stock.stock_location_customers")
        )
        delivery_rule.picking_type_id = cls.wh.out_type_id.copy()
        # create channel the poste
        cls.the_poste_channel = cls.default_channel.copy(
            {
                "picking_type_ids": [Command.set(delivery_rule.picking_type_id.ids)],
            }
        )

    def test_no_alternative_with_channel(self):
        """The delivery has no alternative, remains in channel"""
        self.the_poste_carrier.route_ids = [Command.set(self.the_poste_route.ids)]
        self.env["stock.quant"]._update_available_quantity(
            self.product1, self.loc_stock, 3
        )
        moves = self.delivery.move_ids
        self.delivery.release_channel_id = self.default_channel
        self.the_poste_channel.state = "open"
        self.the_poste_channel.collect_pickings = True
        self.delivery.release_available_to_promise()
        new_delivery = moves.picking_id
        self.assertEqual(new_delivery.release_channel_id, self.default_channel)
        self.assertFalse(new_delivery.need_release)

    def test_bo_alternative_with_channel(self):
        """The delivery with the alternative carrier is assigned a new channel

        Backorder at release
        """
        self.the_poste_carrier.route_ids = [Command.set(self.the_poste_route.ids)]
        self.set_alternatives()
        self.env["stock.quant"]._update_available_quantity(
            self.product1, self.loc_stock, 3
        )
        moves = self.delivery.move_ids
        self.delivery.release_channel_id = self.default_channel
        self.the_poste_channel.state = "open"
        self.the_poste_channel.collect_pickings = True
        with trap_jobs() as trap:
            self.delivery.release_available_to_promise()
            backorder = self.delivery
            trap.assert_jobs_count(1)
            trap.assert_enqueued_job(
                backorder.assign_release_channel,
                args=(),
                kwargs={},
                properties=dict(
                    identity_key=identity_exact,
                ),
            )
        new_delivery = moves.picking_id
        self.assertEqual(new_delivery.release_channel_id, self.the_poste_channel)
        self.assertFalse(new_delivery.need_release)

    def test_bo_alternative_without_channel(self):
        """The delivery with the alternative carrier is not assigned a channel

        Backorder at release
        """
        self.the_poste_carrier.route_ids = [Command.set(self.the_poste_route.ids)]
        self.set_alternatives()
        self.env["stock.quant"]._update_available_quantity(
            self.product1, self.loc_stock, 3
        )
        moves = self.delivery.move_ids
        self.delivery.release_channel_id = self.default_channel
        with trap_jobs() as trap:
            self.delivery.release_available_to_promise()
            backorder = self.delivery
            trap.assert_jobs_count(1)
            trap.assert_enqueued_job(
                backorder.assign_release_channel,
                args=(),
                kwargs={},
                properties=dict(
                    identity_key=identity_exact,
                ),
            )
        new_delivery = moves.picking_id
        self.assertFalse(new_delivery.release_channel_id)
        self.assertTrue(new_delivery.need_release)

    def test_nobo_alternative_with_channel(self):
        """The delivery with the alternative carrier is assigned a new channel

        No backorder at release
        """
        self.wh.delivery_route_id.no_backorder_at_release = True
        self.test_bo_alternative_with_channel()

    def test_nobo_alternative_without_channel(self):
        """The delivery with the alternative carrier is not assigned a channel

        No backorder at release
        """
        self.wh.delivery_route_id.no_backorder_at_release = True
        self.test_bo_alternative_without_channel()
