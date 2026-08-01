try:
    import odoo  # noqa: F401
except ModuleNotFoundError as exc:
    if exc.name != "odoo":
        raise
else:
    from . import models
