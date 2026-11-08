# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.exceptions import AccessError


class MercadoLibreShipment(models.Model):
    _name = "mercadolibre.shipment"
    _inherit = "mercadolibre.binding"
    _description = "Mercado Libre Shipment"
    _order = "id desc"

    backend_id = fields.Many2one(
        comodel_name="mercadolibre.backend",
        required=True,
        ondelete="restrict",
        index=True,
    )
    external_id = fields.Char(required=True, index=True)
    sale_binding_ids = fields.One2many(
        comodel_name="mercadolibre.sale.order",
        inverse_name="shipment_id",
    )
    picking_id = fields.Many2one(
        comodel_name="stock.picking",
        ondelete="set null",
        index=True,
    )
    logistic_type = fields.Char()
    mode = fields.Char()
    status = fields.Char()
    tracking_number = fields.Char()
    receiver_partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Receiver",
        ondelete="set null",
    )

    _shipment_external_unique = models.Constraint(
        "UNIQUE(backend_id, external_id)",
        "This Mercado Libre shipment is already imported.",
    )

    def _check_sales_manager(self):
        if not self.env.user.has_group(
            "connector_mercadolibre.group_mercadolibre_manager"
        ):
            raise AccessError(
                self.env._("Only Mercado Libre managers can import shipments.")
            )

    def button_import(self):
        self._check_sales_manager()
        for shipment in self:
            shipment.backend_id._enqueue_shipment_import(shipment.external_id)

    def _job_import(self):
        self.ensure_one()
        self.backend_id._job_import_shipment(self.external_id)

    def _seller_provides_tracking(self):
        self.ensure_one()
        if self.logistic_type == "fulfillment":
            return False
        return self.mode in ("custom", "me1")

    def _enqueue_tracking_export(self):
        for shipment in self.filtered(lambda row: row._seller_provides_tracking()):
            description = shipment.env._(
                "Export Mercado Libre tracking for %(shipment)s",
                shipment=shipment.external_id,
            )
            shipment.with_delay(
                identity_key=(f"meli:tracking:{shipment.backend_id.id}:{shipment.id}"),
                description=description,
            )._job_export_tracking()

    def _job_export_tracking(self):
        self.ensure_one()
        if not self._seller_provides_tracking():
            return False
        tracking = self.picking_id.carrier_tracking_ref or self.tracking_number
        if not tracking:
            return False
        with self.backend_id.work_on(self._name) as work:
            work.component(usage="backend.adapter").export_tracking(
                self.external_id, tracking
            )
        self.mark_synced()
        return True
