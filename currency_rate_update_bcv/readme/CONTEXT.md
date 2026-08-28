Venezuelan companies need the official BCV rate to value foreign-currency
documents. The BCV publishes that rate on its public website, not through a
stable API.

This module is the OCA provider for that source. It must live in
``l10n-venezuela`` because it is country-specific, not a generic currency
connector.
