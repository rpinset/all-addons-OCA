from odoo.tests import tagged
from odoo.tests.common import TransactionCase


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
