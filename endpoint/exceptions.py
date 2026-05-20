# Copyright 2026 Camptocamp SA (https://www.camptocamp.com).
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json

import werkzeug.exceptions
import werkzeug.wrappers


class RequestValidationError(werkzeug.exceptions.BadRequest):
    """Bad request raised when the body fails JSON Schema validation.

    Emits ``{"detail": [{"loc", "msg", "type"}, ...]}`` (FastAPI-style)
    instead of the generic werkzeug HTML body.
    """

    def __init__(self, detail):
        super().__init__()
        self.detail = detail

    def get_response(self, environ=None, scope=None):
        return werkzeug.wrappers.Response(
            json.dumps({"detail": self.detail}),
            status=self.code,
            mimetype="application/json",
        )
