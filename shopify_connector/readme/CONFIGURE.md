1. Add OCA `queue_job` and this repository to the Odoo addons path, then
   install **Shopify Connector**.
2. Grant operators the **Shopify Manager** group.
3. Open **Shopify > Configuration > Instances** and start onboarding.
4. Enter the custom-app domain, Admin API token, and webhook signing secret.
5. Correct any missing scopes, map Shopify locations, review generated tax
   mappings, choose synchronization policies, and install webhooks.
6. Review payment-gateway and carrier mappings before enabling unattended
   order and fulfillment processing.

Configure `queue_job` worker capacities in `odoo.conf`; the repository README
contains a safe starting allocation for import, export, and webhook channels.
