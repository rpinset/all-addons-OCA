Test connection (UI)


Open an external system record configured with System Type *External System RPC*
and click the *Test Connection* button.

If successful, the adapter will report success (using the success mechanism
provided by ``base_external_system``).

Using the client in code


Use the standard context manager from ``base_external_system``::

    system = self.env.ref("your_module.external_system_odoo_remote")
    with system.client() as odoo:
        partner_model = odoo.env["res.partner"]
        ids = partner_model.search([("is_company", "=", True)], limit=10)
        data = partner_model.read(ids, ["name"])

The yielded object is an ``odoorpc.ODOO`` client instance, so any remote model can be
accessed via ``odoo.env["model.name"]``.

Legacy helper (optional)


Some projects historically called a helper directly on the adapter record::

    odoo = system.interface._connect()

If your adapter keeps that helper for backward compatibility, it returns the same
client object as ``external_get_client()``.
