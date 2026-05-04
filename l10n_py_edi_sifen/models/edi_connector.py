# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import logging
from datetime import datetime

from pysifen.de.bindings.v150.evento_types_v150 import TiTiDeev
from pysifen.de.bindings.v150.evento_v150 import (
    TgGroupEvt,
    TgGroupGesEve,
    TrEve,
    TrGesEve,
    TrGeVeCan,
    TrGeVeInu,
)
from pysifen.de.bindings.v150.xmldsig_core_schema import (
    CanonicalizationMethod,
    Signature,
    SignatureMethod,
    SignatureValue,
    SignedInfo,
)
from pysifen.transmissao import ConsultaSIFEN, TransmissaoDE, TransmissaoEvento
from pysifen.transmissao.config import PRODUCCION, TEST
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from odoo import _, fields, models
from odoo.exceptions import UserError

from odoo.addons.l10n_py_edi_base.services.cdc_generator import CDCGenerator

from ..services.rde_builder import RDeBuilder

_logger = logging.getLogger(__name__)

# Map document type code → TiTiDeev enum for inutilization events
_DOC_TYPE_TO_EVENTO = {
    1: TiTiDeev.VALUE_1,
    4: TiTiDeev.VALUE_4,
    5: TiTiDeev.VALUE_5,
    6: TiTiDeev.VALUE_6,
}


class EDIConnector(models.Model):
    _inherit = "l10n_py.edi.connector"

    provider_type = fields.Selection(
        selection_add=[("sifen", "SIFEN Directo")],
        ondelete={"sifen": "cascade"},
    )

    # === Override public interface ===

    def send_document(self, invoice_data):
        if self.provider_type != "sifen":
            return super().send_document(invoice_data)
        return self._sifen_send_document(invoice_data)

    def check_status(self, document_id):
        if self.provider_type != "sifen":
            return super().check_status(document_id)
        return self._sifen_check_status(document_id)

    def cancel_document(self, document_id, reason=""):
        if self.provider_type != "sifen":
            return super().cancel_document(document_id, reason)
        return self._sifen_cancel_document(document_id, reason)

    def inutilize_range(self, data):
        if self.provider_type != "sifen":
            return super().inutilize_range(data)
        return self._sifen_inutilize_range(data)

    def preview_document(self, invoice_data):
        if self.provider_type != "sifen":
            return super().preview_document(invoice_data)
        return self._sifen_preview_document(invoice_data)

    def test_connection(self):
        if self.provider_type != "sifen":
            return super().test_connection()
        return self._sifen_test_connection()

    # === Private SIFEN methods ===

    def _sifen_send_document(self, invoice_data):
        """Build RDe, sign, and send via SOAP/mTLS."""
        self.ensure_one()
        rde = self._sifen_build_rde(invoice_data)
        transmissao = self._sifen_get_transmissao_de()
        try:
            result = transmissao.enviar_de(rde, sign=True)
            return self._sifen_process_response(result, rde)
        except Exception as e:
            _logger.error("SIFEN send error: %s", str(e))
            return {"success": False, "error": str(e)}
        finally:
            transmissao.cleanup()

    def _sifen_check_status(self, cdc):
        """Check document status via SIFEN consultation."""
        self.ensure_one()
        consulta = self._sifen_get_consulta()
        try:
            result = consulta.consultar_de(cdc)
            if hasattr(result, "rProtDe") and result.rProtDe:
                estado = getattr(result.rProtDe, "dEstRes", "")
                return {
                    "success": estado == "Aprobado",
                    "result": {"status": estado, "cdc": cdc},
                }
            return {"success": False, "error": "Sin respuesta del SIFEN"}
        except Exception as e:
            _logger.error("SIFEN check_status error: %s", str(e))
            return {"success": False, "error": str(e)}
        finally:
            consulta.cleanup()

    def _sifen_cancel_document(self, cdc, reason=""):
        """Cancel document via SIFEN cancellation event (TrGeVeCan)."""
        self.ensure_one()
        evento = self._sifen_get_evento()
        try:
            cancel_event = TrGeVeCan(
                Id=cdc,
                mOtEve=reason or "Cancelación solicitada por el emisor",
            )
            now_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            empty_signature = Signature(
                SignedInfo=SignedInfo(
                    CanonicalizationMethod=CanonicalizationMethod(Algorithm=""),
                    SignatureMethod=SignatureMethod(Algorithm=""),
                ),
                SignatureValue=SignatureValue(),
            )
            r_eve = TrEve(
                dFecFirma=now_str,
                dVerFor="150",
                gGroupTiEvt=TgGroupEvt(rGeVeCan=cancel_event),
                Id="1",
            )
            r_ges_eve = TrGesEve(rEve=r_eve, Signature=empty_signature)
            grupo = TgGroupGesEve(rGesEve=[r_ges_eve])

            result = evento.enviar_evento(grupo)
            _logger.info("SIFEN cancel result for CDC %s: %s", cdc, result)

            if hasattr(result, "gResProcEVe") and result.gResProcEVe:
                proc = result.gResProcEVe
                if hasattr(proc, "dEstRes") and proc.dEstRes == "Aprobado":
                    return {"success": True}
                error_msg = getattr(proc, "dMsgRes", "Error desconocido")
                return {"success": False, "error": error_msg}

            return {"success": False, "error": "Sin respuesta del SIFEN"}
        except Exception as e:
            _logger.error("SIFEN cancel error: %s", str(e))
            return {"success": False, "error": str(e)}
        finally:
            evento.cleanup()

    def _sifen_inutilize_range(self, data):
        """Inutilize document number range via SIFEN event (TrGeVeInu)."""
        self.ensure_one()
        evento = self._sifen_get_evento()
        try:
            doc_type = data.get("tipoDocumento", 1)
            inu_event = TrGeVeInu(
                dNumTim=data.get("timbrado", ""),
                dEst=data.get("establecimiento", "001"),
                dPunExp=data.get("punto", "001"),
                dNumIn=data.get("numeroDesde", "0000001"),
                dNumFin=data.get("numeroHasta", "0000001"),
                iTiDE=_DOC_TYPE_TO_EVENTO.get(doc_type, TiTiDeev.VALUE_1),
                mOtEve=data.get("motivo", "Inutilización de números"),
            )
            now_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            empty_signature = Signature(
                SignedInfo=SignedInfo(
                    CanonicalizationMethod=CanonicalizationMethod(Algorithm=""),
                    SignatureMethod=SignatureMethod(Algorithm=""),
                ),
                SignatureValue=SignatureValue(),
            )
            r_eve = TrEve(
                dFecFirma=now_str,
                dVerFor="150",
                gGroupTiEvt=TgGroupEvt(rGeVeInu=inu_event),
                Id="1",
            )
            r_ges_eve = TrGesEve(rEve=r_eve, Signature=empty_signature)
            grupo = TgGroupGesEve(rGesEve=[r_ges_eve])

            result = evento.enviar_evento(grupo)
            _logger.info("SIFEN inutilize result: %s", result)

            if hasattr(result, "gResProcEVe") and result.gResProcEVe:
                proc = result.gResProcEVe
                if hasattr(proc, "dEstRes") and proc.dEstRes == "Aprobado":
                    return {"success": True}
                error_msg = getattr(proc, "dMsgRes", "Error desconocido")
                return {"success": False, "error": error_msg}

            return {"success": False, "error": "Sin respuesta del SIFEN"}
        except Exception as e:
            _logger.error("SIFEN inutilize error: %s", str(e))
            return {"success": False, "error": str(e)}
        finally:
            evento.cleanup()

    def _sifen_test_connection(self):
        """Test mTLS connection by querying company RUC."""
        self.ensure_one()
        consulta = self._sifen_get_consulta()
        try:
            result = consulta.consultar_ruc(self.company_id.l10n_py_ruc)
            _logger.info("SIFEN test_connection result: %s", result)
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Conexión Exitosa"),
                    "message": _("La conexión con SIFEN fue verificada correctamente."),
                    "type": "success",
                    "sticky": False,
                },
            }
        except Exception as e:
            raise UserError(_("Error de conexión con SIFEN: %s") % str(e)) from e
        finally:
            consulta.cleanup()

    # === pysifen helpers ===

    def _sifen_get_ambiente(self):
        return PRODUCCION if self.environment == "prod" else TEST

    def _sifen_get_pkcs12(self):
        return self.company_id._get_pkcs12_data()

    def _sifen_get_transmissao_de(self):
        cert, pwd = self._sifen_get_pkcs12()
        return TransmissaoDE(self._sifen_get_ambiente(), cert, pwd)

    def _sifen_get_consulta(self):
        cert, pwd = self._sifen_get_pkcs12()
        return ConsultaSIFEN(self._sifen_get_ambiente(), cert, pwd)

    def _sifen_get_evento(self):
        cert, pwd = self._sifen_get_pkcs12()
        return TransmissaoEvento(self._sifen_get_ambiente(), cert, pwd)

    def _sifen_preview_document(self, invoice_data):
        """Build RDe and serialize to XML without signing or sending."""
        self.ensure_one()
        rde = self._sifen_build_rde(invoice_data)
        config = SerializerConfig(pretty_print=True, xml_declaration=True)
        serializer = XmlSerializer(config=config)
        ns_map = {
            "": "http://ekuatia.set.gov.py/sifen/xsd",
            "ds": "http://www.w3.org/2000/09/xmldsig#",
        }
        return serializer.render(rde, ns_map=ns_map)

    def _sifen_build_rde(self, invoice_data):
        """Build RDe from invoice data using RDeBuilder."""
        company = self.company_id
        doc_type = invoice_data.get("tipoDocumento", 1)
        establishment = invoice_data.get("establecimiento", "001")
        punto = invoice_data.get("punto", "001")
        numero = invoice_data.get("numero", "0000001")

        cdc = CDCGenerator.generate(
            company_ruc=company.l10n_py_ruc,
            doc_type=doc_type,
            establishment=establishment,
            expedition_point=punto,
            sequence=int(numero),
        )

        company_data = self._sifen_prepare_company_data()
        return RDeBuilder(invoice_data, company_data, cdc).build()

    def _sifen_prepare_company_data(self):
        """Prepare company data dict for RDeBuilder."""
        company = self.company_id
        partner = company.partner_id
        return {
            "ruc": company.l10n_py_ruc,
            "dv": company.l10n_py_dv,
            "tipoContribuyente": "2" if partner.is_company else "1",
            "razonSocial": company.name,
            "nombreFantasia": company.l10n_py_trade_name or company.name,
            "actividadEconomicaCodigo": (company.l10n_py_economic_activity_code or ""),
            "actividadEconomica": company.l10n_py_economic_activity or "",
            "direccion": partner.street or "",
            "numeroCasa": (
                partner.street_number if hasattr(partner, "street_number") else "0"
            )
            or "0",
            "departamento": company.l10n_py_department_code or 1,
            "departamentoDescripcion": (
                partner.state_id.name if partner.state_id else ""
            ),
            "distrito": company.l10n_py_district_code or 0,
            "ciudad": company.l10n_py_city_code or "",
            "ciudadDescripcion": partner.city or "",
            "telefono": partner.phone or "",
            "email": partner.email or "",
        }

    def _sifen_process_response(self, result, rde):
        """Process RRetEnviDe into standard response dict."""
        signed_xml = ""
        if hasattr(rde, "to_xml"):
            signed_xml = rde.to_xml()

        if (
            hasattr(result, "rProtDe")
            and result.rProtDe
            and getattr(result.rProtDe, "dEstRes", "") == "Aprobado"
        ):
            return {
                "success": True,
                "result": {
                    "deList": [
                        {
                            "cdc": getattr(result.rProtDe, "Id", ""),
                            "xml": signed_xml,
                        }
                    ],
                },
            }

        errors = []
        if hasattr(result, "rProtDe") and result.rProtDe:
            if hasattr(result.rProtDe, "gResProc"):
                for proc in result.rProtDe.gResProc:
                    errors.append(
                        f"[{getattr(proc, 'dCodRes', '')}] "
                        f"{getattr(proc, 'dMsgRes', '')}"
                    )
        return {"success": False, "error": "\n".join(errors) or "Error SIFEN"}
