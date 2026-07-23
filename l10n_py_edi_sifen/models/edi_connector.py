# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import logging
import re
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
from odoo.addons.l10n_py_edi_base.services.qr_generator import QRGenerator

from ..services.rde_builder import RDeBuilder

_logger = logging.getLogger(__name__)

# Namespace del SIFEN. El rDE debe ir en el namespace POR DEFECTO (sin prefijo);
# de lo contrario el SET rechaza con "[0100] XML con Prefijo no reconocido".
_SIFEN_NS = "http://ekuatia.set.gov.py/sifen/xsd"

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

    # CSC (Código de Seguridad del Contribuyente) — necesario para el QR.
    # Lo entrega la SET y es DISTINTO por ambiente (homologación vs producción);
    # por eso vive en el conector, que ya define el ambiente.
    l10n_py_csc = fields.Char(
        string="CSC",
        help="Código de Seguridad del Contribuyente entregado por la SET. "
        "Distinto por ambiente (homologación vs producción).",
    )
    l10n_py_idcsc = fields.Char(
        string="ID CSC",
        default="0001",
        help="Identificador del CSC (ej. 0001).",
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

    def preview_qr(self, invoice_data):
        if self.provider_type != "sifen":
            return super().preview_qr(invoice_data)
        return self._sifen_preview_qr(invoice_data)

    def test_connection(self):
        if self.provider_type != "sifen":
            return super().test_connection()
        return self._sifen_test_connection()

    # === Private SIFEN methods ===

    def _sifen_send_document(self, invoice_data):
        """Firma el DE, inyecta el QR y transmite al SIFEN por SOAP/mTLS.

        Implementa la transmisión directamente (no usa pysifen.enviar_de, que
        no coloca el DE firmado en el cuerpo SOAP). El dCarQR vive en gCamFuFD,
        FUERA del <DE> firmado, por lo que inyectarlo no invalida la firma.
        """
        self.ensure_one()
        rde = self._sifen_build_rde(invoice_data)
        transmissao = self._sifen_get_transmissao_de()
        try:
            # 1) Serializar (namespace por defecto) y firmar el DE.
            xml_de = self._sifen_serialize_rde(rde)
            signed_xml = transmissao._sign_xml(xml_de, rde.DE.Id)
            # 2) Construir el dCarQR a partir del XML firmado e inyectarlo.
            qr_link = self._sifen_qr_link_from_signed(signed_xml)
            if qr_link:
                signed_xml = self._sifen_inject_dcarqr(signed_xml, qr_link)
            # 3) Transmitir el XML firmado (con QR) al SIFEN.
            cert_path, key_path = transmissao._get_cert_files()
            raw = self._sifen_recibe(signed_xml, cert_path, key_path)
            return self._sifen_build_recibe_response(
                raw, rde.DE.Id, signed_xml, qr_link
            )
        except Exception as e:
            _logger.error("SIFEN send error: %s", str(e))
            return {"success": False, "error": str(e)}
        finally:
            transmissao.cleanup()

    def _sifen_recibe(self, signed_xml, cert_path, key_path):
        """POST del DE firmado al WS síncrono de recepción (SOAP 1.2 + mTLS)."""
        import time

        import requests
        from pysifen.transmissao.config import get_endpoint

        url = get_endpoint(self._sifen_get_ambiente(), "recep_de")
        # Quitar la declaración <?xml ...?> del rDE firmado (va dentro de xDE).
        rde_xml = signed_xml
        stripped = rde_xml.lstrip()
        if stripped.startswith("<?xml"):
            rde_xml = stripped[stripped.find("?>") + 2 :].lstrip()
        did = int(time.time() * 1000) % 999999999999999
        envelope = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<env:Envelope xmlns:env="http://www.w3.org/2003/05/soap-envelope">'
            "<env:Header/><env:Body>"
            '<rEnviDe xmlns="http://ekuatia.set.gov.py/sifen/xsd">'
            f"<dId>{did}</dId><xDE>{rde_xml}</xDE>"
            "</rEnviDe></env:Body></env:Envelope>"
        )
        resp = requests.post(
            url,
            data=envelope.encode("utf-8"),
            headers={
                "Content-Type": "application/xml; charset=utf-8",
                "User-Agent": "odoo-l10n-py-edi",
            },
            cert=(cert_path, key_path),
            timeout=90,
        )
        # El SET responde los errores de validación con HTTP 400 y, a veces,
        # Content-Type text/html, pero el cuerpo es un SOAP válido
        # (rRetEnviDe/gResProc). Parseamos por contenido: si el cuerpo es XML
        # lo devolvemos; sólo abortamos si no lo es.
        body = resp.content or b""
        if body.lstrip().startswith(b"<"):
            return body
        resp.raise_for_status()
        return body

    def _sifen_inject_dcarqr(self, signed_xml, qr_link):
        """Añade gCamFuFD/dCarQR al final del rDE (después de la firma).

        Se firma sin gCamFuFD para respetar el orden DE → Signature → gCamFuFD
        del XSD; aquí se inserta el bloque justo antes de </rDE>. El '&' del
        enlace se escapa a '&amp;' (el resto de la URL no tiene caracteres XML).
        Como gCamFuFD está FUERA del <DE> firmado, no invalida la firma.
        """
        escaped = qr_link.replace("&", "&amp;")
        bloque = f"<gCamFuFD><dCarQR>{escaped}</dCarQR></gCamFuFD>"
        new_xml, count = re.subn(
            r"</((?:[\w.-]+:)?rDE)>",
            lambda m: bloque + m.group(0),
            signed_xml,
            count=1,
        )
        return new_xml if count else signed_xml

    def _sifen_build_recibe_response(self, raw, cdc, signed_xml, qr_link):
        """Parsea la respuesta rRetEnviDe/rProtDE y arma el dict estándar."""
        from lxml import etree

        root = etree.fromstring(raw)

        def text(name):
            nodes = root.xpath(f"//*[local-name()='{name}']")
            return nodes[0].text if nodes and nodes[0].text else ""

        estado = text("dEstRes")  # "Aprobado" / "Rechazado"
        if estado == "Aprobado":
            return {
                "success": True,
                "result": {
                    "deList": [
                        {
                            "cdc": text("Id") or cdc,
                            "xml": signed_xml,
                            "qr": qr_link,
                            "protocol": text("dProtAut"),
                        }
                    ]
                },
            }
        errors = []
        for proc in root.xpath("//*[local-name()='gResProc']"):
            cod = proc.xpath("./*[local-name()='dCodRes']/text()")
            msg = proc.xpath("./*[local-name()='dMsgRes']/text()")
            errors.append(f"[{cod[0] if cod else ''}] {msg[0] if msg else ''}")
        return {"success": False, "error": "\n".join(errors) or "Error SIFEN"}

    def _sifen_preview_qr(self, invoice_data):
        """Construye CDC + dCarQR firmando localmente, SIN transmitir."""
        self.ensure_one()
        rde = self._sifen_build_rde(invoice_data)
        transmissao = self._sifen_get_transmissao_de()
        try:
            qr_link = self._sifen_build_qr_link(rde, invoice_data, transmissao)
            return {"cdc": rde.DE.Id, "qr": qr_link}
        finally:
            transmissao.cleanup()

    def _sifen_qr_values_from_signed_xml(self, signed_xml):
        """Extrae del XML FIRMADO los valores del QR.

        Lee exactamente los mismos campos que la librería oficial de la SET
        (facturacionelectronicapy-qrgen), garantizando paridad con el documento.
        """
        from lxml import etree

        root = etree.fromstring(signed_xml.encode("utf-8"))

        def first(name):
            nodes = root.xpath(f"//*[local-name()='{name}']")
            return nodes[0] if nodes else None

        def text(name, default=""):
            node = first(name)
            if node is not None and node.text is not None:
                return node.text
            return default

        de = first("DE")
        nat_rec = text("iNatRec")
        return {
            "cdc": de.get("Id") if de is not None else "",
            "emission_date": text("dFeEmiDE"),
            "receptor_ruc": text("dRucRec") if nat_rec == "1" else None,
            "receptor_doc_number": (None if nat_rec == "1" else text("dNumIDRec", "0")),
            "total_operation": text("dTotGralOpe", "0"),
            "total_iva": text("dTotIVA", "0"),
            "item_count": len(root.xpath("//*[local-name()='gCamItem']")),
            "digest_value": text("DigestValue") or None,
        }

    def _sifen_qr_link_from_signed(self, signed_xml):
        """Construye el enlace dCarQR a partir de un XML ya firmado.

        Lee del XML firmado los mismos campos que la librería oficial de la SET
        (totales, receptor, ítems, DigestValue), garantizando paridad con el
        documento. Devuelve el enlace o False si falta el CSC o el digest.
        """
        if not self.l10n_py_csc or not self.l10n_py_idcsc:
            _logger.warning(
                "CSC/IdCSC no configurado en el conector EDI; se omite el QR."
            )
            return False
        vals = self._sifen_qr_values_from_signed_xml(signed_xml)
        if not vals.get("digest_value"):
            _logger.warning("No se encontró DigestValue en el XML firmado.")
            return False
        return QRGenerator.build_qr_link(
            cdc=vals["cdc"],
            emission_date=vals["emission_date"],
            digest_value=vals["digest_value"],
            idcsc=self.l10n_py_idcsc,
            csc=self.l10n_py_csc,
            total_operation=vals["total_operation"],
            total_iva=vals["total_iva"],
            item_count=vals["item_count"],
            receptor_ruc=vals["receptor_ruc"],
            receptor_doc_number=vals["receptor_doc_number"],
            is_test=self.environment != "prod",
        )

    def _sifen_build_qr_link(self, rde, invoice_data, transmissao):
        """Firma el DE y devuelve el enlace dCarQR (usado por la previsualización)."""
        try:
            xml_de = self._sifen_serialize_rde(rde)
            signed_xml = transmissao._sign_xml(xml_de, rde.DE.Id)
        except Exception as exc:
            _logger.warning("No se pudo firmar el DE para el QR: %s", exc)
            return False
        return self._sifen_qr_link_from_signed(signed_xml)

    def _sifen_serialize_rde(self, rde):
        """Serializa el rDE con el namespace SIFEN POR DEFECTO (sin prefijo).

        pysifen serializa con prefijo (ns0:), que el SET rechaza. Forzamos el
        prefijo None para obtener <rDE xmlns="...sifen/xsd">.
        """
        serializer = XmlSerializer(
            config=SerializerConfig(xml_declaration=True, encoding="UTF-8")
        )
        xml = serializer.render(rde, ns_map={None: _SIFEN_NS})
        # El rDE trae un <Signature> placeholder vacío (el binding lo exige).
        # Hay que quitarlo antes de firmar; si no, signxml AGREGA otra firma y
        # el SET rechaza con "[0140] ... más de una firma".
        xml = re.sub(
            r"<(?:[\w.-]+:)?Signature[\s>].*?</(?:[\w.-]+:)?Signature>",
            "",
            xml,
            count=1,
            flags=re.DOTALL,
        )
        # Quitar gCamFuFD antes de firmar: signxml AGREGA la firma al FINAL del
        # rDE, y el XSD exige el orden DE → Signature → gCamFuFD. Por eso se
        # firma sin gCamFuFD (queda DE, Signature) y luego se reinyecta el
        # gCamFuFD/dCarQR DESPUÉS de la firma (ver _sifen_inject_dcarqr).
        xml = re.sub(
            r"<(?:[\w.-]+:)?gCamFuFD[\s>].*?</(?:[\w.-]+:)?gCamFuFD>",
            "",
            xml,
            count=1,
            flags=re.DOTALL,
        )
        xml = re.sub(r"<(?:[\w.-]+:)?gCamFuFD\s*/>", "", xml, count=1)
        # El SET exige el schema declarado en el rDE; si no: "[0160] No se
        # informó el schema en el XML". (Son atributos del rDE, fuera del <DE>
        # firmado, así que no afectan la firma.)
        xml = re.sub(
            r"(<rDE\b[^>]*?)>",
            r'\1 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
            r' xsi:schemaLocation="http://ekuatia.set.gov.py/sifen/xsd'
            r' siRecepDE_v150.xsd">',
            xml,
            count=1,
        )
        return xml

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
        """Build RDe from invoice data using RDeBuilder.

        Genera el código de seguridad y la fecha UNA sola vez y los comparte
        entre el CDC y el XML (gOpeDE/dCodSeg, gDatGralOpe/dFeEmiDE); de lo
        contrario el SET rechaza con "[0160] CDC Inválido".
        """
        company = self.company_id
        company_data = self._sifen_prepare_company_data()
        doc_type = invoice_data.get("tipoDocumento", 1)
        establishment = invoice_data.get("establecimiento", "001")
        punto = invoice_data.get("punto", "001")
        numero = invoice_data.get("numero", "0000001")

        # Valores compartidos CDC <-> XML
        cod_seg = invoice_data.get("codigoSeguridadAleatorio")
        if not cod_seg or len(str(cod_seg)) != 9 or not str(cod_seg).isdigit():
            cod_seg = CDCGenerator.generate_security_code()
        invoice_data["codigoSeguridadAleatorio"] = cod_seg

        fecha = invoice_data.get("fecha")
        if not fecha:
            fecha = fields.Datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        invoice_data["fecha"] = fecha

        tipo_emision = invoice_data.get("tipoEmision", 1)

        cdc = CDCGenerator.generate(
            doc_type=doc_type,
            ruc=company.l10n_py_ruc,
            dv=company.l10n_py_dv,
            establishment=establishment,
            expedition_point=punto,
            sequence=int(numero),
            taxpayer_type=company_data.get("tipoContribuyente", "2"),
            emission_date=fecha,
            emission_type=tipo_emision,
            security_code=cod_seg,
        )
        return RDeBuilder(invoice_data, company_data, cdc).build()

    @staticmethod
    def _sifen_norm(text):
        """Normaliza para el catálogo del SET: sin acentos, MAYÚSCULAS.

        dDesDepEmi se valida contra el enum del SET (ej. "ALTO PARANA", sin
        acento); las demás descripciones también van sin acentos.
        """
        import unicodedata

        if not text:
            return ""
        nfkd = unicodedata.normalize("NFKD", str(text))
        return "".join(c for c in nfkd if not unicodedata.combining(c)).upper().strip()

    def _sifen_prepare_company_data(self):
        """Prepare company data dict for RDeBuilder."""
        company = self.company_id
        partner = company.partner_id
        # cDisEmi es opcional (minOccurs=0): si no hay distrito válido, se omite.
        distrito = company.l10n_py_district_code or None
        phone = "".join(filter(str.isdigit, partner.phone or ""))
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
            "departamentoDescripcion": self._sifen_norm(
                partner.state_id.name if partner.state_id else ""
            ),
            "distrito": distrito,
            "ciudad": company.l10n_py_city_code or "",
            "ciudadDescripcion": self._sifen_norm(partner.city or ""),
            "telefono": phone,
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
