# l10n_py_edi_base/services/qr_generator.py

"""
Generador del código QR (dCarQR) para documentos electrónicos paraguayos.

Implementa la construcción del enlace de consulta y el cálculo de cHashQR
conforme al Manual Técnico SIFEN (sección "Generación del código QR").

Estructura del enlace::

    {base}?nVersion=150&Id={CDC}&dFeEmiDE={hex}&dRucRec|dNumIDRec={..}
          &dTotGralOpe={..}&dTotIVA={..}&cItems={..}&DigestValue={hex}
          &IdCSC={..}&cHashQR={sha256(querystring + CSC)}

El CSC (Código de Seguridad del Contribuyente) y su Id los entrega la SET
y son DISTINTOS por ambiente (test/homologación vs producción).
"""

import hashlib
import logging
from io import BytesIO

_logger = logging.getLogger(__name__)

# URLs públicas de consulta (NO son los WSDL de transmisión)
QR_BASE_TEST = "https://ekuatia.set.gov.py/consultas-test/qr"
QR_BASE_PROD = "https://ekuatia.set.gov.py/consultas/qr"

QR_VERSION = "150"


class QRGenerator:
    """Construye el dCarQR y la imagen PNG del código QR."""

    @staticmethod
    def _to_hex(value):
        """Codifica un string como su representación hexadecimal (UTF-8)."""
        return (value or "").encode("utf-8").hex()

    @classmethod
    def build_qr_link(
        cls,
        *,
        cdc,
        emission_date,
        digest_value,
        idcsc,
        csc,
        total_operation,
        total_iva,
        item_count,
        receptor_ruc=None,
        receptor_doc_number=None,
        is_test=True,
    ):
        """Construye el enlace dCarQR completo (con cHashQR).

        Args:
            cdc (str): Código de Control (CDC) del DTE.
            emission_date (str): Valor de dFeEmiDE (ISO, ej. 2026-06-24T10:30:00).
            digest_value (str): DigestValue (base64) de la firma del XML.
            idcsc (str): Identificador del CSC (ej. "0001").
            csc (str): Código de Seguridad del Contribuyente (secreto SET).
            total_operation (str|int): dTotGralOpe.
            total_iva (str|int): dTotIVA.
            item_count (int): cItems (cantidad de ítems).
            receptor_ruc (str): RUC del receptor si es contribuyente.
            receptor_doc_number (str): Nº de documento si NO es contribuyente.
            is_test (bool): True para homologación (HML), False para producción.

        Returns:
            str: enlace dCarQR completo.
        """
        if not csc or not idcsc:
            raise ValueError(
                "CSC e IdCSC son obligatorios para generar el código QR. "
                "Configúrelos en el conector EDI (son distintos por ambiente)."
            )
        if not digest_value:
            raise ValueError(
                "DigestValue de la firma es obligatorio para el QR "
                "(el documento debe estar firmado)."
            )

        # Orden EXACTO de los parámetros según el Manual Técnico SIFEN.
        # NOTA: la cadena se construye por concatenación CRUDA (sin url-encode),
        # idéntica a la librería oficial TIPS-SA/facturacionelectronicapy-qrgen,
        # porque el SET recalcula el hash sobre esa misma cadena tal cual.
        params = [
            ("nVersion", QR_VERSION),
            ("Id", cdc),
            ("dFeEmiDE", cls._to_hex(emission_date)),
        ]
        if receptor_ruc:
            params.append(("dRucRec", receptor_ruc))
        else:
            params.append(("dNumIDRec", receptor_doc_number or "0"))
        params += [
            ("dTotGralOpe", str(total_operation)),
            ("dTotIVA", str(total_iva)),
            ("cItems", str(item_count)),
            ("DigestValue", cls._to_hex(digest_value)),
            ("IdCSC", idcsc),
        ]

        query = "&".join(f"{key}={value}" for key, value in params)
        # cHashQR = SHA-256 hex de la cadena concatenada con el CSC.
        chash = hashlib.sha256((query + csc).encode("utf-8")).hexdigest()

        base = QR_BASE_TEST if is_test else QR_BASE_PROD
        return f"{base}?{query}&cHashQR={chash}"

    @staticmethod
    def generate_image(data, box_size=4, border=2):
        """Genera la imagen PNG del QR en base64 (listo para Binary de Odoo).

        Returns:
            bytes: contenido PNG codificado en base64, o False si falla.
        """
        if not data:
            return False
        try:
            import base64

            import qrcode

            qr = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=box_size,
                border=border,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buff = BytesIO()
            img.save(buff, format="PNG")
            return base64.b64encode(buff.getvalue())
        except Exception as exc:  # pragma: no cover - depende de libs externas
            _logger.warning("No se pudo generar la imagen del QR: %s", exc)
            return False
