# Copyright 2019-22 ForgeFlow S.L. (http://www.forgeflow.com)
# - Lois Rilo <lois.rilo@forgeflow.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import logging
from datetime import timedelta

from odoo import api, fields, models
from odoo.tools.float_utils import float_round

logger = logging.getLogger(__name__)


class MultiLevelMrp(models.TransientModel):
    _inherit = "mrp.multi.level"

    @api.model
    def _prepare_mrp_move_data_from_estimate(self, estimate, product_mrp_area, date):
        mrp_type = "d"
        origin = "fc"
        daily_qty_unrounded = estimate.daily_qty
        daily_qty = float_round(
            estimate.daily_qty,
            precision_rounding=product_mrp_area.product_id.uom_id.rounding,
            rounding_method="HALF-UP",
        )
        days_consumed = 0
        if product_mrp_area.group_estimate_days > 1:
            start = estimate.date_from
            if start < date:
                days_consumed = (date - start).days
        group_estimate_days = min(
            product_mrp_area.group_estimate_days, estimate.duration - days_consumed
        )
        mrp_qty = float_round(
            daily_qty_unrounded * group_estimate_days,
            precision_rounding=product_mrp_area.product_id.uom_id.rounding,
            rounding_method="HALF-UP",
        )
        return {
            "mrp_area_id": product_mrp_area.mrp_area_id.id,
            "product_id": product_mrp_area.product_id.id,
            "product_mrp_area_id": product_mrp_area.id,
            "production_id": None,
            "purchase_order_id": None,
            "purchase_line_id": None,
            "stock_move_id": None,
            "mrp_qty": -mrp_qty,
            "current_qty": -daily_qty,
            "mrp_date": date,
            "current_date": date,
            "mrp_type": mrp_type,
            "mrp_origin": origin,
            "mrp_order_number": None,
            "parent_product_id": None,
            "name": "Forecast",
            "state": "confirmed",
        }

    @api.model
    def _estimates_domain(self, product_mrp_area):
        locations = product_mrp_area.mrp_area_id._get_locations()
        return [
            ("product_id", "=", product_mrp_area.product_id.id),
            ("location_id", "child_of", locations.ids),
            ("date_to", ">=", fields.Date.today()),
        ]

    @api.model
    def _init_mrp_move_from_forecast(self, product_mrp_area):
        res = super()._init_mrp_move_from_forecast(product_mrp_area)
        if not product_mrp_area.group_estimate_days:
            return False
        today = fields.Date.today()
        domain = self._estimates_domain(product_mrp_area)
        estimates = self.env["stock.demand.estimate"].search(domain)
        for rec in estimates:
            start = rec.date_from
            if start < today:
                start = today
            mrp_date = fields.Date.from_string(start)
            date_end = fields.Date.from_string(rec.date_to)
            delta = timedelta(days=product_mrp_area.group_estimate_days)
            while mrp_date <= date_end:
                mrp_move_data = self._prepare_mrp_move_data_from_estimate(
                    rec, product_mrp_area, mrp_date
                )
                self.env["mrp.move"].create(mrp_move_data)
                mrp_date += delta
        return res

    def _exclude_considering_estimate_demand_and_other_sources_strat(
        self, product_mrp_area, mrp_date
    ):
        estimate_strat = (
            product_mrp_area.mrp_area_id.estimate_demand_and_other_sources_strat
        )
        if estimate_strat == "all":
            return False

        domain = self._estimates_domain(product_mrp_area)
        estimates = self.env["stock.demand.estimate"].search(domain)
        if not estimates:
            return False

        if estimate_strat == "ignore_others_if_estimates":
            # Ignore
            return True
        if estimate_strat == "ignore_overlapping":
            for estimate in estimates:
                if mrp_date >= estimate.date_from and mrp_date <= estimate.date_to:
                    # Ignore
                    return True
        return False

    @api.model
    def _prepare_mrp_move_data_from_stock_move(
        self, product_mrp_area, move, direction="in"
    ):
        res = super()._prepare_mrp_move_data_from_stock_move(
            product_mrp_area, move, direction=direction
        )
        if direction == "out":
            mrp_date = res.get("mrp_date")
            if (
                self._exclude_considering_estimate_demand_and_other_sources_strat(
                    product_mrp_area, mrp_date
                )
                and not res["production_id"]
            ):
                return False
        return res
