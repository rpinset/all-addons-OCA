Base module of the Mautic connector suite. It provides only the connection
to a Mautic instance:

- the `mautic.backend` model, holding the connection settings (Mautic URL,
  OAuth2 Client ID / Secret),
- the OAuth2 authorization flow (connect, callback, automatic token
  refresh),
- a *Test Connection* action to verify the credentials are still valid.

This module does not synchronize any business data by itself. It is meant
to be extended by future modules (contacts, tags, segments, ...) that will
depend on it.
