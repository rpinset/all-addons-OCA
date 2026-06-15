# Copyright 2025 Tecnativa - Carlos Lopez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import config


class RouteArea(models.Model):
    _inherit = "route.area"

    warehouse_id = fields.Many2one(
        "stock.warehouse",
        copy=False,
        domain="[('company_id', '=', company_id)]",
        default=lambda self: self.env["stock.warehouse"].search(
            [("company_id", "=", self.env.company.id)], limit=1
        ),
    )
    location_id = fields.Many2one(
        "stock.location", copy=False, readonly=True, ondelete="restrict"
    )

    @api.model_create_multi
    def create(self, vals_list):
        areas = super().create(vals_list)
        test_condition = not config["test_enable"] or (
            config["test_enable"]
            and self.env.context.get("test_route_planning_require_warehouse", False)
        )
        if not test_condition:
            return areas
        areas_without_warehouse = areas.filtered(lambda r: not r.warehouse_id)
        if areas_without_warehouse:
            raise UserError(
                self.env._("You must set a warehouse for the Route Areas created.")
            )
        for area in areas:
            area._create_or_update_stock_records()
        return areas

    def write(self, vals):
        res = super().write(vals)
        if "warehouse_id" in vals or "name" in vals or "code" in vals:
            for area in self.filtered("warehouse_id"):
                area._create_or_update_stock_records()
        return res

    def _create_or_update_stock_records(self):
        self.ensure_one()
        self._create_or_update_location()
        self._create_or_update_rule()

    def _create_or_update_location(self):
        Location = self.env["stock.location"].sudo()
        location_values = self._prepare_location_values()
        if not self.location_id:
            self.location_id = Location.create(location_values)
        else:
            self.location_id.write(location_values)

    def _create_or_update_rule(self):
        warehouse = self.warehouse_id
        customer_loc, _supplier_loc = warehouse._get_partner_locations()
        routing_out1 = warehouse.Routing(
            warehouse.lot_stock_id, self.location_id, warehouse.out_type_id, "pull"
        )
        routing_out2 = warehouse.Routing(
            self.location_id, customer_loc, warehouse.out_type_id, "push"
        )
        rule_vals = [
            warehouse._prepare_stock_rule_values(
                warehouse.delivery_route_id, routing_out1, "make_to_stock", True
            ),
            warehouse._prepare_stock_rule_values(
                warehouse.delivery_route_id, routing_out2, "make_to_order", False
            ),
        ]
        warehouse._find_or_create_custom_rule(rule_vals)

    def _prepare_location_values(self):
        code = self.warehouse_id.code.replace(" ", "").upper()
        company = self.warehouse_id.company_id
        return {
            "name": self.name,
            "usage": "transit",
            "location_id": self.warehouse_id.view_location_id.id,
            "company_id": company.id,
            "barcode": self.warehouse_id._valid_barcode(code + self.code, company.id),
        }
