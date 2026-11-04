Connect an Odoo company to a Mercado Libre seller account.

This is the core of the connector. It stores the seller backend, authorizes the
application with OAuth 2.0, refreshes access tokens, and receives Mercado Libre
notifications. Listing, stock, and sale synchronization live in
`connector_mercadolibre_product` and `connector_mercadolibre_sale`.

A notification is stored and acknowledged in the HTTP request. The work runs afterwards
in an OCA queue job.
