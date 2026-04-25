env = locals().get("env")
# create two step pull route, procure a product with it
intermediate_location = env["stock.location"].create(
    {
        "name": "Intermediate location",
        "usage": "internal",
    }
)
env["ir.model.data"]._update_xmlids(
    [
        {
            "xml_id": "openupgrade_test_stock.intermediate_pull_location",
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
                    "action": "pull",
                    #            'location_dest_from_rule': True, # v18
                },
            ),
            (
                0,
                0,
                {
                    "name": "Intermediate → Customer",
                    "location_src_id": intermediate_location.id,
                    "location_dest_id": env.ref("stock.stock_location_customers").id,
                    "picking_type_id": env.ref("stock.picking_type_internal").id,
                    "procure_method": "make_to_order",
                    "action": "pull",
                    #            'location_dest_from_rule': True, # v18
                },
            ),
        ],
    }
)
product = env["product.product"].create(
    {
        "name": "2 step product (pull)",
        "type": "product",
        #    'type': 'consu', # v18
        "route_ids": [(6, 0, two_step_route.ids)],
    }
)
env["ir.model.data"]._update_xmlids(
    [{"xml_id": "openupgrade_test_stock.pull_product", "record": product}]
)
procurement_group = env["procurement.group"].create(
    {
        "name": "2 step procurement",
    }
)
env["procurement.group"].run(
    [
        env["procurement.group"].Procurement(
            product_id=product,
            product_qty=42,
            product_uom=product.uom_id,
            location_id=env.ref("stock.stock_location_customers"),
            name="2 step procurement",
            origin="/",
            company_id=env.company,
            values={"group_id": procurement_group},
        ),
    ]
)
env.cr.commit()
