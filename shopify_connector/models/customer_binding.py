# pylint: disable=consider-merging-classes-inherited

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ShopifyCustomer(models.Model):
    _name = "shopify.customer"
    _description = "Shopify Customer Binding"
    _inherit = "shopify.binding.mixin"
    _order = "id desc"
    _check_company_auto = True

    odoo_id = fields.Many2one(
        "res.partner",
        string="Odoo Customer",
        required=True,
        index=True,
        check_company=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    email_marketing_state = fields.Char(
        readonly=True,
    )
    tags = fields.Text(readonly=True)
    tax_exempt = fields.Boolean(readonly=True)
    address_binding_ids = fields.One2many(
        "shopify.customer.address",
        "customer_binding_id",
        string="Shopify Addresses",
    )
    tag_category_ids = fields.Many2many(
        "res.partner.category",
        "shopify_customer_category_rel",
        "customer_binding_id",
        "category_id",
        string="Imported Shopify Tags",
        readonly=True,
    )

    _instance_partner_unique = models.Constraint(
        "UNIQUE(instance_id, odoo_id)",
        "An Odoo customer can only be linked once per Shopify instance.",
    )

    @api.constrains("instance_id", "odoo_id")
    def _check_customer_company(self):
        for binding in self:
            if (
                binding.odoo_id.company_id
                and binding.odoo_id.company_id != binding.instance_id.company_id
            ):
                raise ValidationError(
                    self.env._(
                        "The customer must be shared or belong to the "
                        "Shopify instance company."
                    )
                )


class ShopifyCustomerAddress(models.Model):
    _name = "shopify.customer.address"
    _description = "Shopify Customer Address Binding"
    _inherit = "shopify.binding.mixin"
    _order = "is_default desc, id"
    _check_company_auto = True

    customer_binding_id = fields.Many2one(
        "shopify.customer",
        required=True,
        index=True,
        ondelete="cascade",
    )
    odoo_id = fields.Many2one(
        "res.partner",
        string="Odoo Address",
        required=True,
        index=True,
        check_company=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    is_default = fields.Boolean(readonly=True)

    _instance_partner_unique = models.Constraint(
        "UNIQUE(instance_id, odoo_id)",
        "An Odoo address can only be linked once per Shopify instance.",
    )

    @api.constrains("instance_id", "customer_binding_id", "odoo_id")
    def _check_address_scope(self):
        for binding in self:
            if (
                binding.customer_binding_id.instance_id != binding.instance_id
                or binding.odoo_id.parent_id != binding.customer_binding_id.odoo_id
                or binding.odoo_id.company_id != binding.instance_id.company_id
            ):
                raise ValidationError(
                    self.env._("Customer addresses must belong to the bound customer.")
                )


class ShopifyCompany(models.Model):
    _name = "shopify.company"
    _description = "Shopify B2B Company Binding"
    _inherit = "shopify.binding.mixin"
    _order = "id desc"
    _check_company_auto = True

    odoo_id = fields.Many2one(
        "res.partner",
        string="Odoo Company",
        required=True,
        index=True,
        check_company=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    external_id = fields.Char(string="Shopify External ID", readonly=True)
    location_binding_ids = fields.One2many(
        "shopify.company.location",
        "company_binding_id",
        string="Company Locations",
    )
    contact_binding_ids = fields.One2many(
        "shopify.company.contact",
        "company_binding_id",
        string="Company Contacts",
    )

    _instance_partner_unique = models.Constraint(
        "UNIQUE(instance_id, odoo_id)",
        "An Odoo company can only be linked once per Shopify instance.",
    )

    @api.constrains("instance_id", "odoo_id")
    def _check_b2b_company_scope(self):
        for binding in self:
            if (
                binding.odoo_id.company_id != binding.instance_id.company_id
                or not binding.odoo_id.is_company
            ):
                raise ValidationError(
                    self.env._("The B2B company must belong to the instance company.")
                )


class ShopifyCompanyLocation(models.Model):
    _name = "shopify.company.location"
    _description = "Shopify B2B Company Location Binding"
    _inherit = "shopify.binding.mixin"
    _order = "id"
    _check_company_auto = True

    company_binding_id = fields.Many2one(
        "shopify.company",
        required=True,
        index=True,
        ondelete="cascade",
    )
    odoo_id = fields.Many2one(
        "res.partner",
        string="Odoo Company Location",
        required=True,
        index=True,
        check_company=True,
        ondelete="cascade",
    )
    billing_odoo_id = fields.Many2one(
        "res.partner",
        string="Odoo Billing Address",
        check_company=True,
        ondelete="set null",
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    @api.constrains("instance_id", "company_binding_id", "odoo_id", "billing_odoo_id")
    def _check_b2b_location_scope(self):
        for binding in self:
            if (
                binding.company_binding_id.instance_id != binding.instance_id
                or binding.odoo_id.parent_id != binding.company_binding_id.odoo_id
                or (
                    binding.billing_odoo_id
                    and binding.billing_odoo_id.parent_id
                    != binding.company_binding_id.odoo_id
                )
            ):
                raise ValidationError(
                    self.env._("The B2B location must belong to its bound company.")
                )


class ShopifyCompanyContact(models.Model):
    _name = "shopify.company.contact"
    _description = "Shopify B2B Company Contact Binding"
    _inherit = "shopify.binding.mixin"
    _order = "id"
    _check_company_auto = True

    company_binding_id = fields.Many2one(
        "shopify.company",
        required=True,
        index=True,
        ondelete="cascade",
    )
    odoo_id = fields.Many2one(
        "res.partner",
        string="Odoo Company Contact",
        required=True,
        index=True,
        check_company=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    customer_shopify_id = fields.Char(readonly=True, index=True)
    title = fields.Char(readonly=True)
    roles = fields.Text(readonly=True)

    @api.constrains("instance_id", "company_binding_id", "odoo_id")
    def _check_b2b_contact_scope(self):
        for binding in self:
            if (
                binding.company_binding_id.instance_id != binding.instance_id
                or binding.odoo_id.parent_id != binding.company_binding_id.odoo_id
            ):
                raise ValidationError(
                    self.env._("The B2B contact must belong to its bound company.")
                )


class ShopifyCatalog(models.Model):
    _name = "shopify.catalog"
    _description = "Shopify B2B Catalog Binding"
    _inherit = "shopify.binding.mixin"
    _order = "id desc"
    _check_company_auto = True

    title = fields.Char(required=True)
    status = fields.Char(readonly=True)
    price_list_shopify_id = fields.Char(
        string="Shopify Price List GID",
        readonly=True,
        index=True,
    )
    odoo_pricelist_id = fields.Many2one(
        "product.pricelist",
        required=True,
        check_company=True,
        ondelete="restrict",
    )
    company_id = fields.Many2one(
        "res.company",
        related="instance_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )

    _instance_pricelist_unique = models.Constraint(
        "UNIQUE(instance_id, odoo_pricelist_id)",
        "An Odoo pricelist can only be linked once per Shopify instance.",
    )


class ResPartnerCategoryShopify(models.Model):
    _inherit = "res.partner.category"

    shopify_company_id = fields.Many2one(
        "res.company",
        index=True,
        ondelete="cascade",
        help="Company scope for categories created from Shopify tags.",
    )

    _shopify_company_name_unique = models.Constraint(
        "UNIQUE(name, shopify_company_id)",
        "A Shopify tag category must be unique per company.",
    )


class ShopifyInstanceCustomerConfig(models.Model):
    _inherit = "shopify.instance"

    customer_export_enabled = fields.Boolean(
        string="Export Odoo Customers",
        default=False,
        help="Export changes for linked customers when Odoo owns the field.",
    )
    guest_partner_id = fields.Many2one(
        "res.partner",
        string="Shopify Guest Customer",
        readonly=True,
        check_company=True,
        ondelete="restrict",
    )
    b2b_import_enabled = fields.Boolean(
        string="Import Shopify B2B",
        default=True,
    )
    shopify_plus_state = fields.Selection(
        [
            ("unknown", "Not Checked"),
            ("available", "Shopify Plus Available"),
            ("unavailable", "Shopify Plus Unavailable"),
        ],
        required=True,
        default="unknown",
        readonly=True,
    )
    customer_binding_ids = fields.One2many(
        "shopify.customer", "instance_id", string="Customers"
    )
    company_binding_ids = fields.One2many(
        "shopify.company", "instance_id", string="B2B Companies"
    )
    catalog_binding_ids = fields.One2many(
        "shopify.catalog", "instance_id", string="B2B Catalogs"
    )

    @api.model_create_multi
    def create(self, vals_list):
        instances = super().create(vals_list)
        for instance in instances:
            if not instance.guest_partner_id:
                guest = (
                    self.env["res.partner"]
                    .sudo()
                    .create(
                        {
                            "name": self.env._("Shopify Guest - %s", instance.name),
                            "company_id": instance.company_id.id,
                            "is_company": False,
                            "customer_rank": 1,
                        }
                    )
                )
                instance.sudo().guest_partner_id = guest
        return instances

    def write(self, values):
        if "company_id" in values and any(
            instance.company_id.id != values["company_id"] for instance in self
        ):
            self.ensure_one()
            company = self.env["res.company"].browse(values["company_id"])
            guest = (
                self.env["res.partner"]
                .sudo()
                .create(
                    {
                        "name": self.env._(
                            "Shopify Guest - %s", (values.get("name") or self.name)
                        ),
                        "company_id": company.id,
                        "is_company": False,
                        "customer_rank": 1,
                    }
                )
            )
            values = {**values, "guest_partner_id": guest.id}
        return super().write(values)

    @api.constrains("company_id", "guest_partner_id")
    def _check_guest_partner_company(self):
        for instance in self:
            if (
                instance.guest_partner_id
                and instance.guest_partner_id.company_id != instance.company_id
            ):
                raise ValidationError(
                    self.env._(
                        "The guest customer must belong to the instance company."
                    )
                )
