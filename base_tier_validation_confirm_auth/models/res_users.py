# Copyright 2026 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from functools import wraps

from odoo import _
from odoo.exceptions import UserError
from odoo.http import request


def _jsonable(o):
    try:
        json.dumps(o)
    except TypeError:
        return False
    else:
        return True


def check_authentication(fn):
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
        if not request:
            raise UserError(_("This method can only be accessed over HTTP"))

        if self.env.context.get("identity_checked"):
            return fn(self, *args, **kwargs)

        ctx = self.env.context.copy()
        ctx["identity_checked"] = True

        safe_context = {k: v for k, v in ctx.items() if _jsonable(v)}

        w = (
            self.sudo()
            .env["res.users.identitycheck"]
            .create(
                {
                    "request": json.dumps(
                        [safe_context, self._name, self.ids, fn.__name__, args, kwargs]
                    )
                }
            )
        )

        return {
            "type": "ir.actions.act_window",
            "res_model": "res.users.identitycheck",
            "res_id": w.id,
            "name": _("Security Control"),
            "target": "new",
            "views": [(False, "form")],
        }

    wrapped.__has_check_identity = True
    return wrapped
