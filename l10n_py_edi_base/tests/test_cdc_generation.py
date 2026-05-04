# l10n_py_edi_base/tests/test_cdc_generation.py

"""
Tests para generación de CDC (Código de Control)
"""

from datetime import datetime

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from ..services.cdc_generator import CDCGenerator


@tagged("post_install", "-at_install", "l10n_py", "cdc")
class TestCDCGeneration(TransactionCase):
    """Tests para generación de CDC (Código de Control)"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Datos de prueba
        cls.company_ruc = "80012345"
        cls.doc_type = 1  # Factura Electrónica
        cls.establishment = "001"
        cls.expedition_point = "001"
        cls.sequence = 1
        cls.emission_date = datetime(2025, 1, 15, 10, 30)

    def test_cdc_length(self):
        """CDC tiene 43 dígitos"""
        cdc = CDCGenerator.generate(
            company_ruc=self.company_ruc,
            doc_type=self.doc_type,
            establishment=self.establishment,
            expedition_point=self.expedition_point,
            sequence=self.sequence,
            emission_date=self.emission_date,
        )
        self.assertEqual(len(cdc), 43)

    def test_cdc_only_digits(self):
        """CDC contiene solo dígitos"""
        cdc = CDCGenerator.generate(
            company_ruc=self.company_ruc,
            doc_type=self.doc_type,
            establishment=self.establishment,
            expedition_point=self.expedition_point,
            sequence=self.sequence,
            emission_date=self.emission_date,
        )
        self.assertTrue(cdc.isdigit())

    def test_cdc_structure(self):
        """Estructura del CDC es correcta"""
        cdc = CDCGenerator.generate(
            company_ruc=self.company_ruc,
            doc_type=self.doc_type,
            establishment=self.establishment,
            expedition_point=self.expedition_point,
            sequence=self.sequence,
            emission_date=self.emission_date,
        )

        components = CDCGenerator.parse_cdc(cdc)

        self.assertEqual(components["ruc"], self.company_ruc.zfill(8))
        self.assertEqual(components["doc_type"], str(self.doc_type).zfill(2))
        self.assertEqual(components["establishment"], self.establishment)
        self.assertEqual(components["expedition_point"], self.expedition_point)
        self.assertEqual(components["sequence"], str(self.sequence).zfill(7))

    def test_validate_valid_cdc(self):
        """Validación pasa para CDC generado"""
        cdc = CDCGenerator.generate(
            company_ruc=self.company_ruc,
            doc_type=self.doc_type,
            establishment=self.establishment,
            expedition_point=self.expedition_point,
            sequence=self.sequence,
            emission_date=self.emission_date,
        )
        is_valid, error = CDCGenerator.validate_cdc(cdc)
        self.assertTrue(is_valid, f"CDC válido fue rechazado: {error}")

    def test_validate_invalid_cdc_length(self):
        """Rechaza CDC con != 43 dígitos"""
        is_valid, error = CDCGenerator.validate_cdc("123456789")
        self.assertFalse(is_valid)
        self.assertIn("43 dígitos", error)

    def test_validate_invalid_check_digit(self):
        """Rechaza DV incorrecto"""
        cdc = CDCGenerator.generate(
            company_ruc=self.company_ruc,
            doc_type=self.doc_type,
            establishment=self.establishment,
            expedition_point=self.expedition_point,
            sequence=self.sequence,
            emission_date=self.emission_date,
        )

        # Cambiar último dígito
        invalid_cdc = cdc[:-1] + ("0" if cdc[-1] != "0" else "1")
        is_valid, error = CDCGenerator.validate_cdc(invalid_cdc)
        self.assertFalse(is_valid)
        self.assertIn("verificador inválido", error)

    def test_validate_non_numeric(self):
        """Rechaza CDC con caracteres no numéricos"""
        is_valid, error = CDCGenerator.validate_cdc("A" * 43)
        self.assertFalse(is_valid)
        self.assertIn("números", error)

    def test_parse_cdc_components(self):
        """Extrae RUC, tipo doc, etc."""
        cdc = CDCGenerator.generate(
            company_ruc=self.company_ruc,
            doc_type=self.doc_type,
            establishment=self.establishment,
            expedition_point=self.expedition_point,
            sequence=self.sequence,
            emission_date=self.emission_date,
        )

        components = CDCGenerator.parse_cdc(cdc)

        required_keys = [
            "ruc",
            "doc_type",
            "establishment",
            "expedition_point",
            "sequence",
            "security_code",
            "datetime_code",
            "check_digit",
        ]
        for key in required_keys:
            self.assertIn(key, components)

    def test_format_cdc(self):
        """Formateo con separadores"""
        cdc = CDCGenerator.generate(
            company_ruc=self.company_ruc,
            doc_type=self.doc_type,
            establishment=self.establishment,
            expedition_point=self.expedition_point,
            sequence=self.sequence,
            emission_date=self.emission_date,
        )

        formatted = CDCGenerator.format_cdc(cdc)
        self.assertIn("-", formatted)

    def test_invalid_ruc_raises(self):
        """ValueError para RUC inválido"""
        with self.assertRaises(ValueError):
            CDCGenerator.generate(
                company_ruc="12345",  # Muy corto
                doc_type=self.doc_type,
                establishment=self.establishment,
                expedition_point=self.expedition_point,
                sequence=self.sequence,
            )

    def test_invalid_doc_type_raises(self):
        """ValueError para tipo inválido"""
        with self.assertRaises(ValueError):
            CDCGenerator.generate(
                company_ruc=self.company_ruc,
                doc_type=999,
                establishment=self.establishment,
                expedition_point=self.expedition_point,
                sequence=self.sequence,
            )

    def test_cdc_uniqueness(self):
        """CDCs generados son únicos"""
        cdcs = []
        for i in range(10):
            cdc = CDCGenerator.generate(
                company_ruc=self.company_ruc,
                doc_type=self.doc_type,
                establishment=self.establishment,
                expedition_point=self.expedition_point,
                sequence=i + 1,
                emission_date=self.emission_date,
            )
            cdcs.append(cdc)

        unique_cdcs = set(cdcs)
        self.assertEqual(len(cdcs), len(unique_cdcs))

    def test_cdc_different_doc_types(self):
        """CDC para diferentes tipos de documentos"""
        doc_types = [1, 4, 5, 6, 7]

        for doc_type in doc_types:
            cdc = CDCGenerator.generate(
                company_ruc=self.company_ruc,
                doc_type=doc_type,
                establishment=self.establishment,
                expedition_point=self.expedition_point,
                sequence=self.sequence,
                emission_date=self.emission_date,
            )

            components = CDCGenerator.parse_cdc(cdc)
            self.assertEqual(
                components["doc_type"],
                str(doc_type).zfill(2),
            )
