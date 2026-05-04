# l10n_py_edi_base/services/cdc_generator.py

"""
Generador de Código de Control (CDC) para documentos electrónicos paraguayos
Implementación conforme Manual Técnico SIFEN v150
"""

import logging
import secrets
from datetime import datetime

_logger = logging.getLogger(__name__)


class CDCGenerator:
    """
    Generador de Código de Control (CDC) para documentos electrónicos

    Formato CDC (43 dígitos):
    - RUC del emisor (8 dígitos)
    - Tipo de documento (2 dígitos)
    - Establecimiento (3 dígitos)
    - Punto de expedición (3 dígitos)
    - Número del documento (7 dígitos)
    - Código de seguridad (8 dígitos)
    - Fecha/hora de emisión (11 dígitos)
    - Dígito verificador (1 dígito)
    """

    # Multiplicadores para dígito verificador (posiciones 1-42)
    MULTIPLIERS = [2, 3, 4, 5, 6, 7, 8, 9] * 6  # Repetir hasta 42 posiciones

    @classmethod
    def generate(
        cls,
        company_ruc,
        doc_type,
        establishment,
        expedition_point,
        sequence,
        emission_date=None,
    ):
        """
        Generar CDC conforme especificación SIFEN v150

        Args:
            company_ruc (str): RUC de la empresa emisora (sin DV)
            doc_type (int): Tipo de documento (1=FE, 4=Autofactura, etc.)
            establishment (str): Establecimiento (3 dígitos)
            expedition_point (str): Punto de expedición (3 dígitos)
            sequence (int): Número secuencial del documento
            emission_date (datetime): Fecha de emisión (opcional)

        Returns:
            str: CDC completo con dígito verificador (43 dígitos)
        """
        if emission_date is None:
            emission_date = datetime.now()

        # Validar parámetros
        cls._validate_parameters(
            company_ruc, doc_type, establishment, expedition_point, sequence
        )

        # Construir CDC base (42 dígitos)
        cdc_base = cls._build_cdc_base(
            company_ruc,
            doc_type,
            establishment,
            expedition_point,
            sequence,
            emission_date,
        )

        # Calcular dígito verificador
        check_digit = cls._calculate_check_digit(cdc_base)

        # CDC final (43 dígitos)
        cdc_complete = cdc_base + str(check_digit)

        # Validar formato final
        if len(cdc_complete) != 43:
            raise ValueError(
                f"CDC debe tener 43 dígitos, generado: {len(cdc_complete)}"
            )

        _logger.info("CDC generado: %s", cdc_complete)
        return cdc_complete

    @classmethod
    def _validate_parameters(
        cls, company_ruc, doc_type, establishment, expedition_point, sequence
    ):
        """Validar parámetros de entrada"""
        # Validar RUC
        ruc_clean = "".join(filter(str.isdigit, str(company_ruc)))
        if len(ruc_clean) < 6 or len(ruc_clean) > 8:
            raise ValueError(f"RUC inválido: {company_ruc}")

        # Validar tipo de documento
        if not isinstance(doc_type, int) or doc_type < 1 or doc_type > 99:
            raise ValueError(f"Tipo de documento inválido: {doc_type}")

        # Validar establishment
        est_clean = str(establishment).zfill(3)
        if len(est_clean) != 3 or not est_clean.isdigit():
            raise ValueError(f"Establecimiento inválido: {establishment}")

        # Validar expedition point
        exp_clean = str(expedition_point).zfill(3)
        if len(exp_clean) != 3 or not exp_clean.isdigit():
            raise ValueError(f"Punto de expedición inválido: {expedition_point}")

        # Validar sequence
        if not isinstance(sequence, int) or sequence < 1 or sequence > 9999999:
            raise ValueError(f"Secuencia inválida: {sequence}")

    @classmethod
    def _build_cdc_base(
        cls,
        company_ruc,
        doc_type,
        establishment,
        expedition_point,
        sequence,
        emission_date,
    ):
        """
        Construir base del CDC (42 dígitos)

        Formato conforme SIFEN:
        - RUC: 8 dígitos
        - Tipo documento: 2 dígitos
        - Establecimiento: 3 dígitos
        - Punto expedición: 3 dígitos
        - Número documento: 7 dígitos
        - Código seguridad: 8 dígitos
        - Fecha/hora: 11 dígitos (YYMMDDHHmm + random)
        """
        # RUC de la empresa (8 dígitos - extraer solo números)
        ruc_clean = "".join(filter(str.isdigit, str(company_ruc)))
        cdc = ruc_clean[:8].zfill(8)

        # Tipo de documento (2 dígitos)
        cdc += str(doc_type).zfill(2)

        # Establecimiento (3 dígitos)
        cdc += str(int(establishment)).zfill(3)

        # Punto de expedición (3 dígitos)
        cdc += str(int(expedition_point)).zfill(3)

        # Número del documento (7 dígitos)
        cdc += str(sequence).zfill(7)

        # Código de seguridad (8 dígitos) - generado aleatoriamente
        security_code = cls._generate_security_code()
        cdc += str(security_code).zfill(8)

        # Fecha y hora (11 dígitos)
        datetime_code = cls._generate_datetime_code(emission_date)
        cdc += datetime_code

        if len(cdc) != 42:
            raise ValueError(f"CDC base debe tener 42 dígitos, generado: {len(cdc)}")

        return cdc

    @classmethod
    def _generate_security_code(cls):
        """Generar código de seguridad aleatorio (8 dígitos)"""
        return secrets.randbelow(90000000) + 10000000

    @classmethod
    def _generate_datetime_code(cls, emission_date):
        """
        Generar código de fecha/hora (11 dígitos)

        Formato: YYMMDDHHmm + dígito aleatorio
        """
        date_str = emission_date.strftime("%y%m%d%H%M")  # 10 dígitos
        random_digit = secrets.randbelow(10)  # 1 dígito

        return date_str + str(random_digit)

    @classmethod
    def _calculate_check_digit(cls, cdc_base):
        """
        Calcular dígito verificador usando módulo 11

        Args:
            cdc_base (str): CDC base (42 dígitos)

        Returns:
            int: Dígito verificador (0-9)
        """
        if len(cdc_base) != 42:
            raise ValueError(
                f"CDC base debe tener 42 dígitos, recibido: {len(cdc_base)}"
            )

        # Calcular suma ponderada
        total = 0
        for i, digit in enumerate(cdc_base):
            multiplier = cls.MULTIPLIERS[i % len(cls.MULTIPLIERS)]
            total += int(digit) * multiplier

        # Calcular resto de la división por 11
        remainder = total % 11

        # Determinar dígito verificador
        if remainder < 2:
            return remainder
        else:
            return 11 - remainder

    @classmethod
    def validate_cdc(cls, cdc):
        """
        Validar formato y dígito verificador de un CDC

        Args:
            cdc (str): CDC a ser validado

        Returns:
            tuple: (is_valid, error_message)
        """
        if not cdc:
            return False, "CDC es obligatorio"

        # Verificar longitud
        if len(cdc) != 43:
            return False, f"CDC debe tener 43 dígitos, recibido: {len(cdc)}"

        # Verificar si contiene solo dígitos
        if not cdc.isdigit():
            return False, "CDC debe contener solo números"

        # Separar base y dígito verificador
        cdc_base = cdc[:42]
        check_digit = int(cdc[42])

        # Calcular dígito verificador esperado
        try:
            calculated_digit = cls._calculate_check_digit(cdc_base)
        except Exception as e:
            return False, f"Error al calcular DV: {str(e)}"

        if calculated_digit != check_digit:
            return (
                False,
                f"Dígito verificador inválido. "
                f"Esperado: {calculated_digit}, "
                f"Recibido: {check_digit}",
            )

        return True, ""

    @classmethod
    def parse_cdc(cls, cdc):
        """
        Extraer componentes del CDC

        Args:
            cdc (str): CDC completo (43 dígitos)

        Returns:
            dict: Diccionario con componentes del CDC
        """
        if len(cdc) != 43:
            raise ValueError(f"CDC debe tener 43 dígitos, recibido: {len(cdc)}")

        return {
            "ruc": cdc[0:8],
            "doc_type": cdc[8:10],
            "establishment": cdc[10:13],
            "expedition_point": cdc[13:16],
            "sequence": cdc[16:23],
            "security_code": cdc[23:31],
            "datetime_code": cdc[31:42],
            "check_digit": cdc[42],
        }

    @classmethod
    def format_cdc(cls, cdc, separator="-"):
        """
        Formatear CDC para visualización legible

        Args:
            cdc (str): CDC completo
            separator (str): Separador entre componentes

        Returns:
            str: CDC formateado
        """
        if len(cdc) != 43:
            return cdc

        components = cls.parse_cdc(cdc)

        return (
            f"{components['ruc']}{separator}"
            f"{components['doc_type']}{separator}"
            f"{components['establishment']}{separator}"
            f"{components['expedition_point']}{separator}"
            f"{components['sequence']}{separator}"
            f"{components['security_code']}{separator}"
            f"{components['datetime_code']}{separator}"
            f"{components['check_digit']}"
        )
