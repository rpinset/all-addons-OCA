from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ShopifyProductTemplate(models.Model):
    _name = "shopify.product.template"
    _description = "Shopify Product Template Binding"
    _inherit = "shopify.binding.mixin"
    _order = "id desc"

    odoo_id = fields.Many2one(
        "product.template",
        string="Odoo Product",
        required=True,
        index=True,
        ondelete="cascade",
    )
    handle = fields.Char(index=True)
    status = fields.Selection(
        [
            ("ACTIVE", "Active"),
            ("DRAFT", "Draft"),
            ("ARCHIVED", "Archived"),
            ("UNLISTED", "Unlisted"),
        ],
        required=True,
        default="DRAFT",
        index=True,
    )
    odoo_status = fields.Selection(
        [
            ("ACTIVE", "Active"),
            ("DRAFT", "Draft"),
            ("ARCHIVED", "Archived"),
            ("UNLISTED", "Unlisted"),
        ],
        string="Odoo-owned Shopify Status",
        required=True,
        default="DRAFT",
        help="Full Shopify lifecycle status used when Odoo owns Status.",
    )
    initial_seed_pending = fields.Boolean(
        readonly=True,
        copy=False,
        help="Retry marker for a newly created Odoo template.",
    )
    remote_deleted = fields.Boolean(
        string="Deleted from Shopify",
        readonly=True,
        copy=False,
        index=True,
    )
    main_image_shopify_id = fields.Char(
        string="Main Image Shopify GID",
        readonly=True,
        copy=False,
    )
    main_image_checksum = fields.Char(readonly=True, copy=False)
    variant_binding_ids = fields.One2many(
        "shopify.product.variant",
        "template_binding_id",
        string="Shopify Variants",
    )
    image_binding_ids = fields.One2many(
        "shopify.product.image",
        "template_binding_id",
        string="Shopify Images",
    )
    collection_ids = fields.Many2many(
        "shopify.collection",
        "shopify_collection_product_rel",
        "product_binding_id",
        "collection_id",
        string="Collections",
    )

    _instance_odoo_unique = models.Constraint(
        "UNIQUE(instance_id, odoo_id)",
        "An Odoo product can only be linked once per Shopify instance.",
    )

    @api.constrains("instance_id", "odoo_id")
    def _check_product_company(self):
        for binding in self:
            if binding.odoo_id.company_id != binding.instance_id.company_id:
                raise ValidationError(
                    self.env._(
                        "The Odoo product and Shopify instance must share a company."
                    )
                )


class ShopifyProductVariant(models.Model):
    _name = "shopify.product.variant"
    _description = "Shopify Product Variant Binding"
    _inherit = "shopify.binding.mixin"
    _order = "id"

    template_binding_id = fields.Many2one(
        "shopify.product.template",
        required=True,
        index=True,
        ondelete="cascade",
    )
    odoo_id = fields.Many2one(
        "product.product",
        string="Odoo Variant",
        required=True,
        index=True,
        ondelete="cascade",
    )
    sku_snapshot = fields.Char(string="Shopify SKU", readonly=True)
    barcode_snapshot = fields.Char(string="Shopify Barcode", readonly=True)
    price_snapshot = fields.Char(
        string="Shopify Price",
        readonly=True,
        help="Decimal amount as provided by Shopify, without float arithmetic.",
    )
    price_item_id = fields.Many2one(
        "product.pricelist.item",
        string="Shopify Pricelist Rule",
        readonly=True,
        ondelete="set null",
    )
    image_shopify_id = fields.Char(
        string="Variant Image Shopify GID",
        readonly=True,
        copy=False,
    )
    image_checksum = fields.Char(readonly=True, copy=False)

    _instance_odoo_unique = models.Constraint(
        "UNIQUE(instance_id, odoo_id)",
        "An Odoo variant can only be linked once per Shopify instance.",
    )

    @api.constrains("instance_id", "template_binding_id", "odoo_id")
    def _check_template_binding(self):
        for binding in self:
            if (
                binding.instance_id != binding.template_binding_id.instance_id
                or binding.odoo_id.product_tmpl_id
                != binding.template_binding_id.odoo_id
            ):
                raise ValidationError(
                    self.env._(
                        "A Shopify variant must belong to the same instance "
                        "and product as its template binding."
                    )
                )


class ShopifyProductImage(models.Model):
    _name = "shopify.product.image"
    _description = "Shopify Product Image Binding"
    _inherit = "shopify.binding.mixin"
    _order = "id"

    template_binding_id = fields.Many2one(
        "shopify.product.template",
        required=True,
        index=True,
        ondelete="cascade",
    )
    variant_binding_id = fields.Many2one(
        "shopify.product.variant",
        index=True,
        ondelete="set null",
    )
    variant_binding_ids = fields.Many2many(
        "shopify.product.variant",
        "shopify_product_image_variant_rel",
        "image_binding_id",
        "variant_binding_id",
        string="Associated Shopify Variants",
    )
    odoo_id = fields.Many2one(
        "product.image",
        string="Odoo Product Image",
        required=True,
        index=True,
        ondelete="cascade",
    )
    source_url = fields.Char(readonly=True)
    image_checksum = fields.Char(readonly=True, copy=False)

    _instance_odoo_unique = models.Constraint(
        "UNIQUE(instance_id, odoo_id)",
        "An Odoo image can only be linked once per Shopify instance.",
    )

    @api.constrains(
        "instance_id",
        "template_binding_id",
        "variant_binding_id",
        "variant_binding_ids",
        "odoo_id",
    )
    def _check_image_binding(self):
        for binding in self:
            if binding.instance_id != binding.template_binding_id.instance_id:
                raise ValidationError(
                    self.env._("An image and its product must use the same instance.")
                )
            if (
                binding.variant_binding_id
                and binding.variant_binding_id.template_binding_id
                != binding.template_binding_id
            ) or binding.variant_binding_ids.filtered(
                lambda variant, binding=binding: (
                    variant.template_binding_id != binding.template_binding_id
                )
            ):
                raise ValidationError(
                    self.env._("The image variant must belong to the bound product.")
                )
            image_template = (
                binding.odoo_id.product_tmpl_id
                or binding.odoo_id.product_variant_id.product_tmpl_id
            )
            if image_template != binding.template_binding_id.odoo_id:
                raise ValidationError(
                    self.env._("The Odoo image must belong to the bound product.")
                )
