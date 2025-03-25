# Copyright 2022 Michael Tietz (MT Software) <mtietz@mt-software.de>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo.tests import TransactionCase


class TestStockRouteGetSourceLocation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.wh = cls.env.ref("stock.warehouse0")
        cls.stock_loc = cls.wh.lot_stock_id
        cls.view_loc = cls.stock_loc.location_id
        cls.customer_loc = cls.env.ref("stock.stock_location_customers")
        cls.location4, cls.operation_type4, cls.route4 = cls.create_type_route_and_rule(
            "4", cls.customer_loc
        )
        cls.location3, cls.operation_type3, cls.route3 = cls.create_type_route_and_rule(
            "3", cls.location4
        )
        cls.location2, cls.operation_type2, cls.route2 = cls.create_type_route_and_rule(
            "2", cls.location3
        )
        cls.location1, cls.operation_type1, cls.route1 = cls.create_type_route_and_rule(
            "1",
            cls.location2,
        )
        _, cls.operation_type_pick, cls.route_pick = cls.create_type_route_and_rule(
            "pick", cls.location1, "make_to_stock", location_src=cls.stock_loc
        )

    @classmethod
    def create_type_route_and_rule(
        cls, suffix, location_dest, procure_method="make_to_order", location_src=None
    ):
        location_src = location_src or cls.stock_loc.create(
            {"name": f"location{suffix}", "location_id": cls.view_loc.id}
        )
        operation_type_name = f"operationtype{suffix}"
        operation_type = cls.env["stock.picking.type"].create(
            {
                "name": operation_type_name,
                "sequence_code": operation_type_name,
                "code": "internal",
                "default_location_src_id": location_src.id,
                "default_location_dest_id": location_dest.id,
            }
        )
        route_name = f"route{suffix}"
        rule_name = f"{route_name} rule{suffix}"
        route = cls.env["stock.route"].create(
            {
                "name": route_name,
                "warehouse_ids": [(6, 0, cls.wh.ids)],
                "rule_ids": [
                    (
                        0,
                        0,
                        {
                            "name": rule_name,
                            "location_src_id": location_src.id,
                            "location_dest_id": location_dest.id,
                            "picking_type_id": operation_type.id,
                            "procure_method": procure_method,
                        },
                    )
                ],
            }
        )
        return location_src, operation_type, route

    def test_get_source_location(self):
        source_location = self.route4._get_source_location(self.location4)
        self.assertEqual(source_location, self.stock_loc)

        source_location = self.route3._get_source_location(self.location3)
        self.assertEqual(source_location, self.stock_loc)

        source_location = self.route2._get_source_location(self.location2)
        self.assertEqual(source_location, self.stock_loc)

        source_location = self.route1._get_source_location(self.location1)
        self.assertEqual(source_location, self.stock_loc)

        # Location is not in route but a valid route is found
        # and will return stock location
        source_location = self.route1._get_source_location(self.location4)
        self.assertEqual(source_location, self.stock_loc)

        # Changing the procure_method on rule2
        self.route2.rule_ids.procure_method = "make_to_stock"
        source_location = self.route4._get_source_location(self.location4)
        self.assertEqual(source_location, self.location2)
