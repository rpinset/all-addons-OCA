# Copyright 2026 Binhex
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import Command, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    barcode_lot_name = fields.Char(
        string="Lot/Serial Read",
        copy=False,
        help="The lot or serial number read from the label when the order was "
        "raised from the Barcode app. It goes onto the receipt when the receipt "
        "is created.",
    )


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _create_picking(self):
        res = super()._create_picking()
        # However the order gets confirmed -- from the scanner, or approved later
        # in the back office -- the lots read go onto its receipt.
        self._barcode_purchase_place_lots()
        return res

    @api.model
    def _barcode_purchase_prepare_lines(self, lines):
        """Validate the scanned lines and resolve their products.

        Returns a list of ``(product, qty, price_unit, lot_name)`` tuples, one per
        scanned line and in the same order: each becomes an order line of its
        own, so a lot scanned on it keeps a receipt move of its own too.
        """
        prepared = []
        for line in lines or []:
            product = (
                self.env["product.product"].browse(line.get("product_id")).exists()
            )
            if not product:
                raise UserError(
                    self.env._("One of the scanned products no longer exists.")
                )
            if not product.purchase_ok:
                raise UserError(
                    self.env._(
                        "%(name)s cannot be purchased.", name=product.display_name
                    )
                )
            qty = float(line.get("qty") or 0)
            if (
                float_compare(qty, 0, precision_rounding=product.uom_po_id.rounding)
                <= 0
            ):
                raise UserError(
                    self.env._(
                        "The quantity to order of %(name)s must be positive.",
                        name=product.display_name,
                    )
                )
            lot_name = (line.get("lot_name") or "").strip() or False
            if (
                product.tracking == "serial"
                and lot_name
                and float_compare(qty, 1, precision_rounding=product.uom_po_id.rounding)
            ):
                raise UserError(
                    self.env._(
                        "Serial number %(lot)s of %(name)s stands for a single unit.",
                        lot=lot_name,
                        name=product.display_name,
                    )
                )
            # No price is not a price of 0 (a free sample): only an empty one
            # leaves the line to the vendor's prices.
            price_unit = line.get("price_unit")
            no_price = price_unit is None or price_unit is False or price_unit == ""
            prepared.append(
                (
                    product,
                    qty,
                    None if no_price else float(price_unit),
                    lot_name,
                )
            )
        if not prepared:
            raise UserError(self.env._("Add at least one product to the order."))
        return prepared

    @api.model
    def barcode_purchase_prices(self, partner_id, lines):
        """The unit price each line would get on an order for the vendor, so
        the scanner can show it before the order exists: computed as the order
        computes it, from the vendor's prices, in the purchase unit and in the
        order's currency. ``lines`` are ``{product_id, qty}``; a line whose
        product is gone gets None."""
        partner = self.env["res.partner"].browse(partner_id).exists()
        order = self.new({"partner_id": partner.id, "company_id": self.env.company.id})
        OrderLine = self.env["purchase.order.line"]
        prices = []
        for line in lines or []:
            product = (
                self.env["product.product"].browse(line.get("product_id")).exists()
            )
            if not partner or not product:
                prices.append(None)
                continue
            order_line = OrderLine.new(
                {"product_id": product.id, "product_qty": float(line.get("qty") or 1)}
            )
            order_line.order_id = order
            prices.append(order_line.price_unit)
        return prices

    @api.model
    def _barcode_purchase_destination(self, location_id, company):
        """Where the goods of the order end up, with the receipt operation of its
        warehouse: an internal location of the company, in a warehouse that
        receives goods. ``(None, None)`` when the operator chose none."""
        if not location_id:
            return None, None
        Location = self.env["stock.location"]
        location = Location.search(
            [("id", "=", location_id), ("usage", "=", "internal")]
            + Location._check_company_domain(company),
            limit=1,
        )
        picking_type = location.warehouse_id.in_type_id
        if not location or not picking_type:
            raise UserError(self.env._("The selected destination is not valid."))
        return location, picking_type

    def _barcode_purchase_place_lots(self):
        """Write the lots read from the labels on the receipt, each on a free
        move line of its own order line's moves, once."""
        for order_line in self.order_line.filtered("barcode_lot_name"):
            move_lines = order_line.move_ids.move_line_ids
            if order_line.barcode_lot_name in move_lines.mapped("lot_name"):
                continue
            free = move_lines.filtered(lambda ml: not ml.lot_id and not ml.lot_name)
            free[:1].lot_name = order_line.barcode_lot_name

    def _barcode_purchase_unplaced_lots(self):
        """The lots read that found no free move line on the receipt, for the
        operator to enter by hand."""
        return [
            f"{line.product_id.display_name} ({line.barcode_lot_name})"
            for line in self.order_line.filtered("barcode_lot_name")
            if line.barcode_lot_name
            not in line.move_ids.move_line_ids.mapped("lot_name")
        ]

    @api.model
    def action_barcode_purchase(
        self,
        partner_id,
        lines,
        confirm=False,
        location_dest_id=False,
        user_id=False,
        partner_ref=False,
    ):
        """Create the purchase order the scanner drafted, and confirm it when
        asked -- all in one transaction, so a failure leaves no half-made order.

        ``lines`` are ``{product_id, qty, price_unit, lot_name}``; a missing
        ``price_unit`` lets Odoo price the line from the vendor's prices.

        Both the destination and the lots are kept on the order, so they hold
        however the order is confirmed: from here, or approved later in the back
        office. ``location_dest_id`` picks the receipt operation of its warehouse
        and is each line's final location, which the stock moves follow (in a
        reception in several steps, through the steps). The lots read are kept
        on their lines and written on the receipt when it is created.

        A lot-tracked product without a lot does not hold the order back: a
        vendor's lot is usually unknown until the goods turn up, and it belongs
        on the receipt. Those products are returned in ``missing_lots``.
        """
        partner = self.env["res.partner"].browse(partner_id).exists()
        if not partner:
            raise UserError(self.env._("The selected vendor no longer exists."))
        prepared = self._barcode_purchase_prepare_lines(lines)
        company = self.env.company
        destination, picking_type = self._barcode_purchase_destination(
            location_dest_id, company
        )
        order_lines = []
        for product, qty, price_unit, lot_name in prepared:
            vals = {
                "product_id": product.id,
                "product_qty": qty,
                "barcode_lot_name": lot_name,
            }
            if price_unit is not None:
                vals["price_unit"] = price_unit
            if destination:
                vals["location_final_id"] = destination.id
            order_lines.append(Command.create(vals))
        order_vals = {
            "partner_id": partner.id,
            "partner_ref": partner_ref or False,
            "user_id": user_id or self.env.user.id,
            "company_id": company.id,
            "order_line": order_lines,
        }
        if picking_type:
            order_vals["picking_type_id"] = picking_type.id
        order = self.create(order_vals)
        if confirm:
            order.button_confirm()
        received = bool(order.picking_ids)
        return {
            "id": order.id,
            "name": order.name,
            "state": order.state,
            "missing_lots": [
                product.display_name
                for product, _qty, _price, lot_name in prepared
                if received and product.tracking != "none" and not lot_name
            ],
            "unplaced_lots": order._barcode_purchase_unplaced_lots()
            if received
            else [],
        }
