# pylint: disable=consider-merging-classes-inherited

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ShopifyLocation(models.Model):
    _name = "shopify.location"
    _description = "Shopify Location Binding"
    _inherit = "shopify.binding.mixin"
    _order = "active desc, name"
    _check_company_auto = True

    name = fields.Char(required=True, index=True)
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    legacy_resource_id = fields.Char(
        string="Shopify Legacy ID",
        readonly=True,
        index=True,
    )
    active = fields.Boolean(
        string="Active in Shopify",
        default=True,
        readonly=True,
        index=True,
    )
    fulfills_online_orders = fields.Boolean(readonly=True)
    address = fields.Char(readonly=True)
    warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="Odoo Warehouse",
        check_company=True,
        ondelete="restrict",
        help="Selecting a warehouse maps its main stock location by default.",
    )
    odoo_location_id = fields.Many2one(
        "stock.location",
        string="Odoo Internal Location",
        check_company=True,
        ondelete="restrict",
        domain="[('usage', '=', 'internal')]",
    )
    is_mapped = fields.Boolean(
        string="Mapped",
        compute="_compute_is_mapped",
        store=True,
        index=True,
    )

    _instance_odoo_location_unique = models.Constraint(
        "UNIQUE(instance_id, odoo_location_id)",
        "An Odoo stock location can only be mapped once per Shopify instance.",
    )

    @api.depends("odoo_location_id")
    def _compute_is_mapped(self):
        for binding in self:
            binding.is_mapped = bool(binding.odoo_location_id)

    @api.onchange("warehouse_id")
    def _onchange_warehouse_id(self):
        for binding in self:
            if binding.warehouse_id:
                binding.odoo_location_id = binding.warehouse_id.lot_stock_id

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("warehouse_id") and not values.get("odoo_location_id"):
                warehouse = self.env["stock.warehouse"].browse(values["warehouse_id"])
                values["odoo_location_id"] = warehouse.lot_stock_id.id
        return super().create(vals_list)

    def write(self, values):
        if values.get("warehouse_id") and "odoo_location_id" not in values:
            self.ensure_one()
            warehouse = self.env["stock.warehouse"].browse(values["warehouse_id"])
            values = {
                **values,
                "odoo_location_id": warehouse.lot_stock_id.id,
            }
        return super().write(values)

    @api.constrains("instance_id", "warehouse_id", "odoo_location_id")
    def _check_location_company_and_usage(self):
        for binding in self:
            company = binding.instance_id.company_id
            if binding.warehouse_id and binding.warehouse_id.company_id != company:
                raise ValidationError(
                    self.env._("The warehouse must belong to the instance company.")
                )
            location = binding.odoo_location_id
            if not location:
                continue
            if location.usage != "internal":
                raise ValidationError(
                    self.env._("Shopify inventory must map to an internal location.")
                )
            if location.company_id and location.company_id != company:
                raise ValidationError(
                    self.env._(
                        "The stock location must belong to the instance company."
                    )
                )
            if (
                binding.warehouse_id
                and location not in binding.warehouse_id.view_location_id.child_ids
                and not location.parent_path.startswith(
                    f"{binding.warehouse_id.view_location_id.parent_path}"
                )
            ):
                raise ValidationError(
                    self.env._(
                        "The stock location must belong to the selected warehouse."
                    )
                )


class ShopifyInventoryState(models.Model):
    _name = "shopify.inventory.state"
    _description = "Shopify Inventory Synchronization State"
    _order = "last_sync_date desc, id desc"
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
    variant_binding_id = fields.Many2one(
        "shopify.product.variant",
        required=True,
        index=True,
        ondelete="cascade",
    )
    location_binding_id = fields.Many2one(
        "shopify.location",
        required=True,
        index=True,
        ondelete="cascade",
    )
    last_pushed_quantity = fields.Integer(readonly=True)
    last_pushed_at = fields.Datetime(readonly=True)
    last_shopify_quantity = fields.Integer(readonly=True)
    last_sync_date = fields.Datetime(readonly=True)

    _inventory_state_unique = models.Constraint(
        "UNIQUE(instance_id, variant_binding_id, location_binding_id)",
        "Inventory state must be unique per instance, variant, and location.",
    )

    @api.constrains("instance_id", "variant_binding_id", "location_binding_id")
    def _check_inventory_state_scope(self):
        for state in self:
            if (
                state.variant_binding_id.instance_id != state.instance_id
                or state.location_binding_id.instance_id != state.instance_id
            ):
                raise ValidationError(
                    self.env._("Inventory state records must use one Shopify instance.")
                )


class ShopifyProductVariantInventory(models.Model):
    _inherit = "shopify.product.variant"

    inventory_item_shopify_id = fields.Char(
        string="Shopify Inventory Item GID",
        readonly=True,
        copy=False,
        index=True,
    )
    inventory_tracked = fields.Boolean(
        string="Tracked by Shopify",
        readonly=True,
        copy=False,
        index=True,
    )
    inventory_sync_enabled = fields.Boolean(
        string="Synchronize Inventory",
        default=True,
        help="Disable to opt this variant out of inventory synchronization.",
    )
    inventory_state_ids = fields.One2many(
        "shopify.inventory.state",
        "variant_binding_id",
        string="Inventory Levels",
    )
    inventory_sync_status = fields.Selection(
        [
            ("ready", "Ready"),
            ("disabled", "Opted Out"),
            ("not_tracked", "Not Tracked"),
            ("not_storable", "Not Storable"),
            ("missing_item", "Missing Inventory Item"),
        ],
        compute="_compute_inventory_sync_status",
        string="Inventory Status",
    )

    @api.depends(
        "inventory_sync_enabled",
        "template_binding_id.inventory_sync_enabled",
        "inventory_tracked",
        "inventory_item_shopify_id",
        "odoo_id.is_storable",
        "odoo_id.type",
    )
    def _compute_inventory_sync_status(self):
        for binding in self:
            if (
                not binding.inventory_sync_enabled
                or not binding.template_binding_id.inventory_sync_enabled
            ):
                status = "disabled"
            elif not binding.inventory_tracked:
                status = "not_tracked"
            elif not binding._is_storable_inventory_product():
                status = "not_storable"
            elif not binding.inventory_item_shopify_id:
                status = "missing_item"
            else:
                status = "ready"
            binding.inventory_sync_status = status

    def _is_storable_inventory_product(self):
        self.ensure_one()
        product = self.odoo_id
        if "is_storable" in product._fields:
            return bool(product.is_storable)
        return product.type == "product"


class ShopifyProductTemplateInventory(models.Model):
    _inherit = "shopify.product.template"

    inventory_sync_enabled = fields.Boolean(
        string="Synchronize Inventory",
        default=True,
        help="Disable to opt every variant of this product out of inventory sync.",
    )
    inventory_sync_status = fields.Char(
        compute="_compute_template_inventory_sync_status",
        string="Inventory Status",
    )

    @api.depends(
        "inventory_sync_enabled",
        "variant_binding_ids.inventory_sync_status",
    )
    def _compute_template_inventory_sync_status(self):
        for binding in self:
            statuses = set(binding.variant_binding_ids.mapped("inventory_sync_status"))
            if not binding.inventory_sync_enabled:
                binding.inventory_sync_status = self.env._("Opted out")
            elif not statuses:
                binding.inventory_sync_status = self.env._("No variants")
            elif statuses == {"ready"}:
                binding.inventory_sync_status = self.env._("Ready")
            elif "ready" in statuses:
                binding.inventory_sync_status = self.env._("Partially ready")
            else:
                binding.inventory_sync_status = self.env._("Not synchronized")


class ShopifyInstanceInventoryConfig(models.Model):
    _inherit = "shopify.instance"

    location_binding_ids = fields.One2many(
        "shopify.location",
        "instance_id",
        string="Shopify Locations",
    )
    inventory_import_enabled = fields.Boolean(
        string="Import Shopify Inventory",
        default=False,
        help=("Apply inventory_levels/update webhooks to mapped Odoo locations."),
    )
    inventory_quantity_basis = fields.Selection(
        [
            ("free_qty", "Free Quantity"),
            ("qty_available", "On-hand Quantity"),
        ],
        required=True,
        default="free_qty",
        help="Odoo quantity used as the source for Shopify available stock.",
    )
    inventory_allow_negative = fields.Boolean(
        string="Allow Negative Shopify Quantities",
        default=False,
        help="Otherwise negative Odoo stock is clamped to zero and logged.",
    )
    inventory_echo_window_seconds = fields.Integer(
        string="Webhook Echo Window",
        required=True,
        default=300,
        help="Seconds during which a matching Shopify webhook is an echo.",
    )

    @api.constrains("inventory_echo_window_seconds")
    def _check_inventory_echo_window(self):
        for instance in self:
            if instance.inventory_echo_window_seconds < 0:
                raise ValidationError(
                    self.env._("The inventory webhook echo window cannot be negative.")
                )
