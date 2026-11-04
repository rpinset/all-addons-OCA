Open **Mercado Libre / Operations / Notifications** to see the callbacks Mercado Libre
has posted. Each row is dispatched by a job on the `root.mercadolibre.webhook` channel.

A topic with no installed handler is marked **Skipped**. Installing a later addon adds a
handler component; the controller stays unchanged.

**Refresh token** on the backend asks Mercado Libre for a new access token immediately.
**Disconnect** deletes the stored tokens.
