# pylint: disable=consider-merging-classes-inherited

from odoo import api, fields, models
from odoo.exceptions import ValidationError

PRODUCT_FIELDS = (
    ("name", "Name"),
    ("description", "Description"),
    ("price", "Price"),
    ("images", "Images"),
    ("status", "Status"),
    ("customer_name", "Customer Name"),
    ("customer_email", "Customer Email"),
    ("customer_phone", "Customer Phone"),
    ("customer_addresses", "Customer Addresses"),
)

DEFAULT_PRODUCT_FIELD_OWNERS = {
    "name": "odoo",
    "description": "odoo",
    "price": "odoo",
    "images": "odoo",
    "status": "shopify",
}

DEFAULT_CUSTOMER_FIELD_OWNERS = {
    "customer_name": "shopify",
    "customer_email": "shopify",
    "customer_phone": "shopify",
    "customer_addresses": "shopify",
}


class ShopifyFieldMapping(models.Model):
    _name = "shopify.field.mapping"
    _description = "Shopify Field Ownership"
    _order = "field"

    instance_id = fields.Many2one(
        "shopify.instance",
        required=True,
        index=True,
        ondelete="cascade",
    )
    field = fields.Selection(PRODUCT_FIELDS, required=True, index=True)
    owner = fields.Selection(
        [("odoo", "Odoo"), ("shopify", "Shopify")],
        required=True,
        default="odoo",
    )

    _instance_field_unique = models.Constraint(
        "UNIQUE(instance_id, field)",
        "Each synchronized field can only be configured once per instance.",
    )


class ShopifyInstance(models.Model):
    _inherit = "shopify.instance"

    field_mapping_ids = fields.One2many(
        "shopify.field.mapping",
        "instance_id",
        string="Product Field Ownership",
        copy=True,
    )
    product_create_if_missing = fields.Boolean(
        string="Create Missing Odoo Products",
        default=True,
        help="Create an Odoo product when no barcode or SKU match exists.",
    )
    product_delete_behavior = fields.Selection(
        [("archive", "Archive in Odoo"), ("ignore", "Keep Active in Odoo")],
        string="Shopify Product Deletion",
        required=True,
        default="archive",
    )
    product_pricelist_id = fields.Many2one(
        "product.pricelist",
        string="Shopify Product Pricelist",
        required=True,
        check_company=True,
        ondelete="restrict",
        help=(
            "Variant-specific Shopify prices are stored as fixed-price "
            "rules on this pricelist."
        ),
    )
    shop_currency_id = fields.Many2one(
        "res.currency",
        string="Shopify Shop Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
        readonly=True,
    )
    _product_pricelist_unique = models.Constraint(
        "UNIQUE(product_pricelist_id)",
        "Each Shopify instance must use its own product pricelist.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            company = self.env["res.company"].browse(
                values.get("company_id") or self.env.company.id
            )
            values.setdefault("shop_currency_id", company.currency_id.id)
            if not values.get("product_pricelist_id"):
                pricelist = (
                    self.env["product.pricelist"]
                    .sudo()
                    .create(
                        {
                            "name": f"Shopify - {values.get('name') or 'Shop'}",
                            "currency_id": company.currency_id.id,
                            "company_id": company.id,
                        }
                    )
                )
                values["product_pricelist_id"] = pricelist.id
        instances = super().create(vals_list)
        mapping_model = self.env["shopify.field.mapping"].sudo()
        for instance in instances:
            configured = set(instance.field_mapping_ids.mapped("field"))
            values = [
                {
                    "instance_id": instance.id,
                    "field": field_name,
                    "owner": owner,
                }
                for field_name, owner in {
                    **DEFAULT_PRODUCT_FIELD_OWNERS,
                    **DEFAULT_CUSTOMER_FIELD_OWNERS,
                }.items()
                if field_name not in configured
            ]
            if values:
                mapping_model.create(values)
            if not instance.product_pricelist_id:
                pricelist = (
                    self.env["product.pricelist"]
                    .sudo()
                    .create(
                        {
                            "name": f"Shopify - {instance.name}",
                            "currency_id": instance.company_id.currency_id.id,
                            "company_id": instance.company_id.id,
                        }
                    )
                )
                instance.sudo().product_pricelist_id = pricelist
        return instances

    def write(self, values):
        company_changed = "company_id" in values and any(
            instance.company_id.id != values["company_id"] for instance in self
        )
        shop_changed = "shop_url" in values and any(
            instance.shop_url != values["shop_url"] for instance in self
        )
        if company_changed or shop_changed:
            synchronized = self.filtered(
                lambda instance: (
                    self.env["shopify.product.template"].search_count(
                        [("instance_id", "=", instance.id)], limit=1
                    )
                    or self.env["shopify.collection"].search_count(
                        [("instance_id", "=", instance.id)], limit=1
                    )
                    or self.env["shopify.location"].search_count(
                        [("instance_id", "=", instance.id)], limit=1
                    )
                    or self.env["shopify.customer"].search_count(
                        [("instance_id", "=", instance.id)], limit=1
                    )
                    or self.env["shopify.company"].search_count(
                        [("instance_id", "=", instance.id)], limit=1
                    )
                    or self.env["shopify.order"].search_count(
                        [("instance_id", "=", instance.id)], limit=1
                    )
                )
            )
            if synchronized:
                raise ValidationError(
                    self.env._(
                        "You cannot change the company or shop domain of an "
                        "instance after synchronized records have been created."
                    )
                )
        if company_changed:
            self.ensure_one()
            company = self.env["res.company"].browse(values["company_id"])
            pricelist = (
                self.env["product.pricelist"]
                .sudo()
                .create(
                    {
                        "name": f"Shopify - {self.name}",
                        "currency_id": company.currency_id.id,
                        "company_id": company.id,
                    }
                )
            )
            values = {**values, "product_pricelist_id": pricelist.id}
        if company_changed or shop_changed:
            company = self.env["res.company"].browse(
                values.get("company_id") or self.company_id.id
            )
            values = {
                **values,
                "state": "draft",
                "shop_currency_id": company.currency_id.id,
            }
        result = super().write(values)
        if shop_changed and not company_changed:
            self.product_pricelist_id.sudo().currency_id = self.company_id.currency_id
        return result

    @api.constrains("company_id", "product_pricelist_id")
    def _check_product_pricelist_company(self):
        for instance in self:
            if (
                instance.product_pricelist_id
                and instance.product_pricelist_id.company_id != instance.company_id
            ):
                raise ValidationError(
                    self.env._(
                        "The Shopify pricelist must belong to the instance company."
                    )
                )

    def _product_field_owners(self):
        self.ensure_one()
        owners = dict(DEFAULT_PRODUCT_FIELD_OWNERS)
        owners.update(
            {
                mapping.field: mapping.owner
                for mapping in self.field_mapping_ids
                if mapping.field in DEFAULT_PRODUCT_FIELD_OWNERS
            }
        )
        return owners

    def _is_product_field_owned_by(self, field_name, owner):
        self.ensure_one()
        return self._product_field_owners().get(field_name) == owner

    def _customer_field_owners(self):
        self.ensure_one()
        owners = dict(DEFAULT_CUSTOMER_FIELD_OWNERS)
        owners.update(
            {
                mapping.field: mapping.owner
                for mapping in self.field_mapping_ids
                if mapping.field in DEFAULT_CUSTOMER_FIELD_OWNERS
            }
        )
        return owners

    def _is_customer_field_owned_by(self, field_name, owner):
        self.ensure_one()
        return self._customer_field_owners().get(field_name) == owner
