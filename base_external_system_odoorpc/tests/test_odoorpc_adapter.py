# pylint: disable=method-required-super
# Copyright 2026 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase

from ..models import external_system_odoo as mod


class _FakeModel:
    def __init__(self, name):
        self._name = name
        self.search_calls = []
        self.read_calls = []
        self.search_read_calls = []

    def search(self, domain, limit=None, order=None):
        self.search_calls.append((domain, limit, order))
        # Simulate "admin" found
        return [1]

    def read(self, ids, fields=None):
        self.read_calls.append((ids, fields))
        return [{"id": ids[0], "name": "Admin"}]

    def search_read(self, domain, fields=None, limit=None, order=None):
        self.search_read_calls.append((domain, fields, limit, order))
        if self._name == "ir.model.data":
            return [{"res_id": 1}]
        return []


class _FakeEnv:
    def __init__(self):
        self._models = {}

    def __getitem__(self, model_name):
        if model_name not in self._models:
            self._models[model_name] = _FakeModel(model_name)
        return self._models[model_name]


class _FakeODOOClient:
    def __init__(self):
        self.logged_in = False
        self.logged_out = False
        self.login_calls = []
        self.env = _FakeEnv()

    def login(self, db, username, password):
        self.login_calls.append((db, username, password))
        # simulate successful login
        self.logged_in = True

    def logout(self):
        self.logged_out = True


class _FakeOdooRPCModule:
    """Fake `odoorpc` module replacement with an ODOO constructor."""

    def __init__(self):
        self.created = []
        self.last_client = None

    def ODOO(self, host, port=None, protocol=None):
        self.created.append((host, port, protocol))
        self.last_client = _FakeODOOClient()
        return self.last_client


class TestBaseExternalSystemOdooRPC(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(su=True)

    def _make_system(self, **overrides):
        vals = {
            "name": "Test system",
            "system_type": "external.system.odoo",
            "host": "test-test@odoo.test",
            "port": 443,
            "db_name": "testdatabase",
            "username": "admin",
            "password": "admin",
            "is_ssl": True,
            "company_ids": [(6, 0, [self.env.company.id])],
        }
        vals.update(overrides)
        return self.env["external.system"].create(vals)

    def _patch_odoorpc(self):
        """
        Patch the `odoorpc` module reference imported inside the adapter file.
        Adapter file imports odoorpc at module import time, so we override that
        module-level name with our fake.
        """
        fake = _FakeOdooRPCModule()
        mod.odoorpc = fake
        return fake

    def test_interface(self):
        sys = self._make_system()
        self.assertTrue(sys.interface)
        self.assertEqual(
            sys.interface._name,
            "external.system.odoo",
        )
        self.assertEqual(
            sys.interface.system_id.id,
            sys.id,
        )

    def test_external_get_client_ssl(self):
        sys = self._make_system(is_ssl=True)
        fake = self._patch_odoorpc()
        client = sys.interface.external_get_client()
        # constructor called with jsonrpc+ssl
        self.assertEqual(fake.created[-1], (sys.host, sys.port, "jsonrpc+ssl"))
        # login called
        self.assertTrue(client.logged_in)
        self.assertEqual(
            client.login_calls[-1],
            (sys.db_name, sys.username, sys.password),
        )

    def test_external_get_client_no_ssl(self):
        sys = self._make_system(is_ssl=False)
        fake = self._patch_odoorpc()
        client = sys.interface.external_get_client()
        self.assertEqual(fake.created[-1], (sys.host, sys.port, "jsonrpc"))
        self.assertTrue(client.logged_in)

    def test_external_get_client_validationerror(self):
        sys = self._make_system(db_name=False)
        self._patch_odoorpc()
        with self.assertRaises(ValidationError):
            sys.interface.external_get_client()

    def test_client_context_manager(self):
        sys = self._make_system()
        fake = self._patch_odoorpc()
        with sys.client() as client:
            self.assertTrue(client.logged_in)
            self.assertFalse(client.logged_out)
        # after context, destroy_client should have logged out
        self.assertTrue(fake.last_client.logged_out)

    def test_interface_connect(self):
        sys = self._make_system()
        fake = self._patch_odoorpc()
        client = sys.interface._connect()
        self.assertIs(client, fake.last_client)
        self.assertTrue(client.logged_in)

    def test_external_test_connection(self):
        """
        base_external_system's default external_test_connection raises UserError
        with a success message. Our adapter should:
          - open a client
          - call ir.model.data search_read probe for base.user_admin
          - then call super() which raises UserError
          - and logout on exit
        """
        sys = self._make_system()
        fake = self._patch_odoorpc()
        with self.assertRaises(UserError):
            sys.interface.external_test_connection()
        self.assertIsNotNone(fake.last_client)
        model_data = fake.last_client.env["ir.model.data"]
        self.assertEqual(len(model_data.search_read_calls), 1)
        self.assertEqual(
            model_data.search_read_calls[0][0],
            [
                ("module", "=", "base"),
                ("name", "=", "user_admin"),
            ],
        )
        self.assertEqual(model_data.search_read_calls[0][1], ["res_id"])
        self.assertEqual(model_data.search_read_calls[0][2], 1)
        # And should have logged out due to adapter.client() finally block
        self.assertTrue(fake.last_client.logged_out)
