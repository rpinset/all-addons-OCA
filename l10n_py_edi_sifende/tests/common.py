# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import copy
import json
import re
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger

from odoo.addons.l10n_py_edi_sifende.models import edi_connector
from odoo.addons.l10n_py_edi_sifende.services.client import clear_enum_cache

FIXTURES = Path(__file__).parent / "fixtures"
API_KEY = "sk_test_clave-ficticia"
CDC = "01800123451001001000000122026042710000000006"
STAMP = "24681357"
FIXED_DATE = date(2026, 10, 20)
SECURITY_CODE = "123456789"
QR_URL = "https://ekuatia.set.gov.py/consultas-test/qr?nVersion=150&Id=" + CDC


class FakeResponse:
    def __init__(self, status=200, body=None, headers=None, content=None):
        self.status_code = status
        self.headers = dict(headers or {})
        self._body = body
        if content is not None:
            self.content = content
        else:
            self.content = json.dumps(body).encode() if body is not None else b""
        if body is not None:
            self.headers.setdefault(
                "Content-Type",
                "application/problem+json" if status >= 400 else "application/json",
            )

    def json(self):
        if self._body is None:
            raise ValueError("sin cuerpo JSON")
        return self._body


def problem(slug, status, detail="", **extra):
    body = {
        "type": f"https://sifende.com.py/docs/solucion-problemas/{slug}",
        "title": slug,
        "status": status,
        "detail": detail,
        **extra,
    }
    return FakeResponse(status, body)


class Call:
    def __init__(self, method, url, kwargs):
        self.method = method
        self.url = url
        self.headers = kwargs.get("headers") or {}
        self.json = kwargs.get("json")
        self.params = kwargs.get("params")

    @property
    def path(self):
        return self.url.split("/api/v1", 1)[-1]


class FakeSifende:
    """Enrutador de `requests.request`: cada ruta consume sus respuestas en orden."""

    def __init__(self):
        self.routes = []
        self.calls = []

    def add(self, method, pattern, *responses):
        self.routes = [
            r for r in self.routes if (r[0], r[1].pattern) != (method, pattern)
        ]
        self.routes.append([method, re.compile(pattern), list(responses)])

    def __call__(self, method, url, **kwargs):
        call = Call(method, url, kwargs)
        self.calls.append(call)
        for route_method, pattern, responses in self.routes:
            if route_method == method and pattern.search(call.path):
                response = responses.pop(0) if len(responses) > 1 else responses[0]
                if isinstance(response, Exception):
                    raise response
                return response
        raise AssertionError(f"Llamada sin ruta simulada: {method} {url}")

    def calls_to(self, method, pattern):
        regex = re.compile(pattern)
        return [c for c in self.calls if c.method == method and regex.search(c.path)]


class SifendeCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.enums_fixture = json.loads((FIXTURES / "enums.json").read_text())
        cls.country_py = cls.env.ref("base.py")
        pyg = cls.env.ref("base.PYG")
        pyg.active = True
        cls.company = cls.env["res.company"].create(
            {
                "name": "Empresa Paraguaya Test",
                "country_id": cls.country_py.id,
                "currency_id": pyg.id,
                "l10n_py_ruc": "80009401",
            }
        )
        cls.env.user.write(
            {"company_ids": [(4, cls.company.id)], "company_id": cls.company.id}
        )
        cls.env = cls.env(
            context=dict(cls.env.context, allowed_company_ids=cls.company.ids)
        )
        cls._setup_accounts()
        cls._setup_taxes()
        cls._setup_partners()
        cls._setup_products()
        cls._setup_journals()
        cls.connector = cls.env["l10n_py.edi.connector"].create(
            {
                "name": "Sifende",
                "provider_type": "sifende",
                "environment": "test",
                "sifende_api_key": API_KEY,
                "company_id": cls.company.id,
            }
        )

    @classmethod
    def _account(cls, account_type, code, name, **extra):
        account = cls.env["account.account"].search(
            [
                ("company_ids", "in", cls.company.id),
                ("account_type", "=", account_type),
            ],
            limit=1,
        )
        return account or cls.env["account.account"].create(
            {
                "name": name,
                "code": code,
                "account_type": account_type,
                "company_ids": [(6, 0, [cls.company.id])],
                **extra,
            }
        )

    @classmethod
    def _setup_accounts(cls):
        cls.account_income = cls._account("income", "400099", "Ingresos")
        cls.account_receivable = cls._account(
            "asset_receivable", "110099", "Cuentas por cobrar", reconcile=True
        )

    @classmethod
    def _setup_taxes(cls):
        group = cls.env["account.tax.group"].create(
            {"name": "IVA Test", "country_id": cls.country_py.id}
        )

        def tax(name, amount, affectation, override="tax_included"):
            return cls.env["account.tax"].create(
                {
                    "name": name,
                    "amount": amount,
                    "amount_type": "percent",
                    "type_tax_use": "sale",
                    "tax_group_id": group.id,
                    "price_include_override": override,
                    "l10n_py_iva_affectation": affectation,
                }
            )

        cls.tax_10 = tax("IVA 10% Test", 10.0, "1")
        cls.tax_5 = tax("IVA 5% Test", 5.0, "1")
        cls.tax_exempt = tax("Exento Test", 0.0, "3")
        cls.tax_10_excluded = tax("IVA 10% excluido Test", 10.0, "1", "tax_excluded")

    @classmethod
    def _setup_partners(cls):
        state = cls.env["res.country.state"].search(
            [("country_id", "=", cls.country_py.id), ("l10n_py_code", "=", 12)], limit=1
        ) or cls.env["res.country.state"].create(
            {
                "name": "Central",
                "code": "CE",
                "country_id": cls.country_py.id,
                "l10n_py_code": 12,
            }
        )
        city = cls.env["res.city"].search(
            [("state_id", "=", state.id), ("name", "=", "LAMBARÉ")], limit=1
        ) or cls.env["res.city"].create(
            {
                "name": "LAMBARÉ",
                "country_id": cls.country_py.id,
                "state_id": state.id,
                "l10n_py_code": "1107",
            }
        )
        cls.city_sifende = cls.env["l10n_py.sifende.city"].search([("code", "=", 6106)])
        cls.city_code = city.l10n_py_code
        cls.city_name = city.name
        common = {
            "country_id": cls.country_py.id,
            "state_id": state.id,
            "city_id": city.id,
            "street": "Avenida Mariscal López",
            "property_account_receivable_id": cls.account_receivable.id,
        }
        cls.partner = cls.env["res.partner"].create(
            {
                **common,
                "name": "Comercial San Roque S.A.",
                "is_company": True,
                "l10n_py_ruc": "80012345",
                "l10n_py_taxpayer_type": "1",
                "email": "facturacion@sanroque.com.py",
                "phone": "+595 21 444 1111",
                "ref": "CLI-001",
            }
        )
        cls.partner_nc = cls.env["res.partner"].create(
            {
                **common,
                "name": "Ana González",
                "l10n_py_taxpayer_type": "2",
                "l10n_py_doc_type": "1",
                "l10n_py_doc_number": "4567890",
            }
        )

    @classmethod
    def _setup_products(cls):
        cls.product = cls.env["product.product"].create(
            {
                "name": "Resma de papel A4",
                "default_code": "PAP-A4",
                "list_price": 11000.0,
                "l10n_py_ncm_code": "48025610",
            }
        )
        cls.uom_kg = cls.env.ref("uom.product_uom_kgm")
        cls.uom_kg.l10n_py_sifende_unidad_medida = 83
        cls.product_kg = cls.env["product.product"].create(
            {
                "name": "Yerba mate",
                "default_code": "YERBA",
                "list_price": 52500.0,
                "uom_id": cls.uom_kg.id,
                "l10n_py_ncm_code": "09030090",
            }
        )

    @classmethod
    def _setup_journals(cls):
        today = date.today()
        doc_types = {
            "fe": "l10n_py_account.dc_py_f",
            "nc": "l10n_py_account.dc_py_nc",
            "nd": "l10n_py_account.dc_py_nd",
            "nr": "l10n_py_account.dc_py_nr",
            "af": "l10n_py_account.dc_py_af",
        }
        cls.doc_types, cls.auths, cls.journals = {}, {}, {}
        for key, xmlid in doc_types.items():
            cls.doc_types[key] = cls.env.ref(xmlid)
            cls.auths[key] = cls.env["account.authorization"].create(
                {
                    "name": STAMP,
                    # cubre FIXED_DATE y hoy, para que los tests no venzan
                    "date_from": min(today, FIXED_DATE) - timedelta(days=30),
                    "date_to": max(today, FIXED_DATE) + timedelta(days=335),
                    "invoice_number_from": 1,
                    "invoice_number_to": 9999999,
                    "establishment": "001",
                    "expedition_point": "001",
                    "l10n_latam_document_type_id": cls.doc_types[key].id,
                    "company_id": cls.company.id,
                }
            )
            cls.journals[key] = cls.env["account.journal"].create(
                {
                    "name": f"Ventas {key}",
                    "type": "sale",
                    "code": f"V{key.upper()}",
                    "company_id": cls.company.id,
                    "l10n_latam_use_documents": True,
                    "l10n_py_authorization_id": cls.auths[key].id,
                }
            )

    def setUp(self):
        super().setUp()
        if self.registry.test_cr is None:
            self.registry.enter_test_mode(self.cr)
            self.addCleanup(self.registry.leave_test_mode)
        clear_enum_cache()
        self.enums = copy.deepcopy(self.enums_fixture)
        self.fake = FakeSifende()
        self.fake.add("GET", r"/public/enums$", FakeResponse(200, self.enums))
        for patcher in (
            patch("requests.request", self.fake),
            patch.object(edi_connector.time, "sleep"),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)
        self.sleep = edi_connector.time.sleep
        mute = mute_logger("odoo.addons.l10n_py_edi_base.models.l10n_py_edi_log")
        mute.__enter__()
        self.addCleanup(mute.__exit__, None, None, None)
        self.addCleanup(clear_enum_cache)

    # === Documentos ===

    def make_move(self, kind="fe", lines=None, posted=True, **vals):
        move_type = "out_refund" if kind == "nc" else "out_invoice"
        lines = lines or [self.line()]
        move = self.env["account.move"].create(
            {
                "move_type": move_type,
                "partner_id": self.partner.id,
                "journal_id": self.journals[kind].id,
                "l10n_latam_document_type_id": self.doc_types[kind].id,
                "l10n_py_authorization_id": self.auths[kind].id,
                "invoice_date": FIXED_DATE,
                "l10n_py_security_code": SECURITY_CODE,
                "invoice_line_ids": [(0, 0, line) for line in lines],
                **vals,
            }
        )
        if posted:
            move.action_post()
        return move

    def line(self, product=None, qty=1, price=11000.0, tax=None, **vals):
        product = product or self.product
        return {
            "product_id": product.id,
            "name": product.name,
            "quantity": qty,
            "price_unit": price,
            "tax_ids": [(6, 0, (tax or self.tax_10).ids)],
            "account_id": self.account_income.id,
            **vals,
        }

    def nre_transport_vals(self, **extra):
        return {
            "transport_mode": "1",
            "transport_type": "1",
            "freight_responsibility": "1",
            "transport_start_date": date(2026, 10, 21),
            "transport_end_date": date(2026, 10, 21),
            "departure_address": "Calle Teniente Benítez",
            "departure_house": 120,
            "sifende_departure_city_id": self.city_sifende.id,
            "transporter_nature": "2",
            "transporter_name": "Carlos Benítez",
            "sifende_transporter_document_type": "1",
            "sifende_transporter_document_number": "3456789",
            "sifende_transporter_address": "Calle Teniente Benítez 120, Lambaré",
            "driver_doc_number": "3456789",
            "driver_name": "Carlos Benítez",
            "sifende_driver_address": "Calle Teniente Benítez 120, Lambaré",
            "vehicle_ids": [
                (
                    0,
                    0,
                    {
                        "vehicle_type": "CAMION",
                        "brand": "ISUZU",
                        "plate_number": "ABC1234",
                    },
                )
            ],
            "delivery_ids": [
                (
                    0,
                    0,
                    {
                        "address": "Avenida Mariscal López",
                        "house_number": 450,
                        "sifende_city_id": self.city_sifende.id,
                    },
                )
            ],
            **extra,
        }

    def make_nre(self, **transport_vals):
        move = self.make_move(
            "nr",
            l10n_py_nre_motive="5",
            l10n_py_sifende_km_recorrido=8,
            l10n_py_sifende_responsable_emision="3",
        )
        move.l10n_py_transport_id = self.env["l10n_py.transport"].create(
            self.nre_transport_vals(**transport_vals)
        )
        self.partner.l10n_py_ruc = self.company.l10n_py_ruc
        return move

    def associate(self, move, cdc="01800123451001001000000012026010112345678901"):
        return self.env["l10n_py.associated.document"].create(
            {"move_id": move.id, "association_type": "1", "cdc": cdc}
        )

    def emission_response(self, cdc=CDC, **extra):
        return FakeResponse(
            202,
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "cdc": cdc,
                "estado": "PENDIENTE",
                "numeroDocumento": 1,
                "numeroFormateado": "001-001-0000001",
                "qrUrl": QR_URL,
                "statusUrl": f"https://api.sifende.com.py/api/v1/documento-electronico/status/{cdc}",
                **extra,
            },
        )

    def status_response(self, estado, cdc=CDC, **extra):
        return FakeResponse(
            200,
            {
                "cdc": cdc,
                "estado": estado,
                "ambiente": "DEV",
                "iTiDe": 1,
                "numeroDocumento": 1,
                **extra,
            },
        )

    def route_emission(self, *responses):
        self.fake.add("POST", r"^/documento-electronico$", *responses)

    def expected(self, name):
        text = (FIXTURES / "expected" / f"{name}.json").read_text()
        return json.loads(text.replace("$DV$", self.partner.l10n_py_ruc_dv))

    def sent_payload(self, move):
        self.route_emission(self.emission_response())
        move.action_send_edi()
        return self.fake.calls_to("POST", r"^/documento-electronico$")[-1].json
