# Copyright 2026 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta
from psycopg2 import IntegrityError

from odoo import fields
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestMaquilaProgram(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.matriz = cls.env["res.partner"].create({"name": "Test Matriz"})
        cls.product = cls.env["product.product"].create(
            {"name": "Test Maquila Product"}
        )
        cls.program = cls.env["l10n_py.maquila.program"].create(
            {
                "name": "Test Program",
                "code": "RES-BIM-TEST-001",
                "maquila_type": "pura",
                "matriz_partner_id": cls.matriz.id,
                "company_id": cls.company.id,
            }
        )

    def _activities(self, extra_domain=None):
        domain = [
            ("res_model", "=", "l10n_py.maquila.program"),
            ("res_id", "=", self.program.id),
        ]
        if extra_domain:
            domain += extra_domain
        return self.env["mail.activity"].search(domain)

    def test_state_transitions(self):
        self.assertEqual(self.program.state, "draft")
        self.program.action_activate()
        self.assertEqual(self.program.state, "active")
        self.program.action_suspend()
        self.assertEqual(self.program.state, "suspended")
        self.program.action_close()
        self.assertEqual(self.program.state, "closed")
        self.program.action_draft()
        self.assertEqual(self.program.state, "draft")

    def test_maquila_types(self):
        selection = dict(self.program._fields["maquila_type"].selection)
        for key in (
            "pura",
            "servicio",
            "ociosidad",
            "sub_maquila",
            "shelter",
            "coexistencia",
            "abrigo",
        ):
            self.assertIn(key, selection)

    def test_legal_regime_default(self):
        self.assertEqual(self.program.legal_regime, "ley_7547")
        self.assertEqual(self.program.benefit_duration_years, 20)

    def test_benefit_expiry(self):
        self.program.cnime_resolution_date = fields.Date.to_date("2026-01-01")
        self.assertEqual(self.program.benefit_expiry, fields.Date.to_date("2046-01-01"))

    def test_company_is_maquiladora_field(self):
        self.company.l10n_py_is_maquiladora = True
        self.assertTrue(self.company.l10n_py_is_maquiladora)

    @mute_logger("odoo.sql_db")
    def test_unique_code_per_company(self):
        with self.assertRaises(IntegrityError), self.cr.savepoint():
            self.env["l10n_py.maquila.program"].create(
                {
                    "name": "Duplicate",
                    "code": "RES-BIM-TEST-001",
                    "maquila_type": "pura",
                    "matriz_partner_id": self.matriz.id,
                    "company_id": self.company.id,
                }
            )
            self.env.flush_all()

    def test_program_product_line(self):
        line = self.env["l10n_py.maquila.program.product"].create(
            {
                "program_id": self.program.id,
                "product_id": self.product.id,
                "intn_certificate": "INTN-1",
                "intn_certificate_date": fields.Date.today(),
                "intn_expiry_date": fields.Date.today() + relativedelta(years=2),
            }
        )
        self.assertIn(line, self.program.product_line_ids)

    def test_cron_program_expiry(self):
        self.program.write(
            {
                "state": "active",
                "cnime_resolution_expiry": fields.Date.today() + relativedelta(days=30),
            }
        )
        cron = self.env["l10n_py.maquila.program"]
        cron._cron_check_expiry()
        cron._cron_check_expiry()
        # idempotent: running twice must not duplicate the activity
        self.assertEqual(len(self._activities()), 1)

    def test_cron_contract_expiry(self):
        agreement = self.env["agreement"].create(
            {
                "name": "Test CNIME Contract",
                "code": "AGR-TEST-1",
                "end_date": fields.Date.today() + relativedelta(days=100),
            }
        )
        self.program.write({"state": "active", "agreement_id": agreement.id})
        self.env["l10n_py.maquila.program"]._cron_check_expiry()
        self.assertTrue(self._activities())

    def test_cron_intn_expiry(self):
        self.env["l10n_py.maquila.program.product"].create(
            {
                "program_id": self.program.id,
                "product_id": self.product.id,
                "intn_certificate": "INTN-2",
                "intn_expiry_date": fields.Date.today() + relativedelta(days=30),
            }
        )
        self.program.write({"state": "active"})
        self.env["l10n_py.maquila.program"]._cron_check_expiry()
        self.assertTrue(self._activities([("summary", "like", "INTN")]))
