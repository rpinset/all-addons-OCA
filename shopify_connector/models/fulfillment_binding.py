# pylint: disable=consider-merging-classes-inherited

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ShopifyFulfillmentOrder(models.Model):
    _name = "shopify.fulfillment.order"
    _description = "Shopify Fulfillment Order"
    _inherit = "shopify.binding.mixin"
    _order = "id"
    _rec_name = "shopify_id"
    _check_company_auto = True

    order_binding_id = fields.Many2one(
        "shopify.order",
        required=True,
        index=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    assigned_location_id = fields.Many2one(
        "shopify.location",
        string="Assigned Shopify Location",
        index=True,
        ondelete="restrict",
    )
    assigned_location_shopify_id = fields.Char(readonly=True, index=True)
    assigned_location_name = fields.Char(readonly=True)
    fulfillment_status = fields.Char(string="Status", readonly=True, index=True)
    request_status = fields.Char(readonly=True, index=True)
    supported_actions = fields.Json(readonly=True)
    fulfillment_holds = fields.Json(readonly=True)
    is_held = fields.Boolean(readonly=True, index=True)
    line_ids = fields.One2many(
        "shopify.fulfillment.order.line",
        "fulfillment_order_id",
        string="Remaining Lines",
    )
    fulfillment_ids = fields.Many2many(
        "shopify.fulfillment",
        "shopify_fulfillment_order_rel",
        "fulfillment_order_id",
        "fulfillment_id",
        string="Fulfillments",
        readonly=True,
    )

    @api.constrains("instance_id", "order_binding_id", "assigned_location_id")
    def _check_fulfillment_order_scope(self):
        for binding in self:
            if binding.order_binding_id.instance_id != binding.instance_id:
                raise ValidationError(
                    self.env._(
                        "The fulfillment order must use its order's Shopify instance."
                    )
                )
            if (
                binding.assigned_location_id
                and binding.assigned_location_id.instance_id != binding.instance_id
            ):
                raise ValidationError(
                    self.env._(
                        "The assigned location must use the same Shopify instance."
                    )
                )

    def action_refresh(self):
        self.mapped("order_binding_id").action_refresh_fulfillment_orders()
        return True

    def action_release_hold(self):
        for binding in self:
            binding.with_delay(
                description=self.env._(
                    "Release Shopify fulfillment hold %s", binding.shopify_id
                ),
                identity_key=(
                    f"shopify.fulfillment.hold.release."
                    f"{binding.instance_id.id}.{binding.shopify_id}"
                ),
            )._job_release_hold()
        return True


class ShopifyFulfillmentOrderLine(models.Model):
    _name = "shopify.fulfillment.order.line"
    _description = "Shopify Fulfillment Order Line"
    _order = "id"
    _check_company_auto = True

    fulfillment_order_id = fields.Many2one(
        "shopify.fulfillment.order",
        required=True,
        index=True,
        ondelete="cascade",
    )
    instance_id = fields.Many2one(
        "shopify.instance",
        related="fulfillment_order_id.instance_id",
        store=True,
        readonly=True,
        index=True,
    )
    company_id = fields.Many2one(
        "res.company",
        related="fulfillment_order_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    shopify_id = fields.Char(
        string="Fulfillment Order Line GID",
        required=True,
        readonly=True,
        index=True,
    )
    order_line_binding_id = fields.Many2one(
        "shopify.order.line",
        string="Shopify Order Line",
        index=True,
        ondelete="restrict",
    )
    order_line_shopify_id = fields.Char(readonly=True, index=True)
    total_quantity = fields.Integer(readonly=True)
    remaining_quantity = fields.Integer(readonly=True)

    _fulfillment_order_line_unique = models.Constraint(
        "UNIQUE(fulfillment_order_id, shopify_id)",
        "A fulfillment-order line can only be imported once.",
    )

    @api.constrains("fulfillment_order_id", "order_line_binding_id")
    def _check_fulfillment_line_scope(self):
        for line in self.filtered("order_line_binding_id"):
            fulfillment_order = line.fulfillment_order_id
            if (
                line.order_line_binding_id.order_binding_id
                != fulfillment_order.order_binding_id
                or line.order_line_binding_id.instance_id
                != fulfillment_order.instance_id
            ):
                raise ValidationError(
                    self.env._("The fulfillment line must belong to its Shopify order.")
                )


class ShopifyFulfillment(models.Model):
    _name = "shopify.fulfillment"
    _description = "Shopify Fulfillment"
    _inherit = "shopify.binding.mixin"
    _order = "create_date desc, id desc"
    _rec_name = "shopify_id"
    _check_company_auto = True

    shopify_id = fields.Char(
        string="Shopify GID",
        required=False,
        readonly=True,
        index=True,
    )
    order_binding_id = fields.Many2one(
        "shopify.order",
        required=True,
        index=True,
        ondelete="cascade",
    )
    fulfillment_order_ids = fields.Many2many(
        "shopify.fulfillment.order",
        "shopify_fulfillment_order_rel",
        "fulfillment_id",
        "fulfillment_order_id",
        string="Fulfillment Orders",
        readonly=True,
    )
    picking_id = fields.Many2one(
        "stock.picking",
        string="Odoo Delivery",
        check_company=True,
        index=True,
        readonly=True,
        ondelete="set null",
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    idempotency_key = fields.Char(readonly=True, index=True, copy=False)
    origin = fields.Selection(
        [("odoo", "Odoo"), ("shopify", "Shopify / External")],
        required=True,
        default="shopify",
        readonly=True,
        index=True,
    )
    fulfillment_status = fields.Char(string="Status", readonly=True, index=True)
    location_shopify_id = fields.Char(readonly=True, index=True)
    tracking_company = fields.Char(readonly=True)
    tracking_number = fields.Char(readonly=True)
    tracking_url = fields.Char(readonly=True)
    raw_payload = fields.Json(readonly=True)

    _instance_idempotency_unique = models.Constraint(
        "UNIQUE(instance_id, idempotency_key)",
        "This Odoo delivery was already sent to Shopify.",
    )

    @api.constrains(
        "instance_id", "order_binding_id", "fulfillment_order_ids", "picking_id"
    )
    def _check_fulfillment_scope(self):
        for binding in self:
            if binding.order_binding_id.instance_id != binding.instance_id:
                raise ValidationError(
                    self.env._("The fulfillment must use its order's Shopify instance.")
                )
            if binding.fulfillment_order_ids.filtered(
                lambda item, binding=binding: (
                    item.instance_id != binding.instance_id
                    or item.order_binding_id != binding.order_binding_id
                )
            ):
                raise ValidationError(
                    self.env._(
                        "All fulfillment orders must belong to the same Shopify order."
                    )
                )
            if (
                binding.picking_id
                and binding.picking_id.company_id != binding.company_id
            ):
                raise ValidationError(
                    self.env._(
                        "The delivery must belong to the Shopify instance company."
                    )
                )

    def action_cancel_shopify(self):
        for fulfillment in self.filtered("shopify_id"):
            fulfillment.with_delay(
                description=self.env._(
                    "Cancel Shopify fulfillment %s", fulfillment.shopify_id
                ),
                identity_key=(
                    f"shopify.fulfillment.cancel."
                    f"{fulfillment.instance_id.id}.{fulfillment.shopify_id}"
                ),
            )._job_cancel_shopify()
        return True


class ShopifyCarrierMapping(models.Model):
    _name = "shopify.carrier.mapping"
    _description = "Shopify Carrier Mapping"
    _order = "carrier_id"
    _rec_name = "tracking_company"
    _check_company_auto = True

    instance_id = fields.Many2one(
        "shopify.instance",
        required=True,
        index=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    carrier_id = fields.Many2one(
        "delivery.carrier",
        required=True,
        check_company=True,
        ondelete="cascade",
    )
    tracking_company = fields.Char(
        required=True,
        help="Company string sent in Shopify tracking information.",
    )

    _instance_carrier_unique = models.Constraint(
        "UNIQUE(instance_id, carrier_id)",
        "A delivery carrier can only be mapped once per Shopify instance.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if not values.get("tracking_company") and values.get("carrier_id"):
                values["tracking_company"] = (
                    self.env["delivery.carrier"].browse(values["carrier_id"]).name
                )
        return super().create(vals_list)

    @api.constrains("instance_id", "carrier_id")
    def _check_carrier_company(self):
        for mapping in self:
            carrier_company = mapping.carrier_id.company_id
            if carrier_company and carrier_company != mapping.company_id:
                raise ValidationError(
                    self.env._(
                        "The carrier must belong to the Shopify instance company."
                    )
                )


class ShopifyOrderFulfillmentRelation(models.Model):
    _inherit = "shopify.order"

    fulfillment_order_ids = fields.One2many(
        "shopify.fulfillment.order",
        "order_binding_id",
        string="Fulfillment Orders",
    )
    fulfillment_ids = fields.One2many(
        "shopify.fulfillment",
        "order_binding_id",
        string="Fulfillments",
    )


class ShopifyInstanceFulfillmentConfiguration(models.Model):
    _inherit = "shopify.instance"

    fulfillment_notify_customer = fields.Boolean(
        string="Notify Customer",
        default=True,
        help="Ask Shopify to send its fulfillment notification.",
    )
    fulfillment_auto_validate_webhook = fields.Boolean(
        string="Validate Deliveries from Webhooks",
        default=False,
        help=(
            "Validate matching Odoo deliveries when an external Shopify "
            "fulfillment webhook is received. Disabled is log-only."
        ),
    )
    carrier_mapping_ids = fields.One2many(
        "shopify.carrier.mapping",
        "instance_id",
        string="Carrier Mappings",
    )


class StockPickingShopifyFulfillmentBinding(models.Model):
    _inherit = "stock.picking"

    shopify_fulfillment_ids = fields.One2many(
        "shopify.fulfillment",
        "picking_id",
        string="Shopify Fulfillments",
        readonly=True,
    )
