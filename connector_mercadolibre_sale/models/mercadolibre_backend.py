# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import AccessError, ValidationError


class MercadoLibreBackend(models.Model):
    _inherit = "mercadolibre.backend"

    import_orders = fields.Boolean()
    import_orders_since = fields.Datetime(string="Import orders since")
    last_order_sync_at = fields.Datetime(readonly=True, copy=False)
    workflow_process_id = fields.Many2one(
        comodel_name="sale.workflow.process",
        string="Automatic Workflow",
        ondelete="restrict",
    )
    team_id = fields.Many2one(comodel_name="crm.team", string="Sales Team")
    fiscal_position_id = fields.Many2one(
        comodel_name="account.fiscal.position",
    )
    shipping_product_id = fields.Many2one(
        comodel_name="product.product",
        domain="[('type', '=', 'service')]",
    )
    fee_product_id = fields.Many2one(
        comodel_name="product.product",
        domain="[('type', '=', 'service')]",
    )
    tracking_carrier_id = fields.Many2one(
        comodel_name="delivery.carrier",
    )
    sale_binding_ids = fields.One2many(
        comodel_name="mercadolibre.sale.order",
        inverse_name="backend_id",
    )

    @api.constrains("import_orders", "workflow_process_id")
    def _check_import_orders_workflow(self):
        for backend in self:
            if backend.import_orders and not backend.workflow_process_id:
                raise ValidationError(
                    self.env._(
                        "Choose an automatic workflow before importing Mercado Libre "
                        "orders."
                    )
                )

    def _check_sales_manager(self):
        if not self.env.user.has_group(
            "connector_mercadolibre.group_mercadolibre_manager"
        ):
            raise AccessError(
                self.env._("Only Mercado Libre managers can import orders.")
            )

    def button_import_orders(self):
        self._check_sales_manager()
        for backend in self:
            backend._enqueue_order_batch()

    def _enqueue_order_batch(self):
        self.ensure_one()
        description = self.env._(
            "Import Mercado Libre orders for %(name)s",
            name=self.display_name,
        )
        self.with_delay(
            identity_key=f"meli:orders:{self.id}",
            description=description,
        )._job_import_orders()

    def _enqueue_order_import(self, order_id):
        self.ensure_one()
        order_id = str(order_id)
        description = self.env._(
            "Import Mercado Libre order %(order)s",
            order=order_id,
        )
        self.with_delay(
            identity_key=f"meli:order:{self.id}:{order_id}",
            description=description,
        )._job_import_order(order_id)

    def _enqueue_shipment_import(self, shipment_id):
        self.ensure_one()
        shipment_id = str(shipment_id)
        description = self.env._(
            "Import Mercado Libre shipment %(shipment)s",
            shipment=shipment_id,
        )
        self.with_delay(
            identity_key=f"meli:shipment:{self.id}:{shipment_id}",
            description=description,
        )._job_import_shipment(shipment_id)

    def _enqueue_payment_import(self, resource):
        self.ensure_one()
        description = self.env._(
            "Import Mercado Libre payment %(resource)s",
            resource=resource,
        )
        self.with_delay(
            identity_key=f"meli:payment:{self.id}:{resource}",
            description=description,
        )._job_import_payment(resource)

    def _job_import_orders(self):
        self.ensure_one()
        if not self.import_orders:
            return
        with self.work_on("mercadolibre.sale.order") as work:
            work.component(usage="batch.importer").run()

    def _job_import_order(self, order_id):
        self.ensure_one()
        with self.work_on("mercadolibre.sale.order") as work:
            work.component(usage="record.importer").run(order_id)

    def _job_import_shipment(self, shipment_id):
        self.ensure_one()
        with self.work_on("mercadolibre.shipment") as work:
            work.component(usage="record.importer").run(shipment_id)

    def _job_import_payment(self, resource):
        self.ensure_one()
        with self.work_on("mercadolibre.sale.order") as work:
            work.component(usage="payment.importer").run(resource)

    @api.model
    def cron_import_orders(self):
        backends = self.search([("import_orders", "=", True)])
        for backend in backends:
            backend._enqueue_order_batch()
