The core Shopify connector links any number of Shopify stores to Odoo 19
Community through company-scoped binding records. It synchronizes products,
inventory, customers, orders, returns, refunds, and fulfillment through the
GraphQL Admin API.

Signed webhooks provide the fast path, OCA `queue_job` provides durable
execution, and scheduled reconciliation repairs missed or delayed events.
Onboarding, health checks, a sync dashboard, error recovery, and configurable
retention support day-to-day operation.

Product images cover the main image of each product and the images of its
variants. Synchronizing the other Shopify product media needs the glue module
Shopify Connector Website Sale, which installs automatically with eCommerce.
