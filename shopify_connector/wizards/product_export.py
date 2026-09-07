from odoo import fields, models
from odoo.exceptions import UserError


class ShopifyProductExportWizard(models.TransientModel):
    _name = "shopify.product.export.wizard"
    _description = "Export Products to Shopify"

    instance_id = fields.Many2one(
        "shopify.instance",
        required=True,
    )
    product_tmpl_ids = fields.Many2many(
        "product.template",
        string="Products",
        required=True,
    )

    def action_export(self):
        self.ensure_one()
        if self.instance_id.state != "connected":
            raise UserError(
                self.env._("Connect the Shopify instance before exporting.")
            )
        invalid_products = self.product_tmpl_ids.filtered(
            lambda template: template.company_id != self.instance_id.company_id
        )
        if invalid_products:
            raise UserError(
                self.env._("All exported products must belong to the instance company.")
            )
        for template in self.product_tmpl_ids:
            self.env["shopify.product.template"]._enqueue_product_export(
                self.instance_id, template
            )
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": self.env._("Product export queued"),
                "message": self.env._(
                    "%s product(s) queued for Shopify export.",
                    len(self.product_tmpl_ids),
                ),
                "type": "success",
                "sticky": False,
            },
        }
