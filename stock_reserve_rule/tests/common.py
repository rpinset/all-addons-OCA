# Copyright 2019 Camptocamp (https://www.camptocamp.com)
# Copyright 2019-2021 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
from odoo.addons.base.tests.common import BaseCommon


class ReserveRuleCommon(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_delta = cls.env.ref("base.res_partner_4")
        cls.wh = cls.env["stock.warehouse"].create(
            {
                "name": "Base Warehouse",
                "reception_steps": "one_step",
                "delivery_steps": "pick_ship",
                "code": "WHTEST",
            }
        )

        cls.customer_loc = cls.env.ref("stock.stock_location_customers")

        cls.loc_zone1 = cls.env["stock.location"].create(
            {"name": "Zone1", "location_id": cls.wh.lot_stock_id.id}
        )
        cls.loc_zone1_bin1 = cls.env["stock.location"].create(
            {"name": "Zone1 Bin1", "location_id": cls.loc_zone1.id}
        )
        cls.loc_zone1_bin2 = cls.env["stock.location"].create(
            {"name": "Zone1 Bin2", "location_id": cls.loc_zone1.id}
        )
        cls.loc_zone2 = cls.env["stock.location"].create(
            {"name": "Zone2", "location_id": cls.wh.lot_stock_id.id}
        )
        cls.loc_zone2_bin1 = cls.env["stock.location"].create(
            {"name": "Zone2 Bin1", "location_id": cls.loc_zone2.id}
        )
        cls.loc_zone2_bin2 = cls.env["stock.location"].create(
            {"name": "Zone2 Bin2", "location_id": cls.loc_zone2.id}
        )
        cls.loc_zone3 = cls.env["stock.location"].create(
            {"name": "Zone3", "location_id": cls.wh.lot_stock_id.id}
        )
        cls.loc_zone3_bin1 = cls.env["stock.location"].create(
            {"name": "Zone3 Bin1", "location_id": cls.loc_zone3.id}
        )
        cls.loc_zone3_bin2 = cls.env["stock.location"].create(
            {"name": "Zone3 Bin2", "location_id": cls.loc_zone3.id}
        )

        cls.product1 = cls.env["product.product"].create(
            {"name": "Product 1", "type": "consu", "is_storable": True}
        )
        cls.product2 = cls.env["product.product"].create(
            {"name": "Product 2", "type": "consu", "is_storable": True}
        )

        cls.unit = cls.env["product.packaging.level"].create(
            {"name": "Unit", "code": "UNIT", "sequence": 0}
        )
        cls.retail_box = cls.env["product.packaging.level"].create(
            {"name": "Retail Box", "code": "RET", "sequence": 3}
        )
        cls.transport_box = cls.env["product.packaging.level"].create(
            {"name": "Transport Box", "code": "BOX", "sequence": 4}
        )
        cls.pallet = cls.env["product.packaging.level"].create(
            {"name": "Pallet", "code": "PAL", "sequence": 5}
        )

    def _create_picking(self, wh, products=None, location_src_id=None):
        """Create picking

        Products must be a list of tuples (product, quantity).
        One stock move will be created for each tuple.
        """
        if products is None:
            products = []

        picking = self.env["stock.picking"].create(
            {
                "location_id": location_src_id or wh.lot_stock_id.id,
                "location_dest_id": wh.wh_output_stock_loc_id.id,
                "partner_id": self.partner_delta.id,
                "picking_type_id": wh.pick_type_id.id,
            }
        )

        for product, qty in products:
            self.env["stock.move"].create(
                {
                    "name": product.name,
                    "product_id": product.id,
                    "product_uom_qty": qty,
                    "product_uom": product.uom_id.id,
                    "picking_id": picking.id,
                    "location_id": location_src_id or wh.lot_stock_id.id,
                    "location_dest_id": wh.wh_output_stock_loc_id.id,
                    "state": "confirmed",
                }
            )
        return picking

    def _update_qty_in_location(self, location, product, quantity, in_date=None):
        self.env["stock.quant"]._update_available_quantity(
            product, location, quantity, in_date=in_date
        )

    def _create_rule(self, rule_values, removal_values):
        rule_config = {
            "name": "Test Rule",
            "location_id": self.wh.lot_stock_id.id,
            "rule_removal_ids": [(0, 0, values) for values in removal_values],
        }
        rule_config.update(rule_values)
        self.env["stock.reserve.rule"].create(rule_config)
        # workaround for https://github.com/odoo/odoo/pull/41900
        self.env["stock.reserve.rule"].invalidate_model()

    def _setup_packagings(self, product, packagings):
        """Create packagings on a product
        packagings is a list [(name, qty, packaging_type)]
        """
        self.env["product.packaging"].create(
            [
                {
                    "name": name,
                    "qty": qty if qty else 1,
                    "product_id": product.id,
                    "packaging_level_id": packaging_level.id,
                }
                for name, qty, packaging_level in packagings
            ]
        )
