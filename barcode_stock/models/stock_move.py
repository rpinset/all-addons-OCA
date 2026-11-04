# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero


class StockMove(models.Model):
    _inherit = "stock.move"

    qty_done_total = fields.Float(
        compute="_compute_qty_progress",
        string="Done",
        store=False,
    )
    qty_remaining = fields.Float(
        compute="_compute_qty_progress",
        string="Remaining Quantity",
        store=False,
    )
    is_fully_picked = fields.Boolean(
        compute="_compute_qty_progress",
        string="Fully Picked",
        store=False,
    )

    def _reset_qty_progress(self):
        for move in self:
            move.qty_done_total = 0
            move.qty_remaining = 0
            move.is_fully_picked = False

    @api.depends("move_line_ids.qty_picked", "picking_id.state")
    def _compute_qty_progress(self):
        if self.env.context.get("install_mode"):
            self._reset_qty_progress()
            return
        ready_moves = self.filtered(lambda m: m.picking_id.state == "assigned")
        if not ready_moves:
            self._reset_qty_progress()
            return
        data = self.env["stock.move.line"]._read_group(
            [("move_id", "in", ready_moves.ids)],
            ["move_id"],
            ["qty_picked:sum"],
        )
        sums = {move.id: qty_picked for move, qty_picked in data}
        for move in self:
            done = sums.get(move.id, 0.0)
            move.qty_done_total = done
            move.qty_remaining = move.product_uom_qty - done
            move.is_fully_picked = move.qty_remaining <= 0

    def barcode_pick_lot(
        self, lot_id, quantity, location_id=False, location_dest_id=False
    ):
        """Pick a lot the move's reservation does not carry, the way Odoo
        reserves stock rather than by rewriting another lot's line. As much of
        the other lots' reservation as the lot replaces is released first. The
        lot is then taken from its own quants under the move's source (or the
        one the operator chose), in the order of the removal strategy: stock
        nothing holds first, then stock other moves hold, whose reservation
        Odoo frees on validation. Each quant gives a line, with its shelf,
        package and owner, marked picked and sent to the destination the
        operator chose, if any.

        Picking more than the lot holds there is allowed, as Odoo allows it:
        what is over goes on the last line, and validating leaves a negative
        quant that shows the gap. With no stock at all, the lot is only picked
        from a source the operator chose.
        """
        self.ensure_one()
        lot = self.env["stock.lot"].browse(lot_id)
        source = (
            self.env["stock.location"].browse(location_id)
            if location_id
            else self.location_id
        )
        self._barcode_release_other_lots(lot, quantity)
        takes = self._barcode_lot_takes(lot, quantity, source)
        vals_list = [
            self._prepare_move_line_vals(quantity=taken, reserved_quant=quant)
            for quant, taken in takes.items()
        ]
        if not vals_list:
            vals_list = [
                self._barcode_chosen_source_vals(lot, quantity, source, location_id)
            ]
        if location_dest_id:
            for vals in vals_list:
                vals["location_dest_id"] = location_dest_id
        lines = self.env["stock.move.line"].create(vals_list)
        uom = self.product_id.uom_id
        over = quantity - sum(takes.values()) if takes else 0
        for line in lines:
            extra = over if line == lines[-1] else 0
            line.qty_picked = line.quantity + uom._compute_quantity(
                extra, line.product_uom_id
            )
        self._recompute_state()
        return True

    def _barcode_release_other_lots(self, lot, quantity):
        """Release, from the other lots' lines, what the move would hold over
        its demand once ``quantity`` of ``lot`` is taken: from the lines
        nothing was picked on first, the last ones first, then what partly
        picked lines hold beyond what was picked on them."""
        uom = self.product_id.uom_id
        excess = (
            sum(self.move_line_ids.mapped("quantity_product_uom"))
            + quantity
            - self.product_qty
        )
        others = self.move_line_ids.filtered(lambda line: line.lot_id != lot)
        untouched = others.filtered(lambda line: not line.picked).sorted(
            "id", reverse=True
        )
        started = (others - untouched).sorted("id", reverse=True)
        for line in untouched + started:
            if float_compare(excess, 0, precision_rounding=uom.rounding) <= 0:
                break
            held = line.quantity_product_uom
            picked = line.product_uom_id._compute_quantity(line.qty_picked, uom)
            release = min(held - picked, excess)
            if float_compare(release, 0, precision_rounding=uom.rounding) <= 0:
                continue
            excess -= release
            if float_is_zero(held - release, precision_rounding=uom.rounding):
                line.unlink()
            else:
                line.quantity = uom._compute_quantity(
                    held - release, line.product_uom_id
                )

    def _barcode_lot_takes(self, lot, quantity, source):
        """How much to take from each quant of the lot under the source, in the
        order of the removal strategy: stock nothing holds first, out of the
        packages the strategy picks for the quantity (least packages) and then
        the rest, then stock other moves hold. Quants without a lot, which
        Odoo's own reservation of a lot may also take, are left alone.

        :return: the quantity taken, by quant
        """
        rounding = self.product_id.uom_id.rounding

        def lot_quants(qty=0):
            quants = self.env["stock.quant"]._gather(
                self.product_id, source, lot_id=lot, qty=qty
            )
            return quants.filtered(
                lambda quant: quant.lot_id == lot
                and float_compare(quant.quantity, 0, precision_rounding=rounding) > 0
            )

        def free(quant):
            return quant.quantity - quant.reserved_quantity - takes[quant]

        quants = lot_quants()
        takes = dict.fromkeys(quants, 0.0)
        rest = quantity
        # Given the quantity, least packages narrows the quants to the packages
        # it picks out of the free stock, so the free stock elsewhere and the
        # stock other moves hold are gathered without it.
        for group, room in (
            (lot_quants(quantity), free),
            (quants, free),
            (quants, lambda quant: quant.quantity - takes[quant]),
        ):
            for quant in group:
                take = min(rest, room(quant))
                if float_compare(take, 0, precision_rounding=rounding) > 0:
                    takes[quant] += take
                    rest -= take
        return {
            quant: taken
            for quant, taken in takes.items()
            if float_compare(taken, 0, precision_rounding=rounding) > 0
        }

    def _barcode_chosen_source_vals(self, lot, quantity, source, chosen):
        """A line for a lot with no stock under the source: only from a source
        the operator chose."""
        if not chosen:
            raise UserError(
                _(
                    "Lot %(lot)s has no stock in %(location)s.",
                    lot=lot.name,
                    location=source.display_name,
                )
            )
        vals = self._prepare_move_line_vals(quantity=quantity)
        vals.update(lot_id=lot.id, location_id=source.id)
        return vals
