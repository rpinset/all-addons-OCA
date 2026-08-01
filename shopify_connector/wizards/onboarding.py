from decimal import Decimal

from odoo import api, fields, models

from odoo.addons.queue_job.delay import chain

from ..graphql import (
    CURRENT_APP_SCOPES_QUERY,
    SHOP_TAX_SETTINGS_QUERY,
)
from ..lib.operability import missing_scopes, scope_handles

REQUIRED_ADMIN_SCOPES = (
    "read_customers",
    "read_draft_orders",
    "read_inventory",
    "read_locations",
    "read_merchant_managed_fulfillment_orders",
    "read_orders",
    "read_products",
    "write_customers",
    "write_inventory",
    "write_merchant_managed_fulfillment_orders",
    "write_products",
)


class ShopifyInstanceWizard(models.TransientModel):
    _name = "shopify.instance.wizard"
    _description = "Shopify Instance Onboarding"

    step = fields.Selection(
        [
            ("credentials", "Credentials"),
            ("scopes", "API Scopes"),
            ("locations", "Locations"),
            ("taxes", "Tax Defaults"),
            ("policies", "Policies"),
            ("webhooks", "Webhooks"),
            ("imports", "Initial Import"),
        ],
        required=True,
        default="credentials",
    )
    instance_id = fields.Many2one(
        "shopify.instance",
        readonly=True,
        ondelete="cascade",
    )
    name = fields.Char(required=True, default="Shopify Store")
    shop_url = fields.Char(required=True)
    access_token = fields.Char(required=True)
    webhook_secret = fields.Char(required=True)
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    required_scopes = fields.Text(readonly=True)
    granted_scopes = fields.Text(readonly=True)
    missing_scopes = fields.Text(readonly=True)
    scope_check_ok = fields.Boolean(readonly=True)
    location_line_ids = fields.One2many(
        "shopify.instance.wizard.location",
        "wizard_id",
        string="Location Mappings",
    )
    taxes_included = fields.Boolean(readonly=True)
    tax_shipping = fields.Boolean(readonly=True)
    tax_country_id = fields.Many2one("res.country", readonly=True)
    tax_mapping_count = fields.Integer(readonly=True)
    order_confirmation_policy = fields.Selection(
        [
            ("quotation", "Import as Quotation"),
            ("auto", "Auto-confirm Eligible"),
        ],
        required=True,
        default="quotation",
    )
    order_invoicing_policy = fields.Selection(
        [
            ("manual", "Manual"),
            ("paid", "Invoice on Paid"),
            ("fulfillment", "Invoice on Fulfillment"),
        ],
        required=True,
        default="manual",
    )
    product_create_if_missing = fields.Boolean(default=True)
    inventory_quantity_basis = fields.Selection(
        [
            ("free_qty", "Free Quantity"),
            ("qty_available", "On-hand Quantity"),
        ],
        required=True,
        default="free_qty",
    )
    inventory_direction = fields.Selection(
        [
            ("odoo_to_shopify", "Odoo to Shopify"),
            ("bidirectional", "Odoo to Shopify + Shopify to Odoo"),
        ],
        string="Stock Direction",
        required=True,
        default="odoo_to_shopify",
    )
    import_products = fields.Boolean(default=True)
    import_customers = fields.Boolean(default=True)
    import_orders = fields.Boolean(default=True)

    @api.model
    def default_get(self, field_names):
        values = super().default_get(field_names)
        instance = (
            self.env["shopify.instance"]
            .browse(self.env.context.get("active_id"))
            .exists()
        )
        values["required_scopes"] = "\n".join(REQUIRED_ADMIN_SCOPES)
        if instance:
            values.update(
                {
                    "instance_id": instance.id,
                    "name": instance.name,
                    "shop_url": instance.shop_url,
                    "access_token": instance.access_token,
                    "webhook_secret": instance.webhook_secret,
                    "company_id": instance.company_id.id,
                    "order_confirmation_policy": (instance.order_confirmation_policy),
                    "order_invoicing_policy": (instance.order_invoicing_policy),
                    "product_create_if_missing": (instance.product_create_if_missing),
                    "inventory_quantity_basis": (instance.inventory_quantity_basis),
                    "inventory_direction": (
                        "bidirectional"
                        if instance.inventory_import_enabled
                        else "odoo_to_shopify"
                    ),
                }
            )
        return values

    def _reopen(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Shopify Onboarding"),
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

    def action_test_connection(self):
        self.ensure_one()
        values = {
            "name": self.name,
            "shop_url": self.shop_url,
            "access_token": self.access_token,
            "webhook_secret": self.webhook_secret,
            "company_id": self.company_id.id,
            "active": True,
        }
        if self.instance_id:
            self.instance_id.write(values)
        else:
            self.instance_id = self.env["shopify.instance"].create(values)
        self.instance_id.action_test_connection()
        self.step = "scopes"
        return self._reopen()

    def action_check_scopes(self):
        self.ensure_one()
        payload = self.instance_id._shopify_client().execute(CURRENT_APP_SCOPES_QUERY)
        granted = scope_handles(payload)
        missing = missing_scopes(granted, REQUIRED_ADMIN_SCOPES)
        self.write(
            {
                "granted_scopes": "\n".join(sorted(granted)),
                "missing_scopes": "\n".join(missing),
                "scope_check_ok": not missing,
            }
        )
        if missing:
            return self._reopen()
        self.instance_id._job_import_locations()
        self.location_line_ids.unlink()
        self.env["shopify.instance.wizard.location"].create(
            [
                {
                    "wizard_id": self.id,
                    "location_binding_id": location.id,
                    "warehouse_id": location.warehouse_id.id,
                    "odoo_location_id": location.odoo_location_id.id,
                }
                for location in self.instance_id.location_binding_ids.filtered("active")
            ]
        )
        self.step = "locations"
        return self._reopen()

    def action_apply_locations(self):
        self.ensure_one()
        for line in self.location_line_ids:
            line.location_binding_id.write(
                {
                    "warehouse_id": line.warehouse_id.id,
                    "odoo_location_id": line.odoo_location_id.id,
                }
            )
        tax_data = self.instance_id._shopify_client().execute(SHOP_TAX_SETTINGS_QUERY)
        shop = tax_data.get("shop") or {}
        country_code = (shop.get("shopAddress") or {}).get("countryCodeV2")
        country = self.env["res.country"].search([("code", "=", country_code)], limit=1)
        if not country:
            country = self.company_id.country_id
        self.write(
            {
                "taxes_included": bool(shop.get("taxesIncluded")),
                "tax_shipping": bool(shop.get("taxShipping")),
                "tax_country_id": country.id,
            }
        )
        self.tax_mapping_count = self._create_common_tax_mappings()
        self.step = "taxes"
        return self._reopen()

    def _create_common_tax_mappings(self):
        self.ensure_one()
        if not self.tax_country_id:
            return 0
        taxes = (
            self.env["account.tax"]
            .with_company(self.company_id)
            .search(
                [
                    ("company_id", "=", self.company_id.id),
                    ("type_tax_use", "=", "sale"),
                    ("amount_type", "=", "percent"),
                    ("price_include", "=", self.taxes_included),
                    ("active", "=", True),
                ]
            )
        )
        mapping_model = self.env["shopify.tax.mapping"]
        created = 0
        for tax in taxes:
            rate = format(
                (Decimal(str(tax.amount)) / Decimal("100")).normalize(),
                "f",
            )
            domain = [
                ("instance_id", "=", self.instance_id.id),
                ("rate", "=", rate),
                ("country_id", "=", self.tax_country_id.id),
                ("price_included", "=", self.taxes_included),
            ]
            if mapping_model.search_count(domain, limit=1):
                continue
            mapping_model.create(
                {
                    "instance_id": self.instance_id.id,
                    "rate": rate,
                    "country_id": self.tax_country_id.id,
                    "price_included": self.taxes_included,
                    "tax_id": tax.id,
                }
            )
            created += 1
        return created

    def action_continue_to_policies(self):
        self.ensure_one()
        self.step = "policies"
        return self._reopen()

    def action_apply_policies(self):
        self.ensure_one()
        self.instance_id.write(
            {
                "order_confirmation_policy": (self.order_confirmation_policy),
                "order_invoicing_policy": self.order_invoicing_policy,
                "product_create_if_missing": (self.product_create_if_missing),
                "inventory_quantity_basis": (self.inventory_quantity_basis),
                "inventory_import_enabled": (
                    self.inventory_direction == "bidirectional"
                ),
            }
        )
        self.step = "webhooks"
        return self._reopen()

    def action_setup_webhooks(self):
        self.ensure_one()
        self.instance_id.action_repair_webhook_subscriptions()
        self.step = "imports"
        return self._reopen()

    def action_finish(self):
        self.ensure_one()
        jobs = []
        identity_base = f"shopify.onboarding.{self.instance_id.id}.{self.id}"
        if self.import_products:
            jobs.append(
                self.instance_id.delayable()
                ._job_fetch_products_bulk()
                .set(
                    channel="root.shopify.import",
                    description=self.env._("Onboarding: import Shopify products"),
                    identity_key=f"{identity_base}.products",
                )
            )
        if self.import_customers:
            jobs.append(
                self.instance_id.delayable()
                ._job_fetch_customers_bulk()
                .set(
                    channel="root.shopify.import",
                    description=self.env._("Onboarding: import Shopify customers"),
                    identity_key=f"{identity_base}.customers",
                )
            )
        if self.import_orders:
            jobs.append(
                self.instance_id.delayable()
                ._job_fetch_orders_bulk(False, False)
                .set(
                    channel="root.shopify.import",
                    description=self.env._("Onboarding: import Shopify orders"),
                    identity_key=f"{identity_base}.orders",
                )
            )
        if jobs:
            (chain(*jobs) if len(jobs) > 1 else jobs[0]).delay()
        self.instance_id._write_log(
            entity="onboarding",
            direction="import",
            level="info",
            message=self.env._(
                "Onboarding completed; %(count)s initial import stages queued.",
                count=len(jobs),
            ),
            record=self.instance_id,
        )
        return {
            "type": "ir.actions.act_window",
            "name": self.instance_id.display_name,
            "res_model": "shopify.instance",
            "res_id": self.instance_id.id,
            "view_mode": "form",
            "target": "current",
        }


class ShopifyInstanceWizardLocation(models.TransientModel):
    _name = "shopify.instance.wizard.location"
    _description = "Shopify Onboarding Location Mapping"

    wizard_id = fields.Many2one(
        "shopify.instance.wizard",
        required=True,
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        "res.company",
        related="wizard_id.company_id",
        store=True,
        readonly=True,
    )
    location_binding_id = fields.Many2one(
        "shopify.location",
        required=True,
        readonly=True,
        ondelete="cascade",
    )
    location_name = fields.Char(
        related="location_binding_id.name",
        readonly=True,
    )
    warehouse_id = fields.Many2one(
        "stock.warehouse",
        check_company=True,
        ondelete="restrict",
    )
    odoo_location_id = fields.Many2one(
        "stock.location",
        check_company=True,
        domain="[('usage', '=', 'internal')]",
        ondelete="restrict",
    )

    @api.onchange("warehouse_id")
    def _onchange_warehouse_id(self):
        for line in self:
            if line.warehouse_id:
                line.odoo_location_id = line.warehouse_id.lot_stock_id
