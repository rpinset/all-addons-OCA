odoo_env dependency is automatically overridden to include FastAPI endpoint context values.

You can override the `fastapi.endpoint`->`_get_app_context()` method to add custom values to the context for your applications.
