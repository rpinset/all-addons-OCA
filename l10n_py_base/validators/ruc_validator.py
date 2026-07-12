# l10n_py_base/validators/ruc_validator.py

"""
Validador robusto para RUC paraguaio
Implementa validação completa conforme especificações da SET (Módulo 11)
"""

import logging
import re

_logger = logging.getLogger(__name__)


class RUCValidator:
    """Validador robusto para RUC paraguaio"""

    # Pesos cíclicos para cálculo do dígito verificador (Módulo 11 SET)
    WEIGHTS = [2, 3, 4, 5, 6, 7, 8, 9]

    @classmethod
    def validate(cls, ruc):
        """
        Validação completa de RUC paraguaio

        Args:
            ruc (str): RUC a ser validado

        Returns:
            tuple: (is_valid, error_message)
        """
        if not ruc:
            return False, "RUC é obrigatório"

        # Limpar caracteres especiais
        clean_ruc = re.sub(r"[^\d-]", "", ruc)

        # Verificar formato básico (aceita com ou sem hífen)
        if not re.match(r"^\d{6,8}(-\d)?$", clean_ruc):
            return False, "Formato inválido. Use: XXXXXXX-D ou XXXXXXX"

        # Separar RUC e dígito verificador se houver hífen
        if "-" in clean_ruc:
            ruc_number, check_digit = clean_ruc.split("-")
        else:
            # Se não houver hífen, assume que o último dígito é o DV
            if len(clean_ruc) >= 7:
                ruc_number = clean_ruc[:-1]
                check_digit = clean_ruc[-1]
            else:
                ruc_number = clean_ruc
                check_digit = None

        # Validar comprimento
        if len(ruc_number) < 6 or len(ruc_number) > 8:
            return False, "RUC deve ter entre 6 e 8 dígitos"

        # Calcular dígito verificador esperado
        calculated_digit = cls._calculate_check_digit(ruc_number)

        # Se um DV foi fornecido, validá-lo
        if check_digit is not None:
            if str(calculated_digit) != check_digit:
                return (
                    False,
                    f"Dígito verificador inválido. "
                    f"Esperado: {calculated_digit}, "
                    f"Recebido: {check_digit}",
                )

        return True, ""

    @classmethod
    def _calculate_check_digit(cls, ruc_number):
        """
        Calcular dígito verificador usando Módulo 11 (SET Paraguay)

        Algoritmo:
        1. Preenche o RUC com zeros à esquerda até 9 dígitos
        2. Aplica pesos [2,3,4,5,6,7,8,9] ciclicamente da esquerda para direita
        3. Encontra DV (0-9) tal que a soma ponderada total (incluindo DV)
           mod 11 == 0

        Verificação: RUC 80012345 → DV 6, RUC 4588955 → DV 1

        Args:
            ruc_number (str): Número do RUC sem dígito verificador

        Returns:
            int: Dígito verificador calculado
        """
        # Preencher com zeros à esquerda até 9 dígitos
        ruc_padded = ruc_number.zfill(9)

        # Calcular soma ponderada parcial (9 dígitos do RUC)
        partial_sum = 0
        for i, digit in enumerate(ruc_padded):
            partial_sum += int(digit) * cls.WEIGHTS[i % 8]

        # O DV fica na posição 9 (índice 9), com peso = WEIGHTS[9 % 8] = WEIGHTS[1] = 3
        # Encontrar DV tal que (partial_sum + DV * 3) % 11 == 0
        # Usando inverso modular: inv(3, 11) = 4 (pois 3*4 = 12 ≡ 1 mod 11)
        remainder = partial_sum % 11
        dv = ((11 - remainder) % 11 * 4) % 11

        # DV deve ser dígito único (0-9)
        if dv >= 10:
            dv = 0

        return dv

    @classmethod
    def format_ruc(cls, ruc, include_dv=True):
        """
        Formatar RUC para exibição padronizada

        Args:
            ruc (str): RUC a ser formatado
            include_dv (bool): Se True, inclui o dígito verificador

        Returns:
            str: RUC formatado (XXXXXXX-D)
        """
        # Limpar formato
        clean_ruc = re.sub(r"[^\d]", "", ruc)

        if len(clean_ruc) < 6:
            return ruc  # Retorna original se muito curto

        # Se o último dígito pode ser DV, separar
        if len(clean_ruc) >= 7:
            ruc_number = clean_ruc[:-1]
            existing_dv = clean_ruc[-1]

            # Validar se o DV está correto
            calculated_dv = cls._calculate_check_digit(ruc_number)

            if str(calculated_dv) == existing_dv:
                # DV correto, usar o fornecido
                if include_dv:
                    return f"{ruc_number}-{existing_dv}"
                else:
                    return ruc_number
            else:
                # DV incorreto ou não existe, calcular
                if include_dv:
                    new_dv = cls._calculate_check_digit(clean_ruc)
                    return f"{clean_ruc}-{new_dv}"
                else:
                    return clean_ruc
        else:
            # Sem DV, calcular
            if include_dv:
                dv = cls._calculate_check_digit(clean_ruc)
                return f"{clean_ruc}-{dv}"
            else:
                return clean_ruc

    @classmethod
    def get_ruc_number(cls, ruc):
        """
        Extrair apenas o número do RUC (sem DV)

        Args:
            ruc (str): RUC completo

        Returns:
            str: Número do RUC sem DV
        """
        clean_ruc = re.sub(r"[^\d]", "", ruc)

        if not clean_ruc:
            return ""

        # Se tiver DV (7-9 dígitos), remover último dígito
        if len(clean_ruc) >= 7:
            # Verificar se o último dígito é um DV válido
            ruc_number = clean_ruc[:-1]
            check_digit = clean_ruc[-1]
            calculated_digit = cls._calculate_check_digit(ruc_number)

            if str(calculated_digit) == check_digit:
                return ruc_number
            else:
                # Não é um DV válido, retornar completo
                return clean_ruc
        else:
            return clean_ruc

    @classmethod
    def get_check_digit(cls, ruc):
        """
        Obter o dígito verificador do RUC

        Args:
            ruc (str): RUC (com ou sem DV)

        Returns:
            str: Dígito verificador
        """
        ruc_number = cls.get_ruc_number(ruc)
        return str(cls._calculate_check_digit(ruc_number))

    @classmethod
    def is_valid_format(cls, ruc):
        """
        Verificar se o formato do RUC é válido (sem validar DV)

        Args:
            ruc (str): RUC a validar

        Returns:
            bool: True se o formato é válido
        """
        if not ruc:
            return False

        # RUC deve conter apenas dígitos e opcionalmente um hífen
        if not re.match(r"^[\d-]+$", ruc):
            return False

        clean_ruc = re.sub(r"[^\d]", "", ruc)

        # Deve ter entre 6 e 9 dígitos (6-8 para RUC + 1 para DV)
        if len(clean_ruc) < 6 or len(clean_ruc) > 9:
            return False

        return True

    @classmethod
    def normalize(cls, ruc):
        """
        Normalizar RUC para formato padronizado

        Args:
            ruc (str): RUC em qualquer formato

        Returns:
            str: RUC normalizado (XXXXXXX-D)
        """
        if not ruc:
            return ""

        is_valid, error = cls.validate(ruc)

        if not is_valid:
            _logger.warning(f"RUC inválido: {ruc} - {error}")
            return ruc  # Retorna original se inválido

        return cls.format_ruc(ruc, include_dv=True)
