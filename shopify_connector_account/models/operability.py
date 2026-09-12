from odoo import models


class ShopifyPayoutRetryOperations(models.Model):
    _inherit = "shopify.payout"

    def _shopify_enqueue_fresh_retry(self):
        self.ensure_one()
        if not self.instance_id.active:
            return False
        self.instance_id.with_delay(
            **self._shopify_retry_options()
        )._job_import_payouts()
        return True


class ShopifyDisputeRetryOperations(models.Model):
    _inherit = "shopify.dispute"

    def _shopify_enqueue_fresh_retry(self):
        self.ensure_one()
        if not self.instance_id.active:
            return False
        self.instance_id.with_delay(
            **self._shopify_retry_options()
        )._job_import_payouts()
        return True
