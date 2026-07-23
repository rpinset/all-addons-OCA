"""Tests para generación de CDC (Código de Control) de 44 dígitos."""

from datetime import datetime

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from ..services.cdc_generator import CDCGenerator


@tagged("post_install", "-at_install", "l10n_py", "cdc")
class TestCDCGeneration(TransactionCase):
    """Tests para generación de CDC (Código de Control) de 44 dígitos."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cdc_kwargs = {
            "doc_type": 1,  # Factura Electrónica
            "ruc": "80012345",
            "dv": "1",
            "establishment": "001",
            "expedition_point": "001",
            "sequence": 1,
            "taxpayer_type": 1,  # 1=física, 2=jurídica
            "emission_date": datetime(2025, 1, 15, 10, 30),
        }

    def _generate(self, **overrides):
        return CDCGenerator.generate(**dict(self.cdc_kwargs, **overrides))

    def test_cdc_length(self):
        """CDC tiene 44 dígitos"""
        self.assertEqual(len(self._generate()), 44)

    def test_cdc_only_digits(self):
        """CDC contiene solo dígitos"""
        self.assertTrue(self._generate().isdigit())

    def test_cdc_structure(self):
        """Estructura del CDC es correcta"""
        components = CDCGenerator.parse_cdc(self._generate())
        self.assertEqual(components["doc_type"], "01")
        self.assertEqual(components["ruc"], "80012345")
        self.assertEqual(components["dv_ruc"], "1")
        self.assertEqual(components["establishment"], "001")
        self.assertEqual(components["expedition_point"], "001")
        self.assertEqual(components["sequence"], "0000001")
        self.assertEqual(components["taxpayer_type"], "1")
        self.assertEqual(components["emission_date"], "20250115")

    def test_security_code_reflected(self):
        """El código de seguridad recibido se refleja en el CDC"""
        cdc = self._generate(security_code="123456789")
        self.assertEqual(CDCGenerator.parse_cdc(cdc)["security_code"], "123456789")

    def test_deterministic_with_security_code(self):
        """Mismos datos + mismo código de seguridad → mismo CDC"""
        self.assertEqual(
            self._generate(security_code="123456789"),
            self._generate(security_code="123456789"),
        )

    def test_validate_valid_cdc(self):
        """Validación pasa para CDC generado"""
        is_valid, error = CDCGenerator.validate_cdc(self._generate())
        self.assertTrue(is_valid, f"CDC válido fue rechazado: {error}")

    def test_validate_invalid_cdc_length(self):
        """Rechaza CDC con != 44 dígitos"""
        is_valid, error = CDCGenerator.validate_cdc("123456789")
        self.assertFalse(is_valid)
        self.assertIn("44 dígitos", error)

    def test_validate_invalid_check_digit(self):
        """Rechaza DV incorrecto"""
        cdc = self._generate()
        invalid_cdc = cdc[:-1] + ("0" if cdc[-1] != "0" else "1")
        is_valid, error = CDCGenerator.validate_cdc(invalid_cdc)
        self.assertFalse(is_valid)
        self.assertIn("verificador inválido", error)

    def test_validate_non_numeric(self):
        """Rechaza CDC con caracteres no numéricos"""
        is_valid, error = CDCGenerator.validate_cdc("A" * 44)
        self.assertFalse(is_valid)
        self.assertIn("números", error)

    def test_parse_cdc_components(self):
        """Extrae RUC, tipo doc, etc."""
        components = CDCGenerator.parse_cdc(self._generate())
        required_keys = [
            "doc_type",
            "ruc",
            "dv_ruc",
            "establishment",
            "expedition_point",
            "sequence",
            "taxpayer_type",
            "emission_date",
            "emission_type",
            "security_code",
            "check_digit",
        ]
        for key in required_keys:
            self.assertIn(key, components)

    def test_parse_cdc_invalid_length_raises(self):
        """ValueError al parsear un CDC de longitud inválida"""
        with self.assertRaises(ValueError):
            CDCGenerator.parse_cdc("123")

    def test_invalid_doc_type_raises(self):
        """ValueError para tipo de documento fuera de rango"""
        with self.assertRaises(ValueError):
            self._generate(doc_type=999)

    def test_cdc_uniqueness(self):
        """CDCs con secuencia distinta son únicos"""
        cdcs = [
            self._generate(sequence=i + 1, security_code="123456789") for i in range(10)
        ]
        self.assertEqual(len(cdcs), len(set(cdcs)))

    def test_cdc_different_doc_types(self):
        """CDC para diferentes tipos de documentos"""
        for doc_type in [1, 4, 5, 6, 7]:
            components = CDCGenerator.parse_cdc(self._generate(doc_type=doc_type))
            self.assertEqual(components["doc_type"], str(doc_type).zfill(2))
