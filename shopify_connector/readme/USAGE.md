Use **Shopify > Dashboard** to monitor binding states, queue backlog, recent
errors, webhook health, drift schedules, and operational table sizes.

Normal changes flow through webhooks and idempotent jobs. Use the entity import
or reconcile actions for manual catch-up. For failures, correct the underlying
configuration or data, select error bindings, and choose **Retry Failed
Shopify Bindings**. Resetting to pending clears the state without scheduling
work.

Run **Check Webhooks** after changing domains or credentials and repair any
missing or misrouted subscriptions. Never edit Shopify IDs or raw payloads.
