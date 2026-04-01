============================
Base External System OdooRPC
============================

This module adds an *external system adapter* for connecting to another Odoo instance
using the Python ``odoorpc`` client (JSON-RPC).

It is built on top of ``base_external_system`` and implements a new adapter model:

* ``external.system.odoo`` (System Type: *External System RPC*)

The adapter supports:

* Validating required connection parameters (host, port, database, username, password)
* Optional SSL transport (JSON-RPC over SSL)
* A context-managed client lifecycle via the ``base_external_system`` adapter contract
  (open client, perform calls, logout/cleanup)

Typical use cases include:

* Reading data from a legacy Odoo (e.g. Odoo 8/9/10) into a newer Odoo (e.g. Odoo 16)
* Synchronizations, migrations, or import tools that must query remote models
  (e.g. ``stock.production.lot``, ``stock.move``, ``res.partner``) via RPC
