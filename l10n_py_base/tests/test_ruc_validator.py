from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from ..validators.ruc_validator import RUCValidator


@tagged("post_install", "-at_install", "l10n_py")
class TestRucValidator(TransactionCase):
    """Tests para el validador de RUC paraguayo"""

    def test_check_digit_known_values(self):
        """DV correcto para RUCs conocidos (verificados contra SET)"""
        self.assertEqual(
            RUCValidator._calculate_check_digit("80012345"),
            6,
            "RUC 80012345 debe tener DV=6",
        )
        self.assertEqual(
            RUCValidator._calculate_check_digit("4588955"),
            1,
            "RUC 4588955 debe tener DV=1",
        )
        self.assertEqual(
            RUCValidator._calculate_check_digit("80009401"),
            0,
            "RUC 80009401 debe tener DV=0",
        )
        self.assertEqual(
            RUCValidator._calculate_check_digit("80067890"),
            7,
            "RUC 80067890 debe tener DV=7",
        )
        self.assertEqual(
            RUCValidator._calculate_check_digit("80054321"),
            2,
            "RUC 80054321 debe tener DV=2",
        )

    def test_valid_ruc_with_correct_dv(self):
        """RUCs válidos con DV correcto deben pasar validación"""
        valid_rucs = [
            "80012345-6",
            "4588955-1",
            "80009401-0",
        ]
        for ruc in valid_rucs:
            is_valid, error = RUCValidator.validate(ruc)
            self.assertTrue(
                is_valid,
                f"RUC {ruc} debería ser válido, error: {error}",
            )

    def test_invalid_ruc_wrong_dv(self):
        """RUC con DV incorrecto debe ser inválido"""
        is_valid, error = RUCValidator.validate("80012345-1")
        self.assertFalse(is_valid)
        self.assertIn("Dígito verificador inválido", error)

    def test_invalid_ruc_too_short(self):
        """RUC muy corto debe ser inválido"""
        is_valid, error = RUCValidator.validate("12345")
        self.assertFalse(is_valid)

    def test_invalid_ruc_letters(self):
        """RUC con letras debe ser inválido"""
        self.assertFalse(RUCValidator.is_valid_format("1234567A"))

    def test_ruc_normalization(self):
        """Normalización agrega DV correcto"""
        normalized = RUCValidator.normalize("80012345-6")
        self.assertEqual(normalized, "80012345-6")

    def test_get_check_digit(self):
        """Obtener dígito verificador"""
        dv = RUCValidator.get_check_digit("80012345")
        self.assertEqual(dv, "6")

    def test_format_ruc_includes_dv(self):
        """Formato RUC con DV"""
        formatted = RUCValidator.format_ruc("80012345", include_dv=True)
        self.assertEqual(formatted, "80012345-6")

    def test_format_ruc_excludes_dv(self):
        """Formato RUC sin DV"""
        formatted = RUCValidator.format_ruc("80012345", include_dv=False)
        self.assertEqual(formatted, "80012345")
        self.assertNotIn("-", formatted)

    def test_get_ruc_number(self):
        """Extraer solo número de RUC"""
        ruc_number = RUCValidator.get_ruc_number("80012345-6")
        self.assertEqual(ruc_number, "80012345")

    def test_get_ruc_number_from_full(self):
        """Extraer número de RUC desde formato completo (dígitos concatenados)"""
        ruc_number = RUCValidator.get_ruc_number("800123456")
        self.assertEqual(ruc_number, "80012345")
