# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _synchronize_quant(
        self, quantity, location, action="available", in_date=False, **quants_value
    ):
        # a negative quantity takes goods out of `location`, a positive one
        # puts goods in it
        put_down = action == "available" and quantity > 0
        if put_down:
            # super() creates the quant when `location` holds none yet, and
            # afterwards nothing tells that quant from an older one
            previous_dates = self._get_line_quants(location, **quants_value).mapped(
                "zone_in_date"
            )
        res = super()._synchronize_quant(
            quantity, location, action=action, in_date=in_date, **quants_value
        )
        if not put_down:
            return res

        same_zone = location._is_same_zone(
            self.location_id._get_zone_location(), location._get_zone_location()
        )
        if same_zone:
            zone_in_date = self._source_zone_in_date()
        else:
            # the move date would be more accurate, but stock.move.line.date
            # only gets it once _action_done has gone through every line.
            # This is the simplest, good enough, approach.
            zone_in_date = fields.Datetime.now()
        if zone_in_date:
            # oldest wins, same as for in_date
            zone_in_date = min([zone_in_date] + previous_dates)
            self._get_line_quants(location, **quants_value).zone_in_date = zone_in_date
        return res

    def _source_zone_in_date(self):
        """Zone entry date of the quant the goods were taken from. Still
        readable here: emptied quants are dropped at the end of _action_done."""
        self.ensure_one()
        dates = self._get_line_quants(
            self.location_id, lot=self.lot_id, package=self.package_id
        ).mapped("zone_in_date")
        return min(dates) if dates else False

    def _get_line_quants(self, location, **quants_value):
        """Quants of ``location`` holding the goods this line moves."""
        self.ensure_one()
        # Used twice below, unlike package and owner.
        lot = quants_value.get("lot", self.lot_id)
        quants = (
            self.env["stock.quant"]
            .sudo()
            ._gather(
                self.product_id,
                location,
                lot_id=lot,
                package_id=quants_value.get("package", self.package_id),
                owner_id=quants_value.get("owner", self.owner_id),
                strict=True,
            )
        )
        if lot:
            # _gather also returns the untracked quant of the location, which
            # holds other goods than the ones this line moves.
            quants = quants.filtered(lambda quant: quant.lot_id)
        return quants
