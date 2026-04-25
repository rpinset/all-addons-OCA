# Copyright 2022 Camptocamp SA
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64

from odoo.addons.edi_component_oca.tests.common import EDIBackendCommonComponentTestCase


def _setup_webservice_backend(env):
    """Create demo webservice backend for tests."""
    return env["webservice.backend"].create(
        {
            "name": "Demo backend",
            "tech_name": "edi_demo_ws",
            "protocol": "http",
            "url": "https://foo.test/{endpoint}",
            "content_type": "application/xml",
            "auth_type": "none",
        }
    )


class TestEDIWebserviceBase(EDIBackendCommonComponentTestCase):
    @classmethod
    def _setup_records(cls):  # pylint:disable=missing-return
        super()._setup_records()
        cls.ws_backend = _setup_webservice_backend(cls.env)
        cls.backend.webservice_backend_id = cls.ws_backend
        cls.filedata = base64.b64encode(b"This is a simple file")
        cls.record = cls.backend.create_record(
            "test_csv_output",
            {
                "model": cls.partner._name,
                "res_id": cls.partner.id,
                "exchange_file": cls.filedata,
            },
        )
