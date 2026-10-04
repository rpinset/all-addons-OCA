from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger

from ..validators.ruc_validator import RUCValidator

# Real Paraguayan RUCs, taken from the python-stdnum test corpus
# (stdnum/tests/test_py_ruc.doctest). Legal entities start after 80000000;
# residents and foreigners use shorter numbers.
REAL_RUCS = [
    "80028061-0",
    "80000035-8",
    "1068460-3",
    "1075150-5",
    "1152390-5",
    "999160-3",
    "2660-3",
]


@tagged("post_install", "-at_install", "l10n_py")
class TestRucValidator(TransactionCase):
    """Tests para el validador de RUC paraguayo"""

    def test_check_digit_known_values(self):
        """DV correcto para RUCs reales (algoritmo módulo 11 de la SET)"""
        test_cases = [
            ("80028061", 0),
            ("80000035", 8),
            ("1068460", 3),
            ("999160", 3),
            ("2660", 3),
        ]
        for ruc_number, expected_dv in test_cases:
            self.assertEqual(
                RUCValidator._calculate_check_digit(ruc_number),
                expected_dv,
                f"RUC {ruc_number} debe tener DV={expected_dv}",
            )

    def test_valid_ruc_with_correct_dv(self):
        """RUCs reales con DV correcto deben pasar validación"""
        for ruc in REAL_RUCS:
            is_valid, error = RUCValidator.validate(ruc)
            self.assertTrue(
                is_valid,
                f"RUC {ruc} debería ser válido, error: {error}",
            )

    def test_valid_ruc_without_dash(self):
        """El guión es opcional: 800280610 equivale a 80028061-0"""
        is_valid, error = RUCValidator.validate("800280610")
        self.assertTrue(is_valid, error)

    def test_invalid_ruc_wrong_dv(self):
        """RUC con DV incorrecto debe ser inválido"""
        is_valid, error = RUCValidator.validate("80028061-1")
        self.assertFalse(is_valid)
        self.assertIn("Invalid check digit", error)
        self.assertIn("Expected: 0", error)

    def test_invalid_ruc_letters(self):
        """RUC con letras debe ser inválido"""
        is_valid, error = RUCValidator.validate("AB1234-5")
        self.assertFalse(is_valid)
        self.assertFalse(RUCValidator.is_valid_format("1234567A"))

    def test_invalid_ruc_too_long(self):
        """RUC con más de 9 dígitos debe ser inválido"""
        is_valid, error = RUCValidator.validate("1234567890")
        self.assertFalse(is_valid)

    def test_invalid_ruc_empty(self):
        """RUC vacío debe ser inválido"""
        is_valid, error = RUCValidator.validate("")
        self.assertFalse(is_valid)
        self.assertIn("required", error)

    def test_leading_zeros_do_not_change_dv(self):
        """Los ceros a la izquierda no alteran el DV"""
        self.assertEqual(
            RUCValidator._calculate_check_digit("0002660"),
            RUCValidator._calculate_check_digit("2660"),
        )
        is_valid, error = RUCValidator.validate("0002660-3")
        self.assertTrue(is_valid, error)

    def test_ruc_normalization(self):
        """Normalización devuelve el formato NNNNNNNN-D"""
        self.assertEqual(RUCValidator.normalize("800280610"), "80028061-0")
        self.assertEqual(RUCValidator.normalize("80028061-0"), "80028061-0")

    @mute_logger("odoo.addons.l10n_py_base.validators.ruc_validator")
    def test_normalize_invalid_returns_original(self):
        """Un RUC inválido se devuelve sin cambios (y se registra un warning)"""
        self.assertEqual(RUCValidator.normalize("80028061-1"), "80028061-1")

    def test_get_check_digit(self):
        """Obtener dígito verificador"""
        self.assertEqual(RUCValidator.get_check_digit("80028061"), "0")

    def test_format_ruc_includes_dv(self):
        """Formato RUC con DV calculado"""
        self.assertEqual(RUCValidator.format_ruc("80028061"), "80028061-0")

    def test_format_ruc_excludes_dv(self):
        """Formato RUC sin DV"""
        formatted = RUCValidator.format_ruc("80028061", include_dv=False)
        self.assertEqual(formatted, "80028061")
        self.assertNotIn("-", formatted)

    def test_get_ruc_number(self):
        """Extraer solo número de RUC"""
        self.assertEqual(RUCValidator.get_ruc_number("80028061-0"), "80028061")

    def test_get_ruc_number_from_full(self):
        """Extraer número de RUC desde formato completo (dígitos concatenados)"""
        self.assertEqual(RUCValidator.get_ruc_number("800280610"), "80028061")
