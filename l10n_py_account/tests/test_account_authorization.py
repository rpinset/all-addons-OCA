from datetime import date, timedelta

from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


@tagged("post_install", "-at_install", "l10n_py")
class TestAccountAuthorization(TransactionCase):
    """Tests para el modelo account.authorization"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Authorization = cls.env["account.authorization"]
        cls.company = cls.env.ref("base.main_company")
        cls.country_py = cls.env.ref("base.py")

        # Obtener tipo de documento factura
        cls.doc_type_invoice = cls.env["l10n_latam.document.type"].search(
            [("country_id", "=", cls.country_py.id), ("code", "=", "1")],
            limit=1,
        )
        if not cls.doc_type_invoice:
            cls.doc_type_invoice = cls.env["l10n_latam.document.type"].create(
                {
                    "name": "Factura",
                    "code": "1",
                    "country_id": cls.country_py.id,
                    "internal_type": "invoice",
                }
            )

        cls.today = date.today()
        cls.date_from = cls.today - timedelta(days=30)
        cls.date_to = cls.today + timedelta(days=335)

    def _create_authorization(self, **kwargs):
        vals = {
            "name": "22334455",
            "date_from": self.date_from,
            "date_to": self.date_to,
            "invoice_number_from": 1,
            "invoice_number_to": 10000,
            "establishment": "001",
            "expedition_point": "001",
            "l10n_latam_document_type_id": self.doc_type_invoice.id,
            "company_id": self.company.id,
        }
        vals.update(kwargs)
        return self.Authorization.create(vals)

    # ============== F01: Timbrado ==============

    def test_create_authorization(self):
        """F01: Crear timbrado válido"""
        auth = self._create_authorization()
        self.assertTrue(auth.id)
        self.assertEqual(auth.state, "valid")

    def test_authorization_state_valid(self):
        """F01: Estado 'valid' cuando vigente"""
        auth = self._create_authorization()
        self.assertEqual(auth.state, "valid")

    def test_authorization_state_expired(self):
        """F01: Estado 'expired' cuando vencido"""
        auth = self._create_authorization(
            date_from=self.today - timedelta(days=400),
            date_to=self.today - timedelta(days=35),
        )
        self.assertEqual(auth.state, "expired")

    def test_authorization_state_to_expire(self):
        """F01: Estado 'to_expire' cuando < 30 días"""
        auth = self._create_authorization(
            date_from=self.today - timedelta(days=300),
            date_to=self.today + timedelta(days=25),
        )
        self.assertEqual(auth.state, "to_expire")

    def test_timbrado_format_validation(self):
        """F01: Rechaza timbrado con != 8 dígitos"""
        with self.assertRaises(ValidationError):
            self._create_authorization(name="1234567")  # 7 dígitos

        with self.assertRaises(ValidationError):
            self._create_authorization(name="1234567A")  # letras

    def test_establishment_format_validation(self):
        """F01: Rechaza establecimiento con != 3 dígitos"""
        with self.assertRaises(ValidationError):
            self._create_authorization(establishment="01")

        with self.assertRaises(ValidationError):
            self._create_authorization(establishment="00A")

    def test_invoice_range_validation(self):
        """F01: Rechaza range inválido (from > to)"""
        with self.assertRaises(ValidationError):
            self._create_authorization(invoice_number_from=1000, invoice_number_to=500)

    def test_reject_range_exceeding_max(self):
        """F01: Rechaza faja excediendo 9.999.999"""
        with self.assertRaises(ValidationError):
            self._create_authorization(invoice_number_to=10000000)

    def test_range_at_max_boundary(self):
        """F01: Aceita faja até exatamente 9.999.999"""
        auth = self._create_authorization(invoice_number_to=9999999)
        self.assertEqual(auth.invoice_number_to, 9999999)

    def test_date_validation(self):
        """F01: Rechaza date_to < date_from"""
        with self.assertRaises(ValidationError):
            self._create_authorization(
                date_from=self.today,
                date_to=self.today - timedelta(days=1),
            )

    def test_document_type_latam_integration(self):
        """F01: l10n_latam_document_type_id funciona"""
        auth = self._create_authorization()
        self.assertEqual(auth.l10n_latam_document_type_id, self.doc_type_invoice)

    def test_check_validity(self):
        """F01: Verificación de vigencia"""
        auth = self._create_authorization()
        self.assertTrue(auth.check_validity())

    def test_check_validity_expired(self):
        """F01: Timbrado vencido lanza error"""
        auth = self._create_authorization(
            date_from=self.today - timedelta(days=400),
            date_to=self.today - timedelta(days=35),
        )
        with self.assertRaises(ValidationError):
            auth.check_validity()

    def test_check_number_available(self):
        """F01: Número dentro del range y no usado"""
        auth = self._create_authorization()
        self.assertTrue(auth.check_number_available(500))

    def test_check_number_out_of_range(self):
        """F01: Número fuera del range"""
        auth = self._create_authorization()
        with self.assertRaises(ValidationError):
            auth.check_number_available(15000)

    def test_next_number_computation(self):
        """F01: Próximo número correcto"""
        auth = self._create_authorization()
        self.assertEqual(auth.next_number, 1)

    # ============== F01: Alertas de uso ==============

    def test_usage_percentage(self):
        """F01: Porcentaje de uso calculado correctamente"""
        auth = self._create_authorization(
            invoice_number_from=1,
            invoice_number_to=100,
        )
        # Sin facturas, uso = 0%
        self.assertEqual(auth.usage_percentage, 0.0)

    # ============== F02: Serie AA-ZZ ==============

    def test_series_default_aa(self):
        """F02: Serie por defecto es AA"""
        auth = self._create_authorization()
        self.assertEqual(auth.series, "AA")

    def test_series_validation_valid(self):
        """F02: Serie válida de 2 letras mayúsculas"""
        auth = self._create_authorization(series="AB")
        self.assertEqual(auth.series, "AB")

        auth2 = self._create_authorization(name="22334456", series="ZZ")
        self.assertEqual(auth2.series, "ZZ")

    def test_series_validation_invalid_mixed(self):
        """F02: Serie con dígitos rechazada"""
        with self.assertRaises(ValidationError):
            self._create_authorization(series="A1")

    def test_series_validation_invalid_lowercase(self):
        """F02: Serie con minúsculas rechazada"""
        with self.assertRaises(ValidationError):
            self._create_authorization(series="ab")

    def test_series_validation_invalid_single(self):
        """F02: Serie de 1 carácter rechazada"""
        with self.assertRaises(ValidationError):
            self._create_authorization(series="A")

    # ============== F01: name_get ==============

    def test_name_get(self):
        """F01: Formato de visualización"""
        auth = self._create_authorization(
            expedition_point="002",
        )
        name = auth.name_get()[0][1]
        self.assertIn("22334455", name)
        self.assertIn("001-002", name)

    def test_name_get_with_series(self):
        """F02: name_get incluye serie cuando != AA"""
        auth = self._create_authorization(series="BC")
        name = auth.name_get()[0][1]
        self.assertIn("Serie BC", name)

    def test_name_get_default_series_hidden(self):
        """F02: name_get no incluye serie AA (por defecto)"""
        auth = self._create_authorization(series="AA")
        name = auth.name_get()[0][1]
        self.assertNotIn("Serie", name)

    # ============== SQL Unique ==============

    @mute_logger("odoo.sql_db")
    def test_unique_constraint(self):
        """F02: Timbrado duplicado lanza IntegrityError"""
        self._create_authorization()
        with self.assertRaises(IntegrityError):
            self._create_authorization()
            self.env.cr.flush()
