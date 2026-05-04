# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from unittest import TestCase
from unittest.mock import patch

from odoo.tests.common import tagged


@tagged("post_install", "-at_install")
class TestRDeBuilder(TestCase):
    """Test RDeBuilder without Odoo environment (pure Python)."""

    def _get_sample_invoice_data(self):
        return {
            "tipoDocumento": 1,
            "establecimiento": "001",
            "punto": "001",
            "numero": "0000001",
            "fecha": "2025-01-15T10:30:00",
            "tipoEmision": 1,
            "tipoTransaccion": 1,
            "codigoSeguridadAleatorio": "123456789",
            "moneda": "PYG",
            "cliente": {
                "ruc": "12345678",
                "razonSocial": "Test Customer",
                "nombreFantasia": "Test",
                "direccion": "Calle Test 123",
                "numeroCasa": "123",
            },
            "factura": {"presencia": 1},
            "items": [
                {
                    "codigo": "PROD-001",
                    "descripcion": "Producto Test",
                    "unidadMedida": 77,
                    "cantidad": 2,
                    "precioUnitario": 100000,
                    "ivaTipo": 1,
                    "ivaBase": 100,
                    "iva": 10,
                    "baseGravada": 181818.18,
                    "liquidacionIva": 18181.82,
                },
            ],
            "totales": {
                "totalExento": 0,
                "totalGravado5": 0,
                "totalGravado10": 200000,
                "totalOperacion": 200000,
                "totalIva": 18181.82,
                "liquidacionIva5": 0,
                "liquidacionIva10": 18181.82,
                "baseGravada5": 0,
                "baseGravada10": 181818.18,
                "totalBaseGravada": 181818.18,
            },
            "condicion": {"tipo": 1},
        }

    def _get_sample_company_data(self):
        return {
            "ruc": "80012345",
            "dv": "6",
            "razonSocial": "Empresa Test SA",
            "nombreFantasia": "Empresa Test",
            "actividadEconomica": "Venta al por menor",
            "direccion": "Av. Principal 456",
            "numeroCasa": "456",
            "departamento": 11,
            "distrito": 1,
            "ciudad": "1",
            "telefono": "021555555",
            "email": "test@empresa.com",
        }

    @patch("l10n_py_edi_sifen.services.rde_builder.RDe")
    @patch("l10n_py_edi_sifen.services.rde_builder.TDe")
    def test_build_creates_rde(self, mock_tde, mock_rde):
        """Test that build() creates an RDe object."""
        from l10n_py_edi_sifen.services.rde_builder import RDeBuilder

        builder = RDeBuilder(
            self._get_sample_invoice_data(),
            self._get_sample_company_data(),
            "0" * 43,
        )
        builder.build()
        mock_rde.assert_called_once()
