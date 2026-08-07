# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>

import math

from odoo import api, fields, models

from .stock_delivery_note import DOMAIN_DELIVERY_NOTE_STATES, DOMAIN_INVOICE_STATUSES


class SaleOrder(models.Model):
    _inherit = "sale.order"

    default_transport_condition_id = fields.Many2one(
        "stock.picking.transport.condition",
        string="Condition of transport",
        default=False,
    )
    default_goods_appearance_id = fields.Many2one(
        "stock.picking.goods.appearance", string="Appearance of goods", default=False
    )
    default_transport_reason_id = fields.Many2one(
        "stock.picking.transport.reason", string="Reason of transport", default=False
    )
    default_transport_method_id = fields.Many2one(
        "stock.picking.transport.method", string="Method of transport", default=False
    )

    @api.onchange("partner_id")
    def onchange_partner_id_shipping_info(self):
        if self.partner_id:
            values = {
                "default_transport_condition_id": (
                    self.partner_id.default_transport_condition_id
                ),
                "default_goods_appearance_id": (
                    self.partner_id.default_goods_appearance_id
                ),
                "default_transport_reason_id": (
                    self.partner_id.default_transport_reason_id
                ),
                "default_transport_method_id": (
                    self.partner_id.default_transport_method_id
                ),
            }

        else:
            values = {
                "default_transport_condition_id": False,
                "default_goods_appearance_id": False,
                "default_transport_reason_id": False,
                "default_transport_method_id": False,
            }

        self.update(values)

    def _assign_delivery_notes_invoices(self, invoice_ids):
        invoices = self.env["account.move"].browse(invoice_ids)
        for order_line in self.order_line:
            for dn_line in order_line.delivery_note_line_ids:
                if dn_line.delivery_note_id.state == DOMAIN_DELIVERY_NOTE_STATES[0]:
                    # The Delivery Note is not ready for invoicing yet,
                    # so all its lines do not have to be invoiced
                    dn_line.invoice_status = DOMAIN_INVOICE_STATUSES[0]
                    continue

                invoiced_dn_lines = (
                    dn_line.sale_line_id.invoice_lines.delivery_note_line_id
                )
                for inv_line in invoices.invoice_line_ids:
                    if dn_line.sale_line_id in inv_line.sale_line_ids:
                        if not inv_line.delivery_note_line_id:
                            # The invoice line is usually linked
                            # upon invoice line creation
                            # (see `sale.order.line._prepare_invoice_line`).
                            # In the case of Kits, we need to create the link
                            # because the Invoiced Kit does not appear in the Delivery Note.
                            inv_line.delivery_note_line_id = dn_line
                        elif dn_line not in invoiced_dn_lines:
                            # The Delivery Note Line is not linked
                            # to any Invoice of the current Sale Order Line
                            continue

                        dn_line.invoice_status = DOMAIN_INVOICE_STATUSES[2]
                        break
                else:
                    dn_line.invoice_status = DOMAIN_INVOICE_STATUSES[1]

    def _generate_delivery_note_lines(self, invoice_ids):
        invoices = self.env["account.move"].browse(invoice_ids)
        invoices.update_delivery_note_lines()

    def _get_invoiceable_lines(self, final=False):
        order_lines = super()._get_invoiceable_lines(final=final)
        new_order_lines = self.env["sale.order.line"].browse()
        for order_line in order_lines:
            invoiceable_dn_lines = order_line._get_invoiceable_dn_lines()
            if len(invoiceable_dn_lines) > 1:
                # Add a new order line for each linked delivery note line.
                # Every new corresponding invoice line
                # will invoice the delivered quantity
                for _index in range(len(invoiceable_dn_lines) - 1):
                    new_order_lines += order_line
            new_order_lines += order_line
        return new_order_lines

    def _create_invoices(self, grouped=False, final=False, date=None):
        invoice_ids = super()._create_invoices(grouped=grouped, final=final, date=date)

        self._assign_delivery_notes_invoices(invoice_ids.ids)
        self._generate_delivery_note_lines(invoice_ids.ids)

        return invoice_ids


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    delivery_note_line_ids = fields.One2many(
        "stock.delivery.note.line", "sale_line_id", readonly=True
    )
    delivery_picking_id = fields.Many2one("stock.picking", readonly=True, copy=False)

    @property
    def has_picking(self):
        return self.move_ids or (self.is_delivery and self.delivery_picking_id)

    @property
    def is_invoiceable(self):
        return (
            self.invoice_status == DOMAIN_INVOICE_STATUSES[1]
            and self.qty_to_invoice != 0
        )

    @property
    def is_invoiced(self):
        return (
            self.invoice_status != DOMAIN_INVOICE_STATUSES[1] and self.qty_invoiced != 0
        )

    @property
    def need_to_be_invoiced(self):
        return self.product_uom_qty != (self.qty_to_invoice + self.qty_invoiced)

    def fix_qty_to_invoice(self, new_qty_to_invoice=0):
        self.ensure_one()

        cache = {
            "invoice_status": self.invoice_status,
            "qty_to_invoice": self.qty_to_invoice,
        }

        self.write(
            {
                "invoice_status": "to invoice" if new_qty_to_invoice else "no",
                "qty_to_invoice": new_qty_to_invoice,
            }
        )

        return cache

    def is_pickings_related(self, picking_ids):
        if self.is_delivery:
            return self.delivery_picking_id in picking_ids

        return bool(self.move_ids & picking_ids.mapped("move_lines"))

    def retrieve_pickings_lines(self, picking_ids):
        return self.filtered(lambda li: li.has_picking).filtered(
            lambda li: li.is_pickings_related(picking_ids)
        )

    def _get_invoiceable_dn_lines(self):
        invoiceable_dn_lines = self.delivery_note_line_ids.filtered(
            lambda dn_line: dn_line.is_invoiceable
            and self.product_id == dn_line.product_id
        )
        invoicing_delivery_notes = self.env.context.get(
            "invoicing_delivery_notes",
            self.env["stock.delivery.note"].browse(),
        )
        if invoicing_delivery_notes:
            invoiceable_dn_lines = invoiceable_dn_lines.filtered(
                lambda dn_line: dn_line.delivery_note_id in invoicing_delivery_notes
            )
        return invoiceable_dn_lines

    def _prepare_invoice_line(self, **optional_values):
        values = super()._prepare_invoice_line(**optional_values)
        invoiced_dn_lines = self.env.context.get(
            "delivery_note_invoiced_lines",
            self.env["stock.delivery.note.line"].browse(),
        )
        invoiceable_dn_lines = self._get_invoiceable_dn_lines() - invoiced_dn_lines

        if invoiceable_dn_lines:
            invoiced_dn_line = fields.first(invoiceable_dn_lines)
            values.update(
                {
                    "delivery_note_line_id": invoiced_dn_line.id,
                    "quantity": math.copysign(
                        invoiced_dn_line.product_qty,
                        values.get("quantity", 1),
                    ),
                }
            )
            self.env.context = dict(
                self.env.context,
                delivery_note_invoiced_lines=invoiced_dn_lines | invoiced_dn_line,
            )
        return values
