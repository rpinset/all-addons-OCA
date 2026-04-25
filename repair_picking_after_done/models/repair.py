# Copyright (C) 2022 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class Repair(models.Model):
    _inherit = "repair.order"

    remaining_quantity = fields.Float(
        "Remaining quantity to be transferred", compute="_compute_remaining_quantity"
    )

    def _compute_remaining_quantity(self):
        for rec in self:
            remaining_quantity = rec.product_qty
            if rec.picking_ids:
                stock_moves = rec.picking_ids.mapped("move_ids").filtered(
                    lambda x: x.state != "cancel"
                )
                remaining_quantity = rec.product_qty - sum(
                    stock_moves.mapped("product_uom_qty")
                )
            rec.remaining_quantity = remaining_quantity

    def action_transfer_done_moves(self):
        self.ensure_one()
        return {
            "name": "Transfer repair moves",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "repair.move.transfer",
            "context": {
                "default_repair_order_id": self.id,
                "default_quantity": self.remaining_quantity,
                "default_remaining_quantity": self.remaining_quantity,
                "default_location_dest_id": self.product_location_dest_id.id,
            },
            "target": "new",
        }

    def _get_auto_transfer_value(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("repair.auto_transfer_repair", default=False)
        )

    def action_validate(self):
        auto_transfer = self._get_auto_transfer_value()

        if auto_transfer and not self.product_id:
            raise ValidationError(
                _(
                    "Automatic transfer cannot be completed because "
                    "no product is specified for this repair order. "
                    "Please ensure that a product is assigned to the "
                    "repair order before proceeding with the transfer."
                )
            )

        return super().action_validate()

    def action_repair_done(self):
        super().action_repair_done()

        auto_transfer = self._get_auto_transfer_value()
        if auto_transfer:
            for repair in self:
                if repair.remaining_quantity > 0:
                    transfer_wizard = self.env["repair.move.transfer"].create(
                        {
                            "repair_order_id": repair.id,
                            "location_dest_id": repair.product_location_dest_id.id,
                            "quantity": repair.remaining_quantity,
                        }
                    )
                    transfer_wizard.action_create_transfer()
                    repair.picking_ids.button_validate()
        return True
