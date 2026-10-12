# l10n_py_edi_base/tests/test_qr_generator.py

"""Tests para la generación del código QR (dCarQR) SIFEN."""

import hashlib

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from ..services.qr_generator import QRGenerator

_CDC = "01800094010001001000000120260624123456789012"
_CSC = "ABCD0000000000000000000000000000"


@tagged("post_install", "-at_install", "l10n_py", "qr")
class TestQRGenerator(TransactionCase):
    """Tests de la construcción del enlace dCarQR y la imagen."""

    def _build(self, **kw):
        params = dict(
            cdc=_CDC,
            emission_date="2026-06-24T10:30:00",
            digest_value="abc123BASE64DIGEST==",
            idcsc="0001",
            csc=_CSC,
            total_operation=110000,
            total_iva=10000,
            item_count=2,
            receptor_ruc="80012345",
            is_test=True,
        )
        params.update(kw)
        return QRGenerator.build_qr_link(**params)

    def test_link_structure(self):
        """El enlace usa la base de homologación y los parámetros esperados."""
        link = self._build()
        self.assertTrue(
            link.startswith("https://ekuatia.set.gov.py/consultas-test/qr?")
        )
        for token in ("nVersion=150", f"Id={_CDC}", "dRucRec=80012345", "IdCSC=0001"):
            self.assertIn(token, link)
        # dFeEmiDE y DigestValue van en hexadecimal
        self.assertIn("dFeEmiDE=" + b"2026-06-24T10:30:00".hex(), link)

    def test_prod_base_url(self):
        """En producción cambia la URL base."""
        link = self._build(is_test=False)
        self.assertTrue(link.startswith("https://ekuatia.set.gov.py/consultas/qr?"))

    def test_non_taxpayer_uses_doc_number(self):
        """Receptor no contribuyente usa dNumIDRec en vez de dRucRec."""
        link = self._build(receptor_ruc=None, receptor_doc_number="1234567")
        self.assertIn("dNumIDRec=1234567", link)
        self.assertNotIn("dRucRec=", link)

    def test_hash_is_deterministic_and_correct(self):
        """cHashQR = SHA-256(querystring + CSC)."""
        link = self._build()
        query, chash = link.split("?", 1)[1].rsplit("&cHashQR=", 1)
        expected = hashlib.sha256((query + _CSC).encode("utf-8")).hexdigest()
        self.assertEqual(chash, expected)

    def test_csc_required(self):
        """Sin CSC se levanta error (no se puede firmar el QR)."""
        with self.assertRaises(ValueError):
            self._build(csc="")

    def test_image_is_png(self):
        """La imagen generada es un PNG (base64)."""
        import base64

        img_b64 = QRGenerator.generate_image(self._build())
        self.assertTrue(img_b64)
        self.assertEqual(base64.b64decode(img_b64)[:8], b"\x89PNG\r\n\x1a\n")
