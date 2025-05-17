# Copyright 2018 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from psycopg2 import errorcodes
from psycopg2.errors import OperationalError
from werkzeug.exceptions import MethodNotAllowed

from odoo import _
from odoo.exceptions import (
    AccessDenied,
    AccessError,
    MissingError,
    UserError,
    ValidationError,
)
from odoo.http import SessionExpiredException
from odoo.service.model import MAX_TRIES_ON_CONCURRENCY_FAILURE

from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component

_CPT_RETRY = 0


class ExceptionService(Component):
    _inherit = "base.rest.service"
    _name = "exception.service"
    _usage = "exception"
    _collection = "base.rest.demo.public.services"
    _description = """
        Exception Services

        Services to test hiw exception are handled by base_erst
    """

    def user_error(self):
        """
        Simulate an odoo.exceptions.UserError
        Should be translated into BadRequest with a description into the json
        body
        """
        raise UserError(_("UserError message"))

    def validation_error(self):
        """
        Simulate an odoo.exceptions.ValidationError
        Should be translated into BadRequest with a description into the json
        body
        """
        raise ValidationError(_("ValidationError message"))

    def session_expired(self):
        """
        Simulate an odoo.http.SessionExpiredException
        Should be translated into Unauthorized without description into the
        json body
        """
        raise SessionExpiredException("Expired message")

    def missing_error(self):
        """
        Simulate an odoo.exceptions.MissingError
        Should be translated into NotFound without description into the json
        body
        """
        raise MissingError(_("Missing message"))

    def access_error(self):
        """
        Simulate an odoo.exceptions.AccessError
        Should be translated into Forbidden without description into the json
        body
        """
        raise AccessError(_("Access error message"))

    def access_denied(self):
        """
        Simulate an odoo.exceptions.AccessDenied
        Should be translated into Forbidden without description into the json
        body
        """
        raise AccessDenied()

    def http_exception(self):
        """
        Simulate an werkzeug.exceptions.MethodNotAllowed
        This exception is not by the framework
        """
        raise MethodNotAllowed(description="Method not allowed message")

    def bare_exception(self):
        """
        Simulate a python exception.
        Should be translated into InternalServerError without description into
        the json body
        """
        raise IOError("My IO error")

    def retryable_error(self, nbr_retries):
        """This method is used in the test suite to check that the retrying
        functionality in case of concurrency error on the database is working
        correctly for retryable exceptions.

        The output will be the number of retries that have been done.

        This method is mainly used to test the retrying functionality
        """
        global _CPT_RETRY
        if _CPT_RETRY < nbr_retries:
            _CPT_RETRY += 1
            raise FakeConcurrentUpdateError("fake error")
        tryno = _CPT_RETRY
        _CPT_RETRY = 0
        return {"retries": tryno}

    # Validator
    def _validator_user_error(self):
        return {}

    def _validator_return_user_error(self):
        return {}

    def _validator_validation_error(self):
        return {}

    def _validator_return_validation_error(self):
        return {}

    def _validator_session_expired(self):
        return {}

    def _validator_return_session_expired(self):
        return {}

    def _validator_missing_error(self):
        return {}

    def _validator_return_missing_error(self):
        return {}

    def _validator_access_error(self):
        return {}

    def _validator_return_access_error(self):
        return {}

    def _validator_access_denied(self):
        return {}

    def _validator_return_access_denied(self):
        return {}

    def _validator_http_exception(self):
        return {}

    def _validator_return_http_exception(self):
        return {}

    def _validator_bare_exception(self):
        return {}

    def _validator_return_bare_exception(self):
        return {}

    def _validator_retryable_error(self):
        return {
            "nbr_retries": {
                "type": "integer",
                "required": True,
                "default": MAX_TRIES_ON_CONCURRENCY_FAILURE,
                "coerce": to_int,
            }
        }

    def _validator_return_retryable_error(self):
        return {"retries": {"type": "integer"}}


class FakeConcurrentUpdateError(OperationalError):
    @property
    def pgcode(self):
        return errorcodes.SERIALIZATION_FAILURE
