1.  Create an application in Mercado Libre (My Applications) with write scope and a
    redirect URI that points at this database, for example
    `https://example.com/mercadolibre/oauth/callback`.
2.  Set the notification callback to
    `https://example.com/mercadolibre/notification/<backend-database-id>`. Subscribe the
    topics the installed addons handle. The core stores every topic; product and sale
    addons consume `items`, `stock-location`, `orders_v2`, `shipments`, and `payments`.
3.  Grant operators **Mercado Libre / User** and administrators **Mercado Libre /
    Manager**.
4.  Open **Mercado Libre / Configuration / Backends**, create a backend, set the
    company, the site (`MLA`, `MLB`, `MLM`, …), the client id, the client secret, and
    the redirect URI.
5.  Click **Connect** and authorize the seller. The backend stores the seller id
    returned by `/users/me` and the token pair.
6.  A scheduled action refreshes the access token before the six-hour expiry. When
    Mercado Libre rejects the refresh token, the backend moves to **Error** and an
    administrator reconnects the seller.
