from datetime import timedelta

from odoo import api, fields, models


class ShopifyLog(models.Model):
    _name = "shopify.log"
    _description = "Shopify Synchronization Log"
    _order = "create_date desc, id desc"

    instance_id = fields.Many2one(
        "shopify.instance",
        required=True,
        index=True,
        ondelete="cascade",
    )
    entity = fields.Char(required=True, index=True)
    direction = fields.Selection(
        [("import", "Shopify to Odoo"), ("export", "Odoo to Shopify")],
        required=True,
        index=True,
    )
    level = fields.Selection(
        [("info", "Info"), ("warning", "Warning"), ("error", "Error")],
        required=True,
        default="info",
        index=True,
    )
    message = fields.Text(required=True)
    res_model = fields.Char(string="Related Document Model", index=True)
    res_id = fields.Integer(string="Related Document ID", index=True)

    @api.autovacuum
    def _gc_shopify_logs(self):
        self._prune_old_logs()

    @api.model
    def _cron_prune(self):
        return self._prune_old_logs()

    @api.model
    def _prune_old_logs(self):
        count = 0
        instances = (
            self.env["shopify.instance"]
            .sudo()
            .with_context(active_test=False)
            .search([("id", "!=", False)])
        )
        for instance in instances:
            cutoff = fields.Datetime.now() - timedelta(days=instance.log_retention_days)
            old_logs = self.sudo().search(
                [
                    ("instance_id", "=", instance.id),
                    ("create_date", "<", cutoff),
                ]
            )
            count += len(old_logs)
            old_logs.unlink()
        return count
