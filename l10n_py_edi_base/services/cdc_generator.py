# l10n_py_edi_base/services/cdc_generator.py

"""
Generador del Código de Control (CDC) de 44 dígitos para documentos
electrónicos paraguayos, conforme al Manual Técnico SIFEN.

Conformación del CDC (44 dígitos)::

    1. iTiDE      (2)  Tipo de Documento Electrónico
    2. dRucEm     (8)  RUC del emisor (sin DV), completado con ceros a la izq.
    3. dDVEmi     (1)  Dígito verificador del RUC emisor
    4. dEst       (3)  Establecimiento
    5. dPunExp    (3)  Punto de expedición
    6. dNumDoc    (7)  Número del documento
    7. iTipCont   (1)  Tipo de contribuyente (1=física, 2=jurídica)
    8. dFeEmiDE   (8)  Fecha de emisión (AAAAMMDD)
    9. iTipEmi    (1)  Tipo de emisión (1=normal, 2=contingencia)
    10. dCodSeg   (9)  Código de seguridad aleatorio
    11. dDVId     (1)  Dígito verificador (módulo 11, base 11)

IMPORTANTE: el `dCodSeg` del CDC debe coincidir con el `dCodSeg` del grupo
gOpeDE del XML; por eso el código de seguridad se genera una sola vez y se
comparte (ver _sifen_build_rde).
"""

import logging
import secrets
from datetime import date, datetime

_logger = logging.getLogger(__name__)

CDC_LENGTH = 44


class CDCGenerator:
    """Generador del Código de Control (CDC) de 44 dígitos."""

    @staticmethod
    def generate_security_code():
        """Código de seguridad aleatorio de 9 dígitos."""
        return str(secrets.randbelow(10**9)).zfill(9)

    @staticmethod
    def _only_digits(value):
        return "".join(filter(str.isdigit, str(value or "")))

    @classmethod
    def _format_date(cls, emission_date):
        """Devuelve la fecha de emisión como AAAAMMDD."""
        if emission_date is None:
            emission_date = datetime.now()
        if isinstance(emission_date, str):
            # Acepta ISO (2026-06-01T..) o AAAA-MM-DD
            emission_date = datetime.fromisoformat(emission_date[:19])
        if isinstance(emission_date, datetime | date):
            return emission_date.strftime("%Y%m%d")
        return str(emission_date)

    @classmethod
    def generate(
        cls,
        *,
        doc_type,
        ruc,
        dv,
        establishment,
        expedition_point,
        sequence,
        taxpayer_type,
        emission_date,
        emission_type=1,
        security_code=None,
    ):
        """Genera el CDC de 44 dígitos conforme al Manual Técnico SIFEN."""
        if security_code is None:
            security_code = cls.generate_security_code()
        ruc_clean = cls._only_digits(ruc)[:8].zfill(8)
        base = (
            str(int(doc_type)).zfill(2)
            + ruc_clean
            + cls._only_digits(dv)[:1]
            + str(int(establishment)).zfill(3)
            + str(int(expedition_point)).zfill(3)
            + str(int(sequence)).zfill(7)
            + str(taxpayer_type)
            + cls._format_date(emission_date)
            + str(int(emission_type))
            + cls._only_digits(security_code).zfill(9)
        )
        if len(base) != CDC_LENGTH - 1:
            raise ValueError(
                f"Base del CDC debe tener {CDC_LENGTH - 1} dígitos, "
                f"generado {len(base)}: {base}"
            )
        cdc = base + str(cls._calculate_check_digit(base))
        _logger.debug("CDC generado: %s", cdc)
        return cdc

    @staticmethod
    def _calculate_check_digit(value, base_max=11):
        """Dígito verificador módulo 11 (base 11, pesos cíclicos 2..base_max).

        Recorre de derecha a izquierda; si resto > 1 → 11 - resto, si no → 0.
        """
        total = 0
        k = 2
        for ch in reversed(value):
            if k > base_max:
                k = 2
            total += int(ch) * k
            k += 1
        resto = total % 11
        return 11 - resto if resto > 1 else 0

    @classmethod
    def validate_cdc(cls, cdc):
        """Valida longitud (44), que sea numérico y el dígito verificador."""
        if not cdc:
            return False, "CDC es obligatorio"
        if len(cdc) != CDC_LENGTH:
            return False, f"CDC debe tener {CDC_LENGTH} dígitos, recibido: {len(cdc)}"
        if not cdc.isdigit():
            return False, "CDC debe contener solo números"
        expected = cls._calculate_check_digit(cdc[:-1])
        if int(cdc[-1]) != expected:
            return (
                False,
                f"Dígito verificador inválido. Esperado: {expected}, "
                f"recibido: {cdc[-1]}",
            )
        return True, ""

    @classmethod
    def parse_cdc(cls, cdc):
        """Extrae los componentes del CDC (44 dígitos)."""
        if len(cdc) != CDC_LENGTH:
            raise ValueError(
                f"CDC debe tener {CDC_LENGTH} dígitos, recibido: {len(cdc)}"
            )
        return {
            "doc_type": cdc[0:2],
            "ruc": cdc[2:10],
            "dv_ruc": cdc[10:11],
            "establishment": cdc[11:14],
            "expedition_point": cdc[14:17],
            "sequence": cdc[17:24],
            "taxpayer_type": cdc[24:25],
            "emission_date": cdc[25:33],
            "emission_type": cdc[33:34],
            "security_code": cdc[34:43],
            "check_digit": cdc[43:44],
        }
