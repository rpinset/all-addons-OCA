from odoo import fields, models


class ShopifyBindingMixin(models.AbstractModel):
    _name = "shopify.binding.mixin"
    _description = "Shopify Binding Mixin"

    instance_id = fields.Many2one(
        "shopify.instance",
        string="Shopify Instance",
        required=True,
        index=True,
        ondelete="cascade",
    )
    shopify_id = fields.Char(
        string="Shopify GID",
        required=True,
        index=True,
        help="Stable Shopify GraphQL global ID.",
    )
    external_updated_at = fields.Datetime(
        string="Shopify Updated At",
        help="UTC update timestamp last reported by Shopify.",
    )
    last_sync_date = fields.Datetime(
        string="Last Synchronization",
        readonly=True,
        help="UTC timestamp of the last successful synchronization.",
    )
    state = fields.Selection(
        [
            ("pending", "Pending"),
            ("synced", "Synchronized"),
            ("error", "Error"),
        ],
        required=True,
        default="pending",
        index=True,
    )
    error_message = fields.Text(readonly=True)

    _instance_gid_unique = models.Constraint(
        "UNIQUE(instance_id, shopify_id)",
        "A Shopify ID can only be bound once per instance.",
    )
