# Copyright 2019 Camptocamp (https://www.camptocamp.com)
# Copyright 2019-2021 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>

from odoo import exceptions, fields

from .common import ReserveRuleCommon


class TestReserveRule(ReserveRuleCommon):
    def test_removal_rule_location_child_of_rule_location(self):
        # removal rule location is a child
        self._create_rule({}, [{"location_id": self.loc_zone1.id}])
        # removal rule location is not a child
        with self.assertRaises(exceptions.ValidationError):
            self._create_rule(
                {}, [{"location_id": self.env.ref("stock.stock_location_locations").id}]
            )

    def test_rule_take_all_in_2(self):
        all_locs = (
            self.loc_zone1_bin1,
            self.loc_zone1_bin2,
            self.loc_zone2_bin1,
            self.loc_zone2_bin2,
            self.loc_zone3_bin1,
            self.loc_zone3_bin2,
        )
        for loc in all_locs:
            self._update_qty_in_location(loc, self.product1, 100)

        picking = self._create_picking(self.wh, [(self.product1, 200)])

        self._create_rule(
            {},
            [
                {"location_id": self.loc_zone1.id, "sequence": 2},
                {"location_id": self.loc_zone2.id, "sequence": 1},
                {"location_id": self.loc_zone3.id, "sequence": 3},
            ],
        )

        picking.action_assign()
        move = picking.move_ids
        ml = move.move_line_ids
        self.assertRecordValues(
            ml,
            [
                {"location_id": self.loc_zone2_bin1.id, "quantity": 100},
                {"location_id": self.loc_zone2_bin2.id, "quantity": 100},
            ],
        )
        self.assertEqual(move.state, "assigned")

    def test_rule_match_parent(self):
        all_locs = (
            self.loc_zone1_bin1,
            self.loc_zone1_bin2,
            self.loc_zone2_bin1,
            self.loc_zone2_bin2,
            self.loc_zone3_bin1,
            self.loc_zone3_bin2,
        )
        for loc in all_locs:
            self._update_qty_in_location(loc, self.product1, 100)

        picking = self._create_picking(
            self.wh, [(self.product1, 200)], self.loc_zone1.id
        )

        self._create_rule(
            {},
            [
                {"location_id": self.loc_zone1.id, "sequence": 2},
                {"location_id": self.loc_zone2.id, "sequence": 1},
                {"location_id": self.loc_zone3.id, "sequence": 3},
            ],
        )

        picking.action_assign()
        move = picking.move_ids
        ml = move.move_line_ids
        self.assertRecordValues(
            ml,
            [
                {"location_id": self.loc_zone1_bin1.id, "quantity": 100},
                {"location_id": self.loc_zone1_bin2.id, "quantity": 100},
            ],
        )
        self.assertEqual(move.state, "assigned")

    def test_rule_take_all_in_2_and_3(self):
        self._update_qty_in_location(self.loc_zone1_bin1, self.product1, 100)
        self._update_qty_in_location(self.loc_zone2_bin1, self.product1, 100)
        self._update_qty_in_location(self.loc_zone3_bin1, self.product1, 100)
        picking = self._create_picking(self.wh, [(self.product1, 150)])

        self._create_rule(
            {},
            [
                {"location_id": self.loc_zone1.id, "sequence": 3},
                {"location_id": self.loc_zone2.id, "sequence": 1},
                {"location_id": self.loc_zone3.id, "sequence": 2},
            ],
        )

        picking.action_assign()
        move = picking.move_ids
        ml = move.move_line_ids
        self.assertRecordValues(
            ml,
            [
                {"location_id": self.loc_zone2_bin1.id, "quantity": 100},
                {"location_id": self.loc_zone3_bin1.id, "quantity": 50},
            ],
        )
        self.assertEqual(move.state, "assigned")

    def test_rule_remaining(self):
        self._update_qty_in_location(self.loc_zone1_bin1, self.product1, 100)
        self._update_qty_in_location(self.loc_zone2_bin1, self.product1, 100)
        self._update_qty_in_location(self.loc_zone3_bin1, self.product1, 100)
        picking = self._create_picking(self.wh, [(self.product1, 400)])

        self._create_rule(
            {},
            [
                {"location_id": self.loc_zone1.id, "sequence": 3},
                {"location_id": self.loc_zone2.id, "sequence": 1},
                {"location_id": self.loc_zone3.id, "sequence": 2},
            ],
        )

        picking.action_assign()
        move = picking.move_ids
        ml = move.move_line_ids
        self.assertRecordValues(
            ml,
            [
                {"location_id": self.loc_zone2_bin1.id, "quantity": 100},
                {"location_id": self.loc_zone3_bin1.id, "quantity": 100},
                {"location_id": self.loc_zone1_bin1.id, "quantity": 100},
            ],
        )
        self.assertEqual(move.state, "partially_available")
        self.assertEqual(move.quantity, 300.0)

    def test_rule_domain(self):
        self._update_qty_in_location(self.loc_zone1_bin1, self.product1, 100)
        self._update_qty_in_location(self.loc_zone2_bin1, self.product1, 100)
        self._update_qty_in_location(self.loc_zone3_bin1, self.product1, 100)
        picking = self._create_picking(self.wh, [(self.product1, 200)])

        domain = [("product_id", "!=", self.product1.id)]
        self._create_rule(
            {"rule_domain": domain, "sequence": 1},
            [
                # this rule should be excluded by the domain
                {"location_id": self.loc_zone1.id, "sequence": 1}
            ],
        )
        self._create_rule(
            {"sequence": 2},
            [
                {"location_id": self.loc_zone2.id, "sequence": 1},
                {"location_id": self.loc_zone3.id, "sequence": 2},
            ],
        )
        picking.action_assign()
        move = picking.move_ids
        ml = move.move_line_ids
        self.assertRecordValues(
            ml,
            [
                {"location_id": self.loc_zone2_bin1.id, "quantity": 100},
                {"location_id": self.loc_zone3_bin1.id, "quantity": 100},
            ],
        )
        self.assertEqual(move.state, "assigned")

    def test_picking_type(self):
        self._update_qty_in_location(self.loc_zone1_bin1, self.product1, 100)
        self._update_qty_in_location(self.loc_zone2_bin1, self.product1, 100)
        self._update_qty_in_location(self.loc_zone3_bin1, self.product1, 100)
        picking = self._create_picking(self.wh, [(self.product1, 200)])

        self._create_rule(
            # different picking, should be excluded
            {"picking_type_ids": [(6, 0, self.wh.int_type_id.ids)], "sequence": 1},
            [{"location_id": self.loc_zone1.id, "sequence": 1}],
        )
        self._create_rule(
            # same picking type as the move
            {"picking_type_ids": [(6, 0, self.wh.pick_type_id.ids)], "sequence": 2},
            [
                {"location_id": self.loc_zone2.id, "sequence": 1},
                {"location_id": self.loc_zone3.id, "sequence": 2},
            ],
        )
        picking.action_assign()
        move = picking.move_ids
        ml = move.move_line_ids
        self.assertRecordValues(
            ml,
            [
                {"location_id": self.loc_zone2_bin1.id, "quantity": 100},
                {"location_id": self.loc_zone3_bin1.id, "quantity": 100},
            ],
        )
        self.assertEqual(move.state, "assigned")

    def test_quant_domain(self):
        self._update_qty_in_location(self.loc_zone1_bin1, self.product1, 100)
        self._update_qty_in_location(self.loc_zone2_bin1, self.product1, 100)
        self._update_qty_in_location(self.loc_zone3_bin1, self.product1, 100)
        picking = self._create_picking(self.wh, [(self.product1, 200)])

        domain = [("quantity", ">", 200)]
        self._create_rule(
            {},
            [
                # This rule is not excluded by the domain,
                # but the quant will be as the quantity is less than 200.
                {
                    "location_id": self.loc_zone1.id,
                    "sequence": 1,
                    "quant_domain": domain,
                },
                {"location_id": self.loc_zone2.id, "sequence": 2},
                {"location_id": self.loc_zone3.id, "sequence": 3},
            ],
        )
        picking.action_assign()
        move = picking.move_ids
        ml = move.move_line_ids
        self.assertRecordValues(
            ml,
            [
                {"location_id": self.loc_zone2_bin1.id, "quantity": 100},
                {"location_id": self.loc_zone3_bin1.id, "quantity": 100},
            ],
        )
        self.assertEqual(move.state, "assigned")

    def test_rule_empty_bin(self):
        self._update_qty_in_location(self.loc_zone1_bin1, self.product1, 300)
        self._update_qty_in_location(self.loc_zone1_bin2, self.product1, 150)
        self._update_qty_in_location(self.loc_zone2_bin1, self.product1, 50)
        self._update_qty_in_location(self.loc_zone3_bin1, self.product1, 100)
        picking = self._create_picking(self.wh, [(self.product1, 250)])

        self._create_rule(
            {},
            [
                # This rule should be excluded for zone1 / bin1 because the
                # bin would not be empty, but applied on zone1 / bin2.
                {
                    "location_id": self.loc_zone1.id,
                    "sequence": 1,
                    "removal_strategy": "empty_bin",
                },
                # this rule should be applied because we will empty the bin
                {
                    "location_id": self.loc_zone2.id,
                    "sequence": 2,
                    "removal_strategy": "empty_bin",
                },
                {"location_id": self.loc_zone3.id, "sequence": 3},
            ],
        )
        picking.action_assign()
        move = picking.move_ids
        ml = move.move_line_ids

        self.assertRecordValues(
            ml,
            [
                {"location_id": self.loc_zone1_bin2.id, "quantity": 150.0},
                {"location_id": self.loc_zone2_bin1.id, "quantity": 50.0},
                {"location_id": self.loc_zone3_bin1.id, "quantity": 50.0},
            ],
        )
        self.assertEqual(move.state, "assigned")

    def test_rule_empty_bin_partial(self):
        self._update_qty_in_location(self.loc_zone1_bin1, self.product1, 50)
        self._update_qty_in_location(self.loc_zone1_bin2, self.product1, 50)
        self._update_qty_in_location(self.loc_zone2_bin1, self.product1, 50)
        picking = self._create_picking(self.wh, [(self.product1, 80)])

        self._create_rule(
            {},
            [
                {
                    "location_id": self.loc_zone1.id,
                    "sequence": 1,
                    "removal_strategy": "empty_bin",
                },
                {"location_id": self.loc_zone2.id, "sequence": 2},
            ],
        )
        picking.action_assign()
        move = picking.move_ids
        ml = move.move_line_ids

        # We expect to take 50 in zone1/bin1 as it will empty a bin,
        # but zone1/bin2 must not be used as it would not empty it.

        self.assertRecordValues(
            ml,
            [
                {"location_id": self.loc_zone1_bin1.id, "quantity": 50.0},
                {"location_id": self.loc_zone2_bin1.id, "quantity": 30.0},
            ],
        )
        self.assertEqual(move.state, "assigned")

    def test_rule_empty_bin_fifo(self):
        self._update_qty_in_location(
            self.loc_zone1_bin1,
            self.product1,
            30,
            in_date=fields.Datetime.to_datetime("2021-01-04 12:00:00"),
        )
        self._update_qty_in_location(
            self.loc_zone1_bin2,
            self.product1,
            60,
            in_date=fields.Datetime.to_datetime("2021-01-02 12:00:00"),
        )
        self._update_qty_in_location(
            self.loc_zone2_bin1,
            self.product1,
            50,
            in_date=fields.Datetime.to_datetime("2021-01-05 12:00:00"),
        )
        picking = self._create_picking(self.wh, [(self.product1, 80)])

        self._create_rule(
            {},
            [
                {
                    "location_id": self.loc_zone1.id,
                    "sequence": 1,
                    "removal_strategy": "empty_bin",
                },
                {"location_id": self.loc_zone2.id, "sequence": 2},
            ],
        )
        picking.action_assign()
        move = picking.move_ids
        ml = move.move_line_ids

        # We expect to take 60 in zone1/bin2 as it will empty a bin and
        # respecting fifo, the 60 of zone2 should be taken before the 30 of
        # zone1. Then, as zone1/bin1 would not be empty, it is discarded. The
        # remaining is taken in zone2 which has no rule.
        self.assertRecordValues(
            ml,
            [
                {"location_id": self.loc_zone1_bin2.id, "quantity": 60.0},
                {"location_id": self.loc_zone2_bin1.id, "quantity": 20.0},
            ],
        )
        self.assertEqual(move.state, "assigned")

    def test_rule_empty_bin_multiple_allocation(self):
        self._update_qty_in_location(self.loc_zone1_bin1, self.product1, 10)
        self._update_qty_in_location(self.loc_zone1_bin1, self.product2, 10)
        self._update_qty_in_location(self.loc_zone2_bin1, self.product1, 10)
        picking = self._create_picking(self.wh, [(self.product1, 10)])

        self._create_rule(
            {},
            [
                # This rule should be excluded for zone1 / bin1 because the
                # bin would not be empty
                {
                    "location_id": self.loc_zone1.id,
                    "sequence": 1,
                    "removal_strategy": "empty_bin",
                },
                {"location_id": self.loc_zone2.id, "sequence": 2},
            ],
        )
        picking.action_assign()
        move = picking.move_ids
        ml = move.move_line_ids

        self.assertRecordValues(
            ml,
            [
                {"location_id": self.loc_zone2_bin1.id, "quantity": 10.0},
            ],
        )
        self.assertEqual(move.state, "assigned")

    def test_rule_packaging(self):
        self._setup_packagings(
            self.product1,
            [("Pallet", 500, self.pallet), ("Retail Box", 50, self.retail_box)],
        )
        self._update_qty_in_location(self.loc_zone1_bin1, self.product1, 40)
        self._update_qty_in_location(self.loc_zone1_bin2, self.product1, 510)
        self._update_qty_in_location(self.loc_zone2_bin1, self.product1, 60)
        self._update_qty_in_location(self.loc_zone3_bin1, self.product1, 100)
        picking = self._create_picking(self.wh, [(self.product1, 590)])

        self._create_rule(
            {},
            [
                # due to this rule and the packaging size of 500, we will
                # not use zone1/bin1, but zone1/bin2 will be used.
                {
                    "location_id": self.loc_zone1.id,
                    "sequence": 1,
                    "removal_strategy": "packaging",
                },
                # zone2/bin2 will match the second packaging size of 50
                {
                    "location_id": self.loc_zone2.id,
                    "sequence": 2,
                    "removal_strategy": "packaging",
                },
                # the rest should be taken here
                {"location_id": self.loc_zone3.id, "sequence": 3},
            ],
        )
        picking.action_assign()
        move = picking.move_ids
        ml = move.move_line_ids
        self.assertRecordValues(
            ml,
            [
                {"location_id": self.loc_zone1_bin2.id, "quantity": 500.0},
                {"location_id": self.loc_zone2_bin1.id, "quantity": 50.0},
                {"location_id": self.loc_zone3_bin1.id, "quantity": 40.0},
            ],
        )
        self.assertEqual(move.state, "assigned")

    def test_rule_packaging_fifo(self):
        self._setup_packagings(
            self.product1,
            [("Pallet", 500, self.pallet), ("Retail Box", 50, self.retail_box)],
        )
        self._update_qty_in_location(
            self.loc_zone1_bin1,
            self.product1,
            500,
            in_date=fields.Datetime.to_datetime("2021-01-04 12:00:00"),
        )
        self._update_qty_in_location(
            self.loc_zone1_bin2,
            self.product1,
            500,
            in_date=fields.Datetime.to_datetime("2021-01-02 12:00:00"),
        )
        self._create_rule(
            {},
            [
                {
                    "location_id": self.loc_zone1.id,
                    "sequence": 1,
                    "removal_strategy": "packaging",
                },
            ],
        )

        # take in bin2 to respect fifo
        picking = self._create_picking(self.wh, [(self.product1, 50)])
        picking.action_assign()
        self.assertRecordValues(
            picking.move_ids.move_line_ids,
            [{"location_id": self.loc_zone1_bin2.id, "quantity": 50.0}],
        )
        picking2 = self._create_picking(self.wh, [(self.product1, 50)])
        picking2.action_assign()
        self.assertRecordValues(
            picking2.move_ids.move_line_ids,
            [{"location_id": self.loc_zone1_bin2.id, "quantity": 50.0}],
        )

    def test_rule_packaging_fifo_pack(self):
        self._setup_packagings(
            self.product1,
            [("Pallet", 500, self.pallet), ("Retail Box", 100, self.retail_box)],
        )
        pack_1, pack_2 = self.env["stock.quant.package"].create(
            [{"name": "PACK0001"}, {"name": "PACK0002"}]
        )
        self._update_qty_in_location(
            self.loc_zone1_bin1,
            self.product1,
            100,
            in_date=fields.Datetime.to_datetime("2021-01-02 12:00:00"),
            package=pack_1,
        )
        self._update_qty_in_location(
            self.loc_zone1_bin2,
            self.product1,
            500,
            in_date=fields.Datetime.to_datetime("2021-01-04 12:00:00"),
            package=pack_2,
        )
        self._create_rule(
            {},
            [
                {
                    "location_id": self.loc_zone1.id,
                    "sequence": 1,
                    "removal_strategy": "packaging",
                },
            ],
        )

        picking = self._create_picking(self.wh, [(self.product1, 500)])
        # Pick from biggest packaging
        picking.action_assign()
        self.assertRecordValues(
            picking.move_ids.move_line_ids,
            [
                {
                    "location_id": self.loc_zone1_bin2.id,
                    "quantity": 500.0,
                    "package_id": pack_2.id,
                }
            ],
        )

    def test_rule_packaging_0_packaging(self):
        # a packaging mistakenly created with a 0 qty should be ignored,
        # not make the reservation fail
        self._setup_packagings(
            self.product1,
            [
                ("Pallet", 500, self.pallet),
                ("Retail Box", 50, self.retail_box),
                ("DivisionByZero", 0, self.unit),
            ],
        )
        self._update_qty_in_location(self.loc_zone1_bin1, self.product1, 40)
        picking = self._create_picking(self.wh, [(self.product1, 590)])
        self._create_rule(
            {},
            [
                {
                    "location_id": self.loc_zone1.id,
                    "sequence": 1,
                    "removal_strategy": "packaging",
                }
            ],
        )
        # Here, it will try to reserve a pallet of 500, then an outer box of
        # 50, then should ignore the one with 0 not to fail because of division
        # by zero
        picking.action_assign()

    def test_rule_packaging_level(self):
        # only take one kind of packaging
        self._setup_packagings(
            self.product1,
            [
                ("Pallet", 500, self.pallet),
                ("Transport Box", 50, self.transport_box),
                ("Retail Box", 10, self.retail_box),
                ("Unit", 1, self.unit),
            ],
        )
        self._update_qty_in_location(self.loc_zone1_bin1, self.product1, 40)
        self._update_qty_in_location(self.loc_zone1_bin2, self.product1, 600)
        self._update_qty_in_location(self.loc_zone2_bin1, self.product1, 30)
        self._update_qty_in_location(self.loc_zone2_bin2, self.product1, 500)
        self._update_qty_in_location(self.loc_zone3_bin1, self.product1, 500)
        picking = self._create_picking(self.wh, [(self.product1, 560)])

        self._create_rule(
            {},
            [
                # we'll take one pallet (500) from zone1/bin2, but as we filter
                # on pallets only, we won't take the 600 out of it (if the rule
                # had no type, we would have taken 100 of transport boxes).
                {
                    "location_id": self.loc_zone1.id,
                    "sequence": 1,
                    "removal_strategy": "packaging",
                    "packaging_level_ids": [(6, 0, self.pallet.ids)],
                },
                # zone2/bin2 will match the second packaging size of 50,
                # but won't take 60 because it doesn't take retail boxes
                {
                    "location_id": self.loc_zone2.id,
                    "sequence": 2,
                    "removal_strategy": "packaging",
                    "packaging_level_ids": [(6, 0, self.transport_box.ids)],
                },
                # the rest should be taken here
                {"location_id": self.loc_zone3.id, "sequence": 3},
            ],
        )
        picking.action_assign()
        move = picking.move_ids
        ml = move.move_line_ids
        self.assertRecordValues(
            ml,
            [
                {"location_id": self.loc_zone1_bin2.id, "quantity": 500.0},
                {"location_id": self.loc_zone2_bin2.id, "quantity": 50.0},
                {"location_id": self.loc_zone3_bin1.id, "quantity": 10.0},
            ],
        )
        self.assertEqual(move.state, "assigned")

    def test_rule_excluded_not_child_location(self):
        self._update_qty_in_location(self.loc_zone1_bin1, self.product1, 100)
        self._update_qty_in_location(self.loc_zone1_bin2, self.product1, 100)
        self._update_qty_in_location(self.loc_zone2_bin1, self.product1, 100)
        picking = self._create_picking(self.wh, [(self.product1, 80)])

        self._create_rule(
            {},
            [
                {"location_id": self.loc_zone1.id, "sequence": 1},
                {"location_id": self.loc_zone2.id, "sequence": 2},
            ],
        )
        move = picking.move_ids

        move.location_id = self.loc_zone2
        picking.action_assign()
        ml = move.move_line_ids

        # As the source location of the stock.move is loc_zone2, we should
        # never take any quantity in zone1.

        self.assertRecordValues(
            ml, [{"location_id": self.loc_zone2_bin1.id, "quantity": 80.0}]
        )
        self.assertEqual(move.state, "assigned")

    def test_several_rules_same_loc_negative(self):
        """
        We have several rules for the same location
        We have two quants in the location with one negative

        """

        self.env["stock.quant"].create(
            {
                "location_id": self.loc_zone1_bin1.id,
                "quantity": 10.0,
                "product_id": self.product1.id,
            }
        )
        self.env["stock.quant"].create(
            {
                "location_id": self.loc_zone1_bin1.id,
                "quantity": -2.0,
                "product_id": self.product1.id,
            }
        )

        picking = self._create_picking(self.wh, [(self.product1, 1.0)])
        self._create_rule(
            {},
            [
                {
                    "location_id": self.loc_zone1_bin1.id,
                    "removal_strategy": "packaging",
                    "sequence": 1,
                },
                {"location_id": self.loc_zone1_bin1.id, "sequence": 2},
            ],
        )
        picking.action_assign()

    def test_move_reassign_partial(self):
        self._create_rule(
            {"force_reassign_partial": True},
            [{"removal_strategy": "default", "location_id": self.wh.lot_stock_id.id}],
        )
        self.product1.tracking = "lot"
        lot_1 = self.env["stock.lot"].create(
            {
                "name": "LOT-0001",
                "product_id": self.product1.id,
            }
        )
        lot_2 = self.env["stock.lot"].create(
            {
                "name": "LOT-0002",
                "product_id": self.product1.id,
            }
        )
        self.env["stock.quant"]._update_available_quantity(
            self.product1, self.wh.lot_stock_id, 10, lot_id=lot_1
        )
        self.env["stock.quant"]._update_available_quantity(
            self.product1, self.wh.lot_stock_id, 5, lot_id=lot_2
        )
        picking_1 = self._create_picking(self.wh, [(self.product1, 10)])
        picking_2 = self._create_picking(self.wh, [(self.product1, 10)])
        picking_1.action_assign()
        self.assertEqual(picking_1.move_ids.state, "assigned")
        self.assertEqual(picking_1.move_line_ids.lot_id, lot_1)

        picking_2.action_assign()
        self.assertEqual(picking_2.move_ids.state, "partially_available")
        self.assertEqual(picking_2.move_line_ids.lot_id, lot_2)

        picking_1.action_cancel()

        self.env["stock.quant"]._update_available_quantity(
            self.product1, self.wh.lot_stock_id, 10, lot_id=lot_2
        )

        picking_2.action_assign()
        self.assertEqual(picking_2.move_line_ids.lot_id, lot_1)
