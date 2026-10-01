# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def _barcode_scanner_get_internal_picking_type(
        self, origin_location, destination_location
    ):
        picking_type_model = self.env["stock.picking.type"]
        warehouse = origin_location.warehouse_id or destination_location.warehouse_id
        # The warehouse's own internal operation type is the canonical target,
        # returned even when archived (a single-step warehouse keeps it inactive).
        if warehouse and warehouse.int_type_id:
            return warehouse.int_type_id
        # Fall back to any internal type for this company (or a company-shared
        # one), archived types included so a valid setup is never overlooked.
        picking_type = picking_type_model.with_context(active_test=False).search(
            [
                ("code", "=", "internal"),
                ("company_id", "in", [self.env.company.id, False]),
            ],
            order="warehouse_id, id",
            limit=1,
        )
        if not picking_type:
            # A warehouse operation is not the place to create configuration:
            # the internal operation type must be set up beforehand.
            raise UserError(
                _(
                    "No internal transfer operation type is configured. "
                    "Please set one up before using barcode transfers."
                )
            )
        return picking_type

    @api.model
    def _barcode_scanner_prepare_internal_transfer(
        self,
        origin_location_id,
        destination_location_id,
        responsible_id,
        lines,
    ):
        if not origin_location_id:
            raise UserError(_("Origin location is required."))
        if not destination_location_id:
            raise UserError(_("Destination location is required."))
        if not lines:
            raise UserError(_("Add at least one product to transfer."))

        origin_location = self.env["stock.location"].browse(origin_location_id).exists()
        destination_location = (
            self.env["stock.location"].browse(destination_location_id).exists()
        )
        if not origin_location or not destination_location:
            raise UserError(_("The selected locations are not valid anymore."))
        if origin_location == destination_location:
            raise UserError(_("Origin and destination locations must be different."))

        responsible = self.env["res.users"]
        if responsible_id:
            responsible = self.env["res.users"].browse(responsible_id).exists()
        prepared_lines = []
        for line in lines:
            product = (
                self.env["product.product"].browse(line.get("product_id")).exists()
            )
            if not product:
                raise UserError(_("One of the selected products no longer exists."))
            qty = float(line.get("qty") or 0)
            if qty <= 0:
                raise UserError(
                    _(
                        "Quantity must be greater than zero for product %(name)s.",
                        name=product.display_name,
                    )
                )

            lot = self.env["stock.lot"]
            lot_id = line.get("lot_id")
            if product.tracking != "none":
                if not lot_id:
                    raise UserError(
                        _(
                            "Lot/Serial Number is required for product %(name)s.",
                            name=product.display_name,
                        )
                    )
                lot = self.env["stock.lot"].browse(int(lot_id)).exists()
                if not lot or lot.product_id != product:
                    raise UserError(
                        _(
                            "The selected Lot/Serial Number is invalid for product "
                            "%(name)s.",
                            name=product.display_name,
                        )
                    )
                if product.tracking == "serial" and qty != 1:
                    raise UserError(
                        _(
                            "Product %(name)s is tracked by serial number and must be "
                            "transferred one unit at a time.",
                            name=product.display_name,
                        )
                    )

            prepared_lines.append(
                {
                    "product": product,
                    "qty": qty,
                    "lot": lot,
                }
            )

        return origin_location, destination_location, responsible, prepared_lines

    @api.model
    def _barcode_scanner_collect_internal_transfer_availability(
        self, origin_location, prepared_lines
    ):
        quant_model = self.env["stock.quant"]
        availability_lines = []
        all_available = True
        for line in prepared_lines:
            product = line["product"]
            lot = line["lot"]
            available_qty = quant_model._get_available_quantity(
                product,
                origin_location,
                lot_id=lot,
                strict=False,
            )
            is_available = (
                float_compare(
                    available_qty,
                    line["qty"],
                    precision_rounding=product.uom_id.rounding,
                )
                >= 0
            )
            all_available &= is_available
            availability_lines.append(
                {
                    "product_id": product.id,
                    "product_name": product.display_name,
                    "lot_id": lot.id if lot else False,
                    "lot_name": lot.name if lot else False,
                    "required_qty": line["qty"],
                    "available_qty": available_qty,
                    "available": is_available,
                }
            )
        return {
            "available": all_available,
            "lines": availability_lines,
        }

    @api.model
    def action_barcode_scanner_check_availability(
        self,
        origin_location_id,
        destination_location_id,
        lines,
        responsible_id=False,
    ):
        (
            origin_location,
            _destination_location,
            _responsible,
            prepared_lines,
        ) = self._barcode_scanner_prepare_internal_transfer(
            origin_location_id,
            destination_location_id,
            responsible_id,
            lines,
        )
        return self._barcode_scanner_collect_internal_transfer_availability(
            origin_location,
            prepared_lines,
        )

    @api.model
    def _barcode_scanner_allocate_from_origin(
        self, origin_location, product, lot, requested_qty
    ):
        """Allocate up to ``requested_qty`` of ``product`` (optionally ``lot``)
        against the real quants available in ``origin_location`` and its child
        locations, honouring the removal strategy.

        Returns a list of ``{"location", "lot", "qty"}`` describing where the
        stock is actually taken from. The candidate quants are row-locked to
        avoid concurrent over-allocation.
        """
        quant_model = self.env["stock.quant"]
        rounding = product.uom_id.rounding
        quants = quant_model._gather(
            product, origin_location, lot_id=lot or None, strict=False
        )
        if quants:
            self.env.cr.execute(
                "SELECT id FROM stock_quant WHERE id IN %s "
                "FOR NO KEY UPDATE SKIP LOCKED",
                [tuple(quants.ids)],
            )
            locked_ids = {row[0] for row in self.env.cr.fetchall()}
            quants = quants.filtered(lambda quant: quant.id in locked_ids)
            # `_gather` read the quantities before the rows were locked, so a
            # concurrent transaction may have moved them in between. Drop the
            # cached values and let the loop below re-read them under the lock.
            quants.invalidate_recordset(["quantity", "reserved_quantity"])

        allocations = []
        remaining = requested_qty
        for quant in quants:
            if float_compare(remaining, 0, precision_rounding=rounding) <= 0:
                break
            free = quant.quantity - quant.reserved_quantity
            if float_compare(free, 0, precision_rounding=rounding) <= 0:
                continue
            take = min(remaining, free)
            allocations.append(
                {
                    "location": quant.location_id,
                    "lot": quant.lot_id,
                    "qty": take,
                }
            )
            remaining -= take
        return allocations

    @api.model
    def action_barcode_scanner_internal_transfer(
        self,
        origin_location_id,
        destination_location_id,
        responsible_id,
        lines,
    ):
        (
            origin_location,
            destination_location,
            responsible,
            prepared_lines,
        ) = self._barcode_scanner_prepare_internal_transfer(
            origin_location_id,
            destination_location_id,
            responsible_id,
            lines,
        )

        # Build the move plan by allocating each line against the stock actually
        # on hand in the origin location *and its children*, capped at what is
        # available. Like the back office, we transfer the available quantity
        # instead of refusing the whole operation when more was requested.
        move_plan = []
        for line_index, line in enumerate(prepared_lines):
            product = line["product"]
            rounding = product.uom_id.rounding
            allocations = self._barcode_scanner_allocate_from_origin(
                origin_location, product, line["lot"], line["qty"]
            )
            allocated = sum(alloc["qty"] for alloc in allocations)
            if float_compare(allocated, 0, precision_rounding=rounding) <= 0:
                continue
            move_plan.append(
                {
                    "line": line,
                    "line_index": line_index,
                    "allocations": allocations,
                    "qty": allocated,
                }
            )

        if not move_plan:
            raise UserError(
                _(
                    "No stock is available in the origin location for the "
                    "selected products."
                )
            )

        picking_type = self._barcode_scanner_get_internal_picking_type(
            origin_location,
            destination_location,
        )
        picking = self.create(
            {
                "picking_type_id": picking_type.id,
                "location_id": origin_location.id,
                "location_dest_id": destination_location.id,
                "move_type": "direct",
                "user_id": responsible.id if responsible else False,
                "origin": _("Barcode Scanner Internal Transfer"),
            }
        )

        move_line_model = self.env["stock.move.line"]
        move_line_vals_list = []
        for plan in move_plan:
            line = plan["line"]
            product = line["product"]
            move = self.env["stock.move"].create(
                {
                    "name": product.display_name,
                    "product_id": product.id,
                    "product_uom_qty": plan["qty"],
                    "product_uom": product.uom_id.id,
                    "picking_id": picking.id,
                    "location_id": origin_location.id,
                    "location_dest_id": destination_location.id,
                    "company_id": picking.company_id.id,
                }
            )
            for alloc in plan["allocations"]:
                vals = {
                    "move_id": move.id,
                    "picking_id": picking.id,
                    "product_id": product.id,
                    "product_uom_id": product.uom_id.id,
                    "quantity": alloc["qty"],
                    "picked": True,
                    "location_id": alloc["location"].id,
                    "location_dest_id": destination_location.id,
                    "company_id": picking.company_id.id,
                    "lot_id": alloc["lot"].id if alloc["lot"] else False,
                    "lot_name": alloc["lot"].name if alloc["lot"] else False,
                    "qty_picked": alloc["qty"],
                }
                move_line_vals_list.append(vals)

        picking.action_confirm()
        # Our manually-allocated move lines are authoritative; drop anything the
        # confirmation may have auto-reserved so we do not double-count stock.
        picking.do_unreserve()
        move_line_model.create(move_line_vals_list)
        picking.with_context(skip_backorder=True).button_validate()

        # Report requested vs. moved per line so the UI can warn the operator
        # when only part of the requested quantity was available (allocation is
        # capped at on-hand stock, and SKIP LOCKED may skip busy quants).
        moved_by_line = {plan["line_index"]: plan["qty"] for plan in move_plan}
        line_summary = [
            {
                "product_id": line["product"].id,
                "product_name": line["product"].display_name,
                "requested_qty": line["qty"],
                "moved_qty": moved_by_line.get(index, 0.0),
            }
            for index, line in enumerate(prepared_lines)
        ]
        fully_transferred = all(
            float_compare(
                summary["moved_qty"],
                summary["requested_qty"],
                precision_rounding=(
                    self.env["product.product"]
                    .browse(summary["product_id"])
                    .uom_id.rounding
                ),
            )
            >= 0
            for summary in line_summary
        )
        return {
            "picking_id": picking.id,
            "picking_name": picking.name,
            "state": picking.state,
            "fully_transferred": fully_transferred,
            "lines": line_summary,
        }
