from psycopg2 import IntegrityError

from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


@tagged("post_install", "-at_install", "l10n_py")
class TestGeographicData(TransactionCase):
    """Tests para datos geográficos de Paraguay"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country_py = cls.env.ref("base.py")

    def test_departments_loaded(self):
        """17 departamentos PY deben estar cargados"""
        departments = self.env["res.country.state"].search(
            [("country_id", "=", self.country_py.id)]
        )
        self.assertGreaterEqual(
            len(departments), 17, "Debe haber al menos 17 departamentos"
        )

    def test_department_set_codes(self):
        """Departamentos deben tener códigos SET"""
        departments = self.env["res.country.state"].search(
            [
                ("country_id", "=", self.country_py.id),
                ("l10n_py_code", "!=", False),
                ("l10n_py_code", "!=", 0),
            ]
        )
        self.assertGreater(
            len(departments), 0, "Al menos un departamento debe tener código SET"
        )

    def test_cities_loaded(self):
        """Ciudades PY deben estar cargadas"""
        cities = self.env["res.city"].search([("country_id", "=", self.country_py.id)])
        self.assertGreater(len(cities), 0, "Debe haber ciudades cargadas")

    def test_neighborhoods_loaded(self):
        """Barrios deben estar cargados"""
        neighborhoods = self.env["l10n_py.neighborhood"].search([])
        self.assertGreater(len(neighborhoods), 0, "Debe haber barrios cargados")

    @mute_logger("odoo.sql_db")
    def test_set_code_unique_per_country(self):
        """Dos departamentos del mismo país no pueden compartir el código SET"""
        State = self.env["res.country.state"]
        State.create(
            {
                "name": "PY Test Dept A",
                "country_id": self.country_py.id,
                "code": "QW",
                "l10n_py_code": 9991,
            }
        )
        with self.assertRaises(IntegrityError), self.cr.savepoint():
            State.create(
                {
                    "name": "PY Test Dept B",
                    "country_id": self.country_py.id,
                    "code": "QX",
                    "l10n_py_code": 9991,
                }
            )

    def test_set_code_reused_across_countries(self):
        """El mismo código SET se permite en países distintos (único por país)"""
        State = self.env["res.country.state"]
        country_ar = self.env.ref("base.ar")
        State.create(
            {
                "name": "PY Test Dept",
                "country_id": self.country_py.id,
                "code": "QY",
                "l10n_py_code": 9992,
            }
        )
        state_ar = State.create(
            {
                "name": "AR Test Prov",
                "country_id": country_ar.id,
                "code": "QY",
                "l10n_py_code": 9992,
            }
        )
        self.assertTrue(state_ar.id)
