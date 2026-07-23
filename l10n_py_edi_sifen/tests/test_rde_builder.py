# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from unittest.mock import patch

from odoo.tests.common import TransactionCase, tagged

from odoo.addons.l10n_py_edi_sifen.services.rde_builder import RDeBuilder

_CDC = "01800123456001001000000112025011515158482505"


@tagged("post_install", "-at_install")
class TestRDeBuilder(TransactionCase):
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

    def _build(self, invoice=None, company=None, cdc=_CDC):
        return RDeBuilder(
            invoice if invoice is not None else self._get_sample_invoice_data(),
            company if company is not None else self._get_sample_company_data(),
            cdc,
        ).build()

    @patch("odoo.addons.l10n_py_edi_sifen.services.rde_builder.RDe")
    @patch("odoo.addons.l10n_py_edi_sifen.services.rde_builder.TDe")
    def test_build_creates_rde(self, mock_tde, mock_rde):
        """build() instancia RDe."""
        RDeBuilder(
            self._get_sample_invoice_data(),
            self._get_sample_company_data(),
            "0" * 44,
        ).build()
        mock_rde.assert_called_once()

    def test_build_root(self):
        """El rDE lleva versión, CDC y sistema de facturación."""
        rde = self._build()
        self.assertEqual(rde.dVerFor, 150)
        self.assertEqual(rde.DE.Id, _CDC)
        self.assertEqual(rde.DE.dDVId, _CDC[-1])
        self.assertEqual(rde.DE.dSisFact, 1)

    def test_build_timbrado(self):
        """gTimb refleja establecimiento, punto y número."""
        gtimb = self._build().DE.gTimb
        self.assertEqual(gtimb.iTiDE, 1)
        self.assertEqual(gtimb.dEst, "001")
        self.assertEqual(gtimb.dPunExp, "001")
        self.assertEqual(gtimb.dNumDoc, "0000001")

    def test_build_emisor(self):
        """gEmis toma el RUC y DV de la empresa."""
        emis = self._build().DE.gDatGralOpe.gEmis
        self.assertEqual(emis.dRucEm, "80012345")
        self.assertEqual(emis.dDVEmi, "6")
        self.assertEqual(emis.dNomEmi, "Empresa Test SA")

    def test_build_receptor(self):
        """gDatRec toma los datos del cliente."""
        rec = self._build().DE.gDatGralOpe.gDatRec
        self.assertEqual(rec.dRucRec, "12345678")
        self.assertEqual(rec.dNomRec, "Test Customer")

    def test_build_items(self):
        """gCamItem contiene los ítems de la factura."""
        items = self._build().DE.gDtipDE.gCamItem
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].dCodInt, "PROD-001")
        self.assertEqual(items[0].dDesProSer, "Producto Test")
        self.assertIsNotNone(items[0].gValorItem)
        self.assertIsNotNone(items[0].gCamIVA)

    def test_build_condicion_contado(self):
        """Condición contado (tipo 1)."""
        cond = self._build().DE.gDtipDE.gCamCond
        self.assertEqual(cond.iCondOpe, 1)

    def test_build_condicion_credito(self):
        """Condición crédito (tipo 2) arma gPagCred."""
        data = self._get_sample_invoice_data()
        data["condicion"] = {"tipo": 2, "credito": {"tipo": 1, "plazo": "30 días"}}
        cond = self._build(invoice=data).DE.gDtipDE.gCamCond
        self.assertEqual(cond.iCondOpe, 2)
        self.assertIsNotNone(cond.gPagCred)

    def test_build_serializes_to_xml(self):
        """El rDE serializa a XML bien formado con los datos esperados."""
        from lxml import etree
        from xsdata.formats.dataclass.serializers import XmlSerializer

        xml = XmlSerializer().render(self._build())
        root = etree.fromstring(xml.encode())
        self.assertTrue(root.tag.endswith("rDE"))
        self.assertIn("80012345", xml)
        self.assertIn("PROD-001", xml)
        self.assertIn("Producto Test", xml)
