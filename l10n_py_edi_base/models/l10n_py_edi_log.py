# l10n_py_edi_base/models/l10n_py_edi_log.py

"""
Sistema de Logs Avançado para operações EDI
Implementa logging completo conforme propostas de melhoria
"""

import json
import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class EDILog(models.Model):
    """Modelo robusto para registrar logs de operações EDI"""

    _name = "l10n_py.edi.log"
    _description = "Log de Operações EDI Paraguay"
    _order = "create_date desc"
    _rec_name = "operation_type"

    # ============== IDENTIFICAÇÃO DA OPERAÇÃO ==============

    operation_type = fields.Selection(
        [
            ("send", "Envio de Documento"),
            ("status", "Consulta de Status"),
            ("cancel", "Cancelación"),
            ("event", "Evento"),
            ("download_pdf", "Download PDF"),
            ("download_xml", "Download XML"),
            ("validate", "Validação"),
        ],
        string="Tipo de Operação",
        required=True,
        index=True,
    )

    # ============== DOCUMENTOS RELACIONADOS ==============

    document_id = fields.Many2one(
        "account.move",
        string="Documento",
        ondelete="cascade",
        index=True,
        help="Documento fiscal relacionado",
    )

    cdc = fields.Char(string="CDC", index=True, help="Código de Control del documento")

    # ============== PROVEDOR EDI ==============

    provider = fields.Selection(
        [
            ("factpy", "FactPy"),
            ("facturasend", "FacturaSend"),
            ("sifen", "SIFEN Directo"),
            ("local", "Processamento Local"),
        ],
        string="Provedor",
        required=True,
        index=True,
    )

    # ============== DADOS DA REQUISIÇÃO ==============

    endpoint = fields.Char(help="URL ou endpoint da API")

    method = fields.Selection(
        [
            ("GET", "GET"),
            ("POST", "POST"),
            ("PUT", "PUT"),
            ("DELETE", "DELETE"),
            ("PATCH", "PATCH"),
        ],
        string="Método HTTP",
    )

    request_headers = fields.Text(
        string="Headers da Requisição", help="Headers HTTP enviados"
    )

    request_data = fields.Text(string="Dados Enviados", help="Payload da requisição")

    # ============== DADOS DA RESPOSTA ==============

    status_code = fields.Integer(
        string="Código de Status", help="Código de status HTTP"
    )

    response_headers = fields.Text(
        string="Headers da Resposta", help="Headers HTTP recebidos"
    )

    response_data = fields.Text(string="Resposta Recebida", help="Payload da resposta")

    # ============== MÉTRICAS ==============

    execution_time = fields.Float(
        string="Tempo de Execução (ms)",
        help="Tempo de execução em milissegundos",
        digits=(10, 2),
    )

    # ============== STATUS E ERRO ==============

    success = fields.Boolean(
        string="Sucesso",
        default=True,
        index=True,
        help="Indica se a operação foi bem-sucedida",
    )

    error_message = fields.Text(
        string="Mensagem de Erro", help="Descrição do erro se houver"
    )

    error_code = fields.Char(string="Código de Erro", help="Código de erro do provedor")

    # ============== DADOS ADICIONAIS ==============

    batch_id = fields.Char(
        string="ID do Lote", help="Identificador de lote do provedor"
    )

    retry_count = fields.Integer(
        string="Tentativas", default=0, help="Número de tentativas realizadas"
    )

    # ============== CAMPOS COMPUTADOS ==============

    error = fields.Boolean(
        string="É Erro",
        compute="_compute_error",
        store=True,
        help="Indica se houve erro na operação",
    )

    duration_human = fields.Char(
        string="Duração",
        compute="_compute_duration_human",
        help="Duração em formato legível",
    )

    # ============== MÉTODOS COMPUTE ==============

    @api.depends("status_code", "success")
    def _compute_error(self):
        """Computar se é erro baseado no status code e flag success"""
        for record in self:
            if record.status_code:
                record.error = record.status_code >= 400
            else:
                record.error = not record.success

    @api.depends("execution_time")
    def _compute_duration_human(self):
        """Formatar duração para exibição"""
        for record in self:
            if record.execution_time:
                if record.execution_time < 1000:
                    record.duration_human = f"{int(record.execution_time)} ms"
                else:
                    seconds = record.execution_time / 1000
                    record.duration_human = f"{round(seconds, 2)} s"
            else:
                record.duration_human = "N/A"

    # ============== MÉTODOS PÚBLICOS ==============

    @api.model
    def log_operation(
        self,
        operation_type,
        provider,
        document=None,
        request_data=None,
        response_data=None,
        execution_time=0,
        success=True,
        error_message=None,
        **kwargs,
    ):
        """
        Registrar operação EDI

        Args:
            operation_type (str): Tipo de operação
            provider (str): Provedor EDI
            document (account.move): Documento relacionado
            request_data (dict): Dados da requisição
            response_data (dict): Dados da resposta
            execution_time (float): Tempo de execução em ms
            success (bool): Se a operação foi bem-sucedida
            error_message (str): Mensagem de erro (se houver)
            **kwargs: Campos adicionais

        Returns:
            l10n_py.edi.log: Registro de log criado
        """
        try:
            # Preparar dados do log
            log_vals = {
                "operation_type": operation_type,
                "provider": provider,
                "execution_time": execution_time,
                "success": success,
                "error_message": error_message,
            }

            # Documento relacionado
            if document:
                log_vals["document_id"] = document.id
                log_vals["cdc"] = getattr(document, "l10n_py_cdc", False)

            # Dados da requisição
            if request_data:
                if isinstance(request_data, dict):
                    log_vals["request_data"] = json.dumps(
                        request_data, indent=2, ensure_ascii=False
                    )
                else:
                    log_vals["request_data"] = str(request_data)

            # Dados da resposta
            if response_data:
                if isinstance(response_data, dict):
                    response_json = json.dumps(
                        response_data, indent=2, ensure_ascii=False
                    )
                    # Limitar tamanho para evitar problemas
                    log_vals["response_data"] = response_json[:10000]
                else:
                    log_vals["response_data"] = str(response_data)[:10000]

            # Campos adicionais
            for key, value in kwargs.items():
                if key in self._fields:
                    log_vals[key] = value

            # Criar registro de log
            log_record = self.create(log_vals)

            # Log no sistema também
            if not success:
                _logger.error(
                    f"EDI Error [{provider}] {operation_type}: {error_message}"
                )
            else:
                _logger.info(
                    f"EDI Success [{provider}] {operation_type} "
                    f"({int(execution_time)}ms)"
                )

            return log_record

        except Exception as e:
            _logger.exception(f"Erro ao criar log EDI: {str(e)}")
            return False

    def action_view_document(self):
        """Abrir documento relacionado"""
        self.ensure_one()
        if not self.document_id:
            return False

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": self.document_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_retry_operation(self):
        """Repetir operação (se aplicável)"""
        self.ensure_one()

        if self.operation_type == "send" and self.document_id:
            # Incrementar contador de tentativas
            self.write({"retry_count": self.retry_count + 1})
            return self.document_id.action_send_edi()

        return False

    def action_view_request_data(self):
        """Exibir dados da requisição em formato legível"""
        self.ensure_one()
        return self._show_data_wizard("request", self.request_data)

    def action_view_response_data(self):
        """Exibir dados da resposta em formato legível"""
        self.ensure_one()
        return self._show_data_wizard("response", self.response_data)

    def _show_data_wizard(self, data_type, data):
        """Mostrar wizard com dados formatados"""
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Dados da %s") % data_type.capitalize(),
                "message": data or _("Sem dados"),
                "type": "info",
                "sticky": True,
            },
        }
