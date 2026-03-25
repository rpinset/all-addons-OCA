This module provides an overridable request context for FastAPI endpoints.

It allows to customize the behavior of requests deep in the odoo call stack
according to the current request context without having to override routers
that may come from external modules.

This context contains by default the current endpoint app and id, respectively
accessible via `self.env.context.get('fastapi_endpoint_app')` and
`self.env.context.get('fastapi_endpoint_id')`.
