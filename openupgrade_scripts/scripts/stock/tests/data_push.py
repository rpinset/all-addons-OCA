env = locals().get("env")
# create two step push route, move a product there
intermediate_location = env["stock.location"].create(
    {
        "name": "Intermediate location",
        "usage": "internal",
    }
)
env["ir.model.data"]._update_xmlids(
    [
        {
            "xml_id": "openupgrade_test_stock.intermediate_push_location",
            "record": intermediate_location,
        }
    ]
)
two_step_route = env["stock.route"].create(
    {
        "name": "2 steps",
        "rule_ids": [
            (
                0,
                0,
                {
                    "name": "Stock → Intermediate",
                    "location_src_id": env.ref("stock.stock_location_stock").id,
                    "location_dest_id": intermediate_location.id,
                    "picking_type_id": env.ref("stock.picking_type_internal").id,
                    "action": "push",
                },
            ),
            (
                0,
                0,
                {
                    "name": "Intermediate → Customer",
                    "location_src_id": intermediate_location.id,
                    "location_dest_id": env.ref("stock.stock_location_customers").id,
                    "picking_type_id": env.ref("stock.picking_type_out").id,
                    "action": "push",
                },
            ),
        ],
    }
)
product = env["product.product"].create(
    {
        "name": "2 step product (push)",
        "type": "product",
        #    'type': 'consu', # v18
        "route_ids": [(6, 0, two_step_route.ids)],
    }
)
env["ir.model.data"]._update_xmlids(
    [{"xml_id": "openupgrade_test_stock.push_product", "record": product}]
)
in_move = env["stock.move"].create(
    {
        "name": "in",
        "location_id": env.ref("stock.stock_location_suppliers").id,
        "location_dest_id": env.ref("stock.stock_location_stock").id,
        #    'location_final_id': env.ref('stock.stock_location_customers').id,
        "route_ids": [(6, 0, two_step_route.ids)],
        "product_id": product.id,
        "quantity": 42,
        "product_uom_qty": 42,
        "picked": True,
    }
)
in_move._action_done()
in_move.move_dest_ids._action_done()
env.cr.commit()
