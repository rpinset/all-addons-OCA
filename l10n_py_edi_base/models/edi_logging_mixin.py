# l10n_py_edi_base/models/edi_logging_mixin.py

"""
Mixin para Logging Automático de Operações EDI
Facilita o logging consistente em todos os conectores
"""

import logging
import time
from contextlib import contextmanager

from odoo import models

_logger = logging.getLogger(__name__)


class EDILoggingMixin(models.AbstractModel):
    """Mixin para logging automático de operações EDI"""

    _name = "l10n_py.edi.logging.mixin"
    _description = "Mixin para Logging Automático EDI"

    @contextmanager
    def log_edi_operation(self, operation_type, provider, document=None, **kwargs):
        """
        Context manager para logging automático de operações EDI

        Usage:
            with self.log_edi_operation('send', 'factpy', document) as log_data:
                result = self.send_to_provider(data)
                log_data['response_data'] = result

        Args:
            operation_type (str): Tipo de operação
            provider (str): Provedor EDI
            document (account.move): Documento relacionado
            **kwargs: Dados adicionais para o log

        Yields:
            dict: Dicionário para adicionar dados durante a operação
        """
        start_time = time.time()
        log_data = {
            "operation_type": operation_type,
            "provider": provider,
            "document": document,
            **kwargs,
        }

        try:
            # Executar operação
            yield log_data

            # Operação bem-sucedida
            execution_time = (time.time() - start_time) * 1000
            self.env["l10n_py.edi.log"].log_operation(
                execution_time=execution_time, success=True, **log_data
            )

        except Exception as e:
            # Operação com erro
            execution_time = (time.time() - start_time) * 1000
            self.env["l10n_py.edi.log"].log_operation(
                execution_time=execution_time,
                success=False,
                error_message=str(e),
                **log_data,
            )
            # Re-raise a exceção
            raise

    def _log_success(
        self, operation_type, provider, document=None, execution_time=0, **kwargs
    ):
        """
        Log de operação bem-sucedida

        Args:
            operation_type (str): Tipo de operação
            provider (str): Provedor EDI
            document (account.move): Documento relacionado
            execution_time (float): Tempo de execução em ms
            **kwargs: Dados adicionais
        """
        return self.env["l10n_py.edi.log"].log_operation(
            operation_type=operation_type,
            provider=provider,
            document=document,
            execution_time=execution_time,
            success=True,
            **kwargs,
        )

    def _log_error(
        self,
        operation_type,
        provider,
        error_message,
        document=None,
        execution_time=0,
        **kwargs,
    ):
        """
        Log de operação com erro

        Args:
            operation_type (str): Tipo de operação
            provider (str): Provedor EDI
            error_message (str): Mensagem de erro
            document (account.move): Documento relacionado
            execution_time (float): Tempo de execução em ms
            **kwargs: Dados adicionais
        """
        return self.env["l10n_py.edi.log"].log_operation(
            operation_type=operation_type,
            provider=provider,
            document=document,
            execution_time=execution_time,
            success=False,
            error_message=error_message,
            **kwargs,
        )
