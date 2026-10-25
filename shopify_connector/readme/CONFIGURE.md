**Shopify app**

Since January 1, 2026, Shopify no longer lets merchants create legacy custom
apps from the Shopify admin. Create the app in the Shopify Dev Dashboard:

1. Open the Dev Dashboard of the organization that owns the store. Odoo gets
   its access tokens with the client credentials grant, which only works when
   the app and the store belong to the same organization. Owning the store or
   installing the app on it is not enough. For a test store, create it from
   the **Dev stores** page of that same Dev Dashboard.
2. Create the app and fill in its version. The connector has no page in the
   Shopify admin and never sends users through Shopify's authorization pages,
   so:
   - **App URL**: `https://shopify.dev/apps/default-app-home`, the default
     Shopify gives for apps that are not embedded.
   - **Embed app in Shopify admin**: unchecked.
   - **Allowed redirection URL(s)**: none. If Shopify asks for one, enter the
     App URL again.
   - **Use legacy install flow**: unchecked, so that installing the app
     grants the scopes selected on the version. With the legacy flow the app
     would have to request them itself, which the connector cannot do.
   - **Webhooks**: none. Odoo creates its own subscriptions during
     onboarding.
   - **Webhooks API version**: `2026-01`, the Admin API version the
     connector uses. Shopify writes the payloads of the subscriptions Odoo
     creates in this version.
   - **Scopes**: `read_customers`, `write_customers`, `read_draft_orders`,
     `read_fulfillments`, `read_inventory`, `write_inventory`,
     `read_locations`, `read_merchant_managed_fulfillment_orders`,
     `write_merchant_managed_fulfillment_orders`, `read_orders`,
     `read_products`, `write_products` and `read_returns`. To import orders
     older than 60 days, also select `read_all_orders`, which Shopify may
     have to approve.
3. Release the version and install the app on the store. After a later
   scope change, release a new version and approve the change on the store.
4. Copy the client ID and the client secret from the app's **Settings** page.

The app must have access to protected customer data: names, addresses,
emails and phone numbers. For merchant-created apps this depends on the
store's plan, and the Basic plan does not include it. Without it, Shopify
refuses some of the order webhooks and the order and customer imports fail.

A legacy custom app created before 2026 keeps working. Leave the client ID
empty and enter the app's Admin API access token and API secret key instead.

**Odoo**

1. Add OCA `queue_job` and this repository to the Odoo addons path, then
   install **Shopify Connector**.
2. Grant operators the **Shopify Manager** group. The administrator gets it
   on install.
3. Set the `web.base.url` system parameter to a public HTTPS address of Odoo,
   and set `web.base.url.freeze` to `True` so that it does not change when an
   administrator logs in from another address. Shopify sends its webhooks to
   `<web.base.url>/shopify/webhook/<instance id>` and downloads exported
   product images from the same address.
4. Open **Shopify > Configuration > Instances** and click **Start
   Onboarding**:
   - **Credentials**: enter the `<store>.myshopify.com` domain, the client ID
     and the client secret, then **Test Connection**. Odoo requests the
     access token and renews it before it expires, every 24 hours. The client
     secret also verifies the webhook signatures.
   - **API Scopes**: add any missing scope to a new app version, release it,
     approve the change on the store and check again.
   - Map the Shopify locations, review the generated tax mappings, choose the
     synchronization policies, install the webhooks and queue the initial
     imports.
5. Review the payment-gateway and carrier mappings before enabling unattended
   order and fulfillment processing.

Jobs run on the `root.shopify.import`, `root.shopify.export` and
`root.shopify.webhook` channels. Add `queue_job` to the server-wide modules,
after the Odoo defaults `base,rpc,web`, and give each channel a capacity in
`odoo.conf`, for example:

``` ini
[options]
server_wide_modules = base,rpc,web,queue_job

[queue_job]
channels = root:4,root.shopify.import:2,root.shopify.export:1,root.shopify.webhook:1
```
