# l10n_py_edi_base/models/account_move.py

import logging
import re
import secrets
import string
from typing import ClassVar

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.binary import BinaryBytes

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    # ============== CAMPOS EDI PARAGUAY ==============

    l10n_py_emission_type = fields.Selection(
        [("1", "Normal"), ("2", "Contingencia")],
        string="Tipo de Emisión",
        default="1",
        required=True,
    )

    l10n_py_transaction_type = fields.Selection(
        [
            ("1", "Venta de mercadería"),
            ("2", "Prestación de servicios"),
            ("3", "Mixto (Venta de mercadería y servicios)"),
            ("4", "Venta de activo fijo"),
            ("5", "Venta de divisas"),
            ("6", "Compra de divisas"),
            ("7", "Promoción o entrega de muestras"),
            ("8", "Donación"),
            ("9", "Anticipo"),
            ("10", "Compra de productos"),
            ("11", "Compra de servicios"),
            ("12", "Venta de crédito fiscal"),
            ("13", "Compra de crédito fiscal"),
        ],
        string="Tipo de Transacción",
        required=True,
        default="1",
    )

    l10n_py_presence_type = fields.Selection(
        [
            ("1", "Operación presencial"),
            ("2", "Operación electrónica"),
            ("3", "Operación telemarketing"),
            ("4", "Venta a domicilio"),
            ("5", "Operación bancaria"),
        ],
        string="Tipo de Presencia",
        default="1",
    )

    # Campos de respuesta EDI
    l10n_py_cdc = fields.Char(
        "CDC",
        readonly=True,
        copy=False,
        help="Código de Control del documento electrónico",
    )
    l10n_py_qr_code = fields.Binary("Código QR", readonly=True, copy=False)
    l10n_py_qr_string = fields.Char("String QR", readonly=True, copy=False)
    l10n_py_edi_xml = fields.Binary("XML Firmado", readonly=True, copy=False)
    l10n_py_edi_xml_filename = fields.Char("XML Filename", readonly=True)
    l10n_py_kude_pdf = fields.Binary("KUDE (PDF)", readonly=True, copy=False)
    l10n_py_kude_filename = fields.Char("KUDE Filename", readonly=True)

    l10n_py_edi_status = fields.Selection(
        [
            ("draft", "Borrador"),
            ("to_send", "Para Enviar"),
            ("sent", "Enviado"),
            ("processing", "Procesando"),
            ("accepted", "Aceptado"),
            ("rejected", "Rechazado"),
            ("cancelled", "Cancelado"),
            ("error", "Error"),
        ],
        string="Estado EDI",
        default="draft",
        readonly=True,
        copy=False,
    )

    l10n_py_edi_message = fields.Text("Mensaje EDI", readonly=True, copy=False)
    l10n_py_edi_batch_id = fields.Char("ID de Lote", readonly=True, copy=False)
    l10n_py_security_code = fields.Char(
        "Código de Seguridad", size=9, readonly=True, copy=False
    )
    l10n_py_receipt_id = fields.Char("Receipt ID", help="ID único del sistema cliente")

    # Campos para contingencia
    l10n_py_contingency_motive = fields.Char("Motivo de Contingencia")

    # Documentos asociados (Grupo H SIFEN)
    l10n_py_associated_document_ids = fields.One2many(
        "l10n_py.associated.document",
        "move_id",
        string="Documentos Asociados",
        help="Documentos asociados al DTE (Grupo H del SIFEN)",
    )

    # Operación comercial (Grupo D — gOpeCom)
    l10n_py_exchange_rate_condition = fields.Selection(
        [("1", "Global"), ("2", "Por Ítem")],
        string="Condición Tipo de Cambio",
        default="1",
        help="Condición del tipo de cambio (D015)",
    )

    # Tipo de pago (Grupo E — gPaConEIni)
    l10n_py_payment_type = fields.Selection(
        [
            ("1", "Efectivo"),
            ("2", "Cheque"),
            ("3", "Tarjeta de crédito"),
            ("4", "Tarjeta de débito"),
            ("5", "Transferencia"),
            ("6", "Giro"),
            ("7", "Billetera electrónica"),
            ("8", "Tarjeta empresarial"),
            ("9", "Vale"),
            ("10", "Retención"),
            ("11", "Anticipo"),
            ("12", "Valor fiscal"),
            ("13", "Valor comercial"),
            ("14", "Compensación"),
            ("15", "Permuta"),
            ("16", "Pago bancario"),
        ],
        string="Tipo de Pago",
        default="1",
        help="Tipo de pago para condición contado (E606)",
    )

    # Campos AFE — Autofactura Electrónica (Grupo E — gCamAE)
    l10n_py_afe_constancia_type = fields.Selection(
        [("1", "No contribuyente"), ("2", "Microproductor")],
        string="Tipo de Constancia (EA002)",
    )
    l10n_py_afe_constancia_number = fields.Char(
        string="Número de Constancia (EA004)",
        size=20,
    )
    l10n_py_afe_constancia_control = fields.Char(
        string="Número de Control (EA005)",
        size=20,
    )
    l10n_py_afe_vendor_doc_type = fields.Selection(
        [
            ("1", "Cédula paraguaya"),
            ("2", "Pasaporte"),
            ("3", "Cédula extranjera"),
            ("4", "Carnet de residencia"),
        ],
        string="Tipo Doc. Vendedor (EA006)",
    )
    l10n_py_afe_vendor_doc_number = fields.Char(
        string="Nro. Doc. Vendedor (EA008)",
        size=20,
    )
    l10n_py_afe_vendor_name = fields.Char(
        string="Nombre Vendedor (EA009)",
    )
    l10n_py_afe_vendor_address = fields.Char(
        string="Dirección Vendedor (EA010)",
    )
    l10n_py_afe_vendor_house = fields.Integer(
        string="Nro. Casa Vendedor (EA011)",
    )
    l10n_py_afe_vendor_department = fields.Integer(
        string="Departamento Vendedor (EA012)",
    )
    l10n_py_afe_vendor_district = fields.Integer(
        string="Distrito Vendedor (EA014)",
    )
    l10n_py_afe_vendor_city = fields.Integer(
        string="Ciudad Vendedor (EA016)",
    )
    l10n_py_afe_provision_address = fields.Char(
        string="Dirección Provisión (EA018)",
    )
    l10n_py_afe_provision_department = fields.Integer(
        string="Departamento Provisión (EA019)",
    )
    l10n_py_afe_provision_district = fields.Integer(
        string="Distrito Provisión (EA021)",
    )
    l10n_py_afe_provision_city = fields.Integer(
        string="Ciudad Provisión (EA023)",
    )

    # Campo auxiliar para visibilidad en la vista
    l10n_py_doc_type_code = fields.Char(
        compute="_compute_l10n_py_doc_type_code",
    )

    # Campo auxiliar para visibilidad en la vista (Factura de Exportación)
    l10n_py_is_export = fields.Boolean(
        compute="_compute_l10n_py_is_export",
    )

    # Campos NRE (Nota de Remisión Electrónica — tipo 7)
    l10n_py_nre_motive = fields.Selection(
        [
            ("1", "Traslado por venta"),
            ("2", "Traslado por consignación"),
            ("3", "Traslado por exportación"),
            ("4", "Traslado por importación"),
            ("5", "Traslado entre locales"),
            ("6", "Otros"),
        ],
        string="Motivo de Remisión (E501)",
    )

    l10n_py_nre_estimated_invoice_date = fields.Date(
        string="Fecha Estimada de Facturación (E506)",
        help="Fecha estimada de facturación para NRE sin factura asociada",
    )

    # Transporte (Grupo G SIFEN — NRE)
    l10n_py_transport_id = fields.Many2one(
        "l10n_py.transport",
        string="Datos de Transporte",
        help="Datos de transporte para Nota de Remisión (Grupo G SIFEN)",
    )

    # Campo prazo de transmissão
    l10n_py_transmission_deadline = fields.Datetime(
        string="Plazo de Transmisión",
        compute="_compute_transmission_deadline",
        store=True,
        help="Plazo máximo para transmitir el DTE (72 horas desde emisión)",
    )

    # ============== LIFECYCLE METHODS ==============

    def action_post(self):
        """Override para configurar estado EDI al confirmar factura."""
        res = super().action_post()
        for move in self:
            if move.move_type in ("out_invoice", "out_refund"):
                move.l10n_py_edi_status = "to_send"
        return res

    @api.depends("invoice_date")
    def _compute_transmission_deadline(self):
        """Calcular plazo máximo de transmisión (72h desde emisión)"""
        for move in self:
            if move.invoice_date:
                # 72 horas desde el inicio del día de emisión
                move.l10n_py_transmission_deadline = fields.Datetime.from_string(
                    str(move.invoice_date) + " 00:00:00"
                ) + relativedelta(hours=72)
            else:
                move.l10n_py_transmission_deadline = False

    @api.depends("l10n_latam_document_type_id")
    def _compute_l10n_py_doc_type_code(self):
        for move in self:
            move.l10n_py_doc_type_code = (
                move.l10n_latam_document_type_id.code
                if move.l10n_latam_document_type_id
                else ""
            )

    @api.depends("fiscal_position_id", "partner_id.country_id")
    def _compute_l10n_py_is_export(self):
        for move in self:
            move.l10n_py_is_export = move._l10n_py_is_export()

    def _l10n_py_is_export(self):
        """Factura de Exportación: fiscal position dedicada o parceiro do exterior."""
        self.ensure_one()
        if self.fiscal_position_id and self.fiscal_position_id.l10n_py_is_export:
            return True
        partner = self.partner_id
        return bool(partner.country_id) and partner.country_id.code != "PY"

    # ============== ONCHANGE METHODS ==============

    @api.onchange("invoice_line_ids")
    def _onchange_invoice_lines_transaction_type(self):
        """Auto-detectar tipo de transacción basado en los productos"""
        if self.invoice_line_ids:
            has_products = False
            has_services = False

            for line in self.invoice_line_ids.filtered(
                lambda line: line.display_type not in ("line_section", "line_note")
            ):
                if line.product_id:
                    if line.product_id.type in ["consu", "product"]:
                        has_products = True
                    elif line.product_id.type == "service":
                        has_services = True

            if has_products and has_services:
                self.l10n_py_transaction_type = "3"  # Mixto
            elif has_services:
                self.l10n_py_transaction_type = "2"  # Servicios
            else:
                self.l10n_py_transaction_type = "1"  # Mercadería

    # ============== CONSTRAINT METHODS ==============

    @api.constrains("l10n_py_security_code")
    def _check_security_code(self):
        for record in self:
            if record.l10n_py_security_code and len(record.l10n_py_security_code) != 9:
                raise ValidationError(
                    self.env._(
                        "El código de seguridad debe tener exactamente 9 caracteres"
                    )
                )

    # ============== PRIVATE METHODS ==============

    def _generate_security_code(self):
        """Generar código de seguridad aleatorio de 9 dígitos"""
        return "".join(secrets.choice(string.digits) for _ in range(9))

    # ISO 3166-1 alpha-2 -> alpha-3, tabela completa (todos os países/territórios
    # publicados pela ISO 3166-1). Usada por _get_country_alpha3 para o
    # cPaisRec/dDesPaisRe do SIFEN; qualquer country.code ISO válido resolve aqui.
    _ALPHA2_TO_3: ClassVar[dict[str, str]] = {
        "AD": "AND",
        "AE": "ARE",
        "AF": "AFG",
        "AG": "ATG",
        "AI": "AIA",
        "AL": "ALB",
        "AM": "ARM",
        "AO": "AGO",
        "AQ": "ATA",
        "AR": "ARG",
        "AS": "ASM",
        "AT": "AUT",
        "AU": "AUS",
        "AW": "ABW",
        "AX": "ALA",
        "AZ": "AZE",
        "BA": "BIH",
        "BB": "BRB",
        "BD": "BGD",
        "BE": "BEL",
        "BF": "BFA",
        "BG": "BGR",
        "BH": "BHR",
        "BI": "BDI",
        "BJ": "BEN",
        "BL": "BLM",
        "BM": "BMU",
        "BN": "BRN",
        "BO": "BOL",
        "BQ": "BES",
        "BR": "BRA",
        "BS": "BHS",
        "BT": "BTN",
        "BV": "BVT",
        "BW": "BWA",
        "BY": "BLR",
        "BZ": "BLZ",
        "CA": "CAN",
        "CC": "CCK",
        "CD": "COD",
        "CF": "CAF",
        "CG": "COG",
        "CH": "CHE",
        "CI": "CIV",
        "CK": "COK",
        "CL": "CHL",
        "CM": "CMR",
        "CN": "CHN",
        "CO": "COL",
        "CR": "CRI",
        "CU": "CUB",
        "CV": "CPV",
        "CW": "CUW",
        "CX": "CXR",
        "CY": "CYP",
        "CZ": "CZE",
        "DE": "DEU",
        "DJ": "DJI",
        "DK": "DNK",
        "DM": "DMA",
        "DO": "DOM",
        "DZ": "DZA",
        "EC": "ECU",
        "EE": "EST",
        "EG": "EGY",
        "EH": "ESH",
        "ER": "ERI",
        "ES": "ESP",
        "ET": "ETH",
        "FI": "FIN",
        "FJ": "FJI",
        "FK": "FLK",
        "FM": "FSM",
        "FO": "FRO",
        "FR": "FRA",
        "GA": "GAB",
        "GB": "GBR",
        "GD": "GRD",
        "GE": "GEO",
        "GF": "GUF",
        "GG": "GGY",
        "GH": "GHA",
        "GI": "GIB",
        "GL": "GRL",
        "GM": "GMB",
        "GN": "GIN",
        "GP": "GLP",
        "GQ": "GNQ",
        "GR": "GRC",
        "GS": "SGS",
        "GT": "GTM",
        "GU": "GUM",
        "GW": "GNB",
        "GY": "GUY",
        "HK": "HKG",
        "HM": "HMD",
        "HN": "HND",
        "HR": "HRV",
        "HT": "HTI",
        "HU": "HUN",
        "ID": "IDN",
        "IE": "IRL",
        "IL": "ISR",
        "IM": "IMN",
        "IN": "IND",
        "IO": "IOT",
        "IQ": "IRQ",
        "IR": "IRN",
        "IS": "ISL",
        "IT": "ITA",
        "JE": "JEY",
        "JM": "JAM",
        "JO": "JOR",
        "JP": "JPN",
        "KE": "KEN",
        "KG": "KGZ",
        "KH": "KHM",
        "KI": "KIR",
        "KM": "COM",
        "KN": "KNA",
        "KP": "PRK",
        "KR": "KOR",
        "KW": "KWT",
        "KY": "CYM",
        "KZ": "KAZ",
        "LA": "LAO",
        "LB": "LBN",
        "LC": "LCA",
        "LI": "LIE",
        "LK": "LKA",
        "LR": "LBR",
        "LS": "LSO",
        "LT": "LTU",
        "LU": "LUX",
        "LV": "LVA",
        "LY": "LBY",
        "MA": "MAR",
        "MC": "MCO",
        "MD": "MDA",
        "ME": "MNE",
        "MF": "MAF",
        "MG": "MDG",
        "MH": "MHL",
        "MK": "MKD",
        "ML": "MLI",
        "MM": "MMR",
        "MN": "MNG",
        "MO": "MAC",
        "MP": "MNP",
        "MQ": "MTQ",
        "MR": "MRT",
        "MS": "MSR",
        "MT": "MLT",
        "MU": "MUS",
        "MV": "MDV",
        "MW": "MWI",
        "MX": "MEX",
        "MY": "MYS",
        "MZ": "MOZ",
        "NA": "NAM",
        "NC": "NCL",
        "NE": "NER",
        "NF": "NFK",
        "NG": "NGA",
        "NI": "NIC",
        "NL": "NLD",
        "NO": "NOR",
        "NP": "NPL",
        "NR": "NRU",
        "NU": "NIU",
        "NZ": "NZL",
        "OM": "OMN",
        "PA": "PAN",
        "PE": "PER",
        "PF": "PYF",
        "PG": "PNG",
        "PH": "PHL",
        "PK": "PAK",
        "PL": "POL",
        "PM": "SPM",
        "PN": "PCN",
        "PR": "PRI",
        "PS": "PSE",
        "PT": "PRT",
        "PW": "PLW",
        "PY": "PRY",
        "QA": "QAT",
        "RE": "REU",
        "RO": "ROU",
        "RS": "SRB",
        "RU": "RUS",
        "RW": "RWA",
        "SA": "SAU",
        "SB": "SLB",
        "SC": "SYC",
        "SD": "SDN",
        "SE": "SWE",
        "SG": "SGP",
        "SH": "SHN",
        "SI": "SVN",
        "SJ": "SJM",
        "SK": "SVK",
        "SL": "SLE",
        "SM": "SMR",
        "SN": "SEN",
        "SO": "SOM",
        "SR": "SUR",
        "SS": "SSD",
        "ST": "STP",
        "SV": "SLV",
        "SX": "SXM",
        "SY": "SYR",
        "SZ": "SWZ",
        "TC": "TCA",
        "TD": "TCD",
        "TF": "ATF",
        "TG": "TGO",
        "TH": "THA",
        "TJ": "TJK",
        "TK": "TKL",
        "TL": "TLS",
        "TM": "TKM",
        "TN": "TUN",
        "TO": "TON",
        "TR": "TUR",
        "TT": "TTO",
        "TV": "TUV",
        "TW": "TWN",
        "TZ": "TZA",
        "UA": "UKR",
        "UG": "UGA",
        "UM": "UMI",
        "US": "USA",
        "UY": "URY",
        "UZ": "UZB",
        "VA": "VAT",
        "VC": "VCT",
        "VE": "VEN",
        "VG": "VGB",
        "VI": "VIR",
        "VN": "VNM",
        "VU": "VUT",
        "WF": "WLF",
        "WS": "WSM",
        "YE": "YEM",
        "YT": "MYT",
        "ZA": "ZAF",
        "ZM": "ZMB",
        "ZW": "ZWE",
    }

    @staticmethod
    def _get_country_alpha3(country):
        """Convert res.country (ISO alpha-2) to ISO alpha-3 for SIFEN PaisType.

        Fallback: sem país ou sem code -> "PRY" (comportamento original,
        preservado). Country com code ISO válido não mapeado (não deveria
        ocorrer, tabela é completa) -> devolve o próprio code alpha-2.
        """
        if not country or not country.code:
            return "PRY"
        return AccountMove._ALPHA2_TO_3.get(country.code, country.code)

    def _prepare_edi_document_data(self):
        """Preparar datos del documento electrónico en formato JSON"""
        self.ensure_one()

        if not self.l10n_py_security_code:
            self.l10n_py_security_code = self._generate_security_code()

        # Obtener código de tipo de documento desde l10n_latam
        doc_type_code = "1"
        if self.l10n_latam_document_type_id:
            doc_type_code = self.l10n_latam_document_type_id.code or "1"

        # Datos del timbrado (Grupo B)
        auth = self.journal_id.l10n_py_authorization_id
        timbrado_data = {}
        if auth:
            timbrado_data = {
                "timbrado": auth.name or "",
                "timbradoFechaInicio": (
                    auth.date_from.strftime("%Y-%m-%d") if auth.date_from else ""
                ),
                "timbradoFechaFin": (
                    auth.date_to.strftime("%Y-%m-%d") if auth.date_to else ""
                ),
            }

        # Construir estructura de datos según formato requerido
        document_data = {
            "tipoDocumento": int(doc_type_code),
            "establecimiento": (self.journal_id.l10n_py_establishment or "001"),
            "punto": self.journal_id.l10n_py_point or "001",
            "numero": self._get_edi_sequence_number(),
            **timbrado_data,
            "descripcion": self.name or "",
            "observacion": self.narration or "",
            "fecha": (
                self.invoice_date.strftime("%Y-%m-%dT%H:%M:%S")
                if self.invoice_date
                else fields.Datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            ),
            "tipoEmision": int(self.l10n_py_emission_type),
            "tipoTransaccion": int(self.l10n_py_transaction_type),
            "tipoImpuesto": 1,  # IVA
            "moneda": self.currency_id.name,
            "condicionTipoCambio": int(self.l10n_py_exchange_rate_condition or "1"),
            "tipoCambio": self.l10n_py_exchange_rate or 0,
            "receiptId": (self.l10n_py_receipt_id or f"{self.company_id.id}-{self.id}"),
            "codigoSeguridadAleatorio": self.l10n_py_security_code,
            "cliente": self._prepare_customer_data(),
            "factura": {"presencia": int(self.l10n_py_presence_type)},
            "condicion": self._prepare_payment_condition(),
            "items": self._prepare_invoice_lines(),
        }

        # Agregar datos de usuario emisor si existe
        if self.user_id:
            document_data["usuario"] = {
                "documentoTipo": 1,  # Cédula
                "documentoNumero": self.user_id.partner_id.vat or "",
                "nombre": self.user_id.name,
                "cargo": self.user_id.function or "Vendedor",
            }

        # Documentos asociados (Grupo H)
        if self.l10n_py_associated_document_ids:
            document_data["documentosAsociados"] = self._prepare_associated_documents()

        # Campos NRE (tipo=7)
        doc_type_code = "1"
        if self.l10n_latam_document_type_id:
            doc_type_code = self.l10n_latam_document_type_id.code or "1"
        if doc_type_code == "7":
            document_data["remision"] = {
                "motivo": int(self.l10n_py_nre_motive or "1"),
            }
            if self.l10n_py_nre_estimated_invoice_date:
                document_data["remision"]["fechaEstimada"] = (
                    self.l10n_py_nre_estimated_invoice_date.strftime("%Y-%m-%d")
                )

        # Campos AFE (tipo=4) — Autofactura Electrónica
        if doc_type_code == "4":
            document_data["autofactura"] = self._prepare_autofactura_data()

        # Transporte (tipo=7 — NRE; también Factura de Exportación, tipo=1)
        if (
            doc_type_code == "7" or self._l10n_py_is_export()
        ) and self.l10n_py_transport_id:
            document_data["transporte"] = self._prepare_transport_data()

        # Totales SIFEN
        document_data["totales"] = {
            "totalExento": self.l10n_py_amount_exempt,  # F003
            "totalExonerado": self.l10n_py_amount_exonerado,  # dSubExo
            "totalGravado5": self.l10n_py_amount_subtotal_5,  # F004
            "totalGravado10": self.l10n_py_amount_subtotal_10,  # F005
            "totalOperacion": self.l10n_py_total_operation,  # F008
            "totalIva": self.l10n_py_amount_iva_total,  # F014
            "liquidacionIva5": self.l10n_py_amount_iva_5,  # F015
            "liquidacionIva10": self.l10n_py_amount_iva_10,  # F016
            "baseGravada5": self.l10n_py_base_5,  # F018
            "baseGravada10": self.l10n_py_base_10,  # F019
            "totalBaseGravada": self.l10n_py_base_total,  # F020
        }
        if self.l10n_py_amount_total_pyg is not None:
            document_data["totales"]["totalPYG"] = self.l10n_py_amount_total_pyg  # F023
        else:
            # Fallback: use totalOperacion when currency is PYG
            document_data["totales"]["totalPYG"] = document_data["totales"][
                "totalOperacion"
            ]

        return document_data

    def _prepare_associated_documents(self):
        """Preparar datos de documentos asociados para JSON EDI."""
        docs = []
        for ad in self.l10n_py_associated_document_ids:
            doc_data = {
                "tipoAsociacion": int(ad.association_type),
            }
            if ad.association_type == "1":
                doc_data["cdc"] = ad.cdc
            elif ad.association_type == "2":
                doc_data.update(
                    {
                        "timbrado": ad.timbrado,
                        "establecimiento": ad.establishment,
                        "punto": ad.expedition_point,
                        "numero": ad.doc_number,
                        "tipoDocumentoImpreso": int(ad.doc_type_code),
                        "fecha": (
                            ad.doc_date.strftime("%Y-%m-%d") if ad.doc_date else ""
                        ),
                    }
                )
            elif ad.association_type == "3":
                doc_data.update(
                    {
                        "constanciaTipo": int(ad.constancia_type),
                        "constanciaNumero": ad.constancia_number,
                    }
                )
            docs.append(doc_data)
        return docs

    def _prepare_customer_data(self):
        """Preparar datos del cliente (Grupo D receptor)"""
        partner = self.partner_id

        # iNatRec: 1=Contribuyente, 2=No Contribuyente
        nat_rec = partner.l10n_py_taxpayer_type or "1"

        # iTiOpe: 1=B2B, 2=B2C, 3=B2G, 4=B2F (extranjero)
        if partner.country_id and partner.country_id.code != "PY":
            ti_ope = "4"  # Extranjero
        elif nat_rec == "2":
            ti_ope = "2"  # B2C
        else:
            ti_ope = "1"  # B2B

        customer_data = {
            "naturalezaReceptor": nat_rec,
            "tipoOperacion": ti_ope,
            "contribuyente": nat_rec == "1",
            "ruc": partner.l10n_py_ruc or "",
            "dvReceptor": partner.l10n_py_ruc_dv or "",
            "tipoContribuyente": "2" if partner.is_company else "1",
            "razonSocial": partner.name,
            "nombreFantasia": partner.l10n_py_fantasy_name or partner.name,
            "direccion": partner.street or "N/A",
            "numeroCasa": (
                partner.street_number if hasattr(partner, "street_number") else "0"
            )
            or "0",
            "pais": self._get_country_alpha3(partner.country_id) or "PRY",
            "paisDescripcion": partner.country_id.name or "Paraguay",
        }

        # Agregar datos de ubicación si están disponibles
        if partner.l10n_py_department_code:
            customer_data.update(
                {
                    "departamento": partner.l10n_py_department_code,
                    "departamentoDescripcion": (
                        partner.state_id.name if partner.state_id else ""
                    ),
                    "ciudad": partner.l10n_py_city_code or "",
                    "ciudadDescripcion": partner.city or "",
                }
            )

        # Agregar contacto
        # res.partner.mobile was merged into phone in 19.0
        if partner.phone:
            customer_data["telefono"] = partner.phone

        if partner.email:
            customer_data["email"] = partner.email

        # No-contribuyente: incluir documento de identidad (D024/D025)
        if nat_rec == "2":
            if partner.l10n_py_doc_type:
                customer_data["documentoTipo"] = int(partner.l10n_py_doc_type)
            if partner.l10n_py_doc_number:
                customer_data["documentoNumero"] = partner.l10n_py_doc_number

        return customer_data

    def _prepare_payment_condition(self):
        """Preparar condición de pago"""
        payment_condition = {
            "tipo": (
                2 if self.invoice_payment_term_id else 1
            ),  # 1: Contado, 2: Crédito
        }

        if self.invoice_payment_term_id:
            # Es crédito
            payment_condition["credito"] = {
                "tipo": 1,  # 1: Plazo, 2: Cuotas
                "plazo": (
                    f"{self.invoice_payment_term_id.line_ids[0].days} días"
                    if self.invoice_payment_term_id.line_ids
                    else "0 días"
                ),
                "cuotas": len(self.invoice_payment_term_id.line_ids),
            }

            # Preparar información de cuotas
            cuotas = []
            if self.invoice_date and self.invoice_payment_term_id.line_ids:
                for line in self.invoice_payment_term_id.line_ids:
                    due_date = self.invoice_date + relativedelta(days=line.days)
                    cuotas.append(
                        {
                            "moneda": self.currency_id.name,
                            "monto": (
                                self.amount_total
                                / len(self.invoice_payment_term_id.line_ids)
                            ),
                            "vencimiento": due_date.strftime("%Y-%m-%d"),
                        }
                    )

            payment_condition["credito"]["infoCuotas"] = cuotas
        else:
            # Es contado
            payment_condition["entregas"] = [
                {
                    "tipo": int(self.l10n_py_payment_type or "1"),
                    "monto": str(self.amount_total),
                    "moneda": self.currency_id.name,
                    "cambio": 0,
                }
            ]

        return payment_condition

    def _l10n_py_infer_affectation(self, tax):
        """Fallback p/ impostos sem l10n_py_iva_affectation (retrocompat)."""
        if tax.amount == 0:
            return "3"
        return "1"

    def _prepare_invoice_lines(self):
        """Preparar líneas de la factura"""
        items = []

        for line in self.invoice_line_ids.filtered(
            lambda line: line.display_type not in ("line_section", "line_note")
        ):
            # Determinar tasa de IVA e afetação (iAfecIVA)
            if not line.tax_ids:
                # Sin guard, la línea caería en el default (gravado 10%) y
                # declararía una base gravada inexistente ante el SIFEN.
                raise UserError(
                    self.env._(
                        "La línea '%s' no tiene ningún impuesto: cada ítem del "
                        "DE debe declarar su afectación de IVA (gravado, "
                        "exonerado, exento o gravado parcial)."
                    )
                    % (line.name or line.product_id.display_name)
                )
            iva_rate = 10  # Por defecto 10%
            iva_type = 1  # Gravado IVA

            for tax in line.tax_ids:
                affectation = (
                    tax.l10n_py_iva_affectation or self._l10n_py_infer_affectation(tax)
                )
                iva_type = int(affectation)
                if tax.amount in (0, 5, 10):
                    iva_rate = int(tax.amount)

            prop_iva = 0 if iva_type in (2, 3) else 100

            # Calcular base gravable e liquidação IVA por linha (SIFEN)
            base_gravada = 0.0
            liquidacion_iva = 0.0
            if iva_rate > 0 and line.price_total:
                base_gravada = line.price_total / (1 + iva_rate / 100)
                liquidacion_iva = line.price_total - base_gravada

            item = {
                "codigo": (
                    line.product_id.default_code or f"PROD-{line.product_id.id}"
                ),
                # Odoo antepone "[CÓDIGO] " al nombre de línea y permite saltos
                # de línea; el SET valida un patrón en dDesProSer, así que se
                # quita el prefijo y se colapsan los espacios/saltos.
                "descripcion": re.sub(
                    r"\s+",
                    " ",
                    re.sub(
                        r"^\[[^\]]*\]\s*",
                        "",
                        (line.name or line.product_id.name or ""),
                    ),
                ).strip(),
                "observacion": "",
                "ncm": (
                    line.product_id.l10n_py_ncm_code
                    if hasattr(line.product_id, "l10n_py_ncm_code")
                    else ""
                )
                or "",
                "unidadMedida": 77,  # UNI - Unidad
                "cantidad": line.quantity,
                "precioUnitario": line.price_unit,
                "cambio": 0,
                "ivaTipo": iva_type,
                "ivaBase": prop_iva,
                "iva": iva_rate,
                "baseGravada": round(base_gravada, 2),
                "liquidacionIva": round(liquidacion_iva, 2),
                "lote": "",
                "vencimiento": "",
            }

            items.append(item)

        return items

    def _prepare_transport_data(self):
        """Preparar datos de transporte (Grupo G SIFEN)."""
        t = self.l10n_py_transport_id
        data = {
            "modalidad": int(t.transport_mode),
        }
        if t.transport_type:
            data["tipo"] = int(t.transport_type)
        if t.freight_responsibility:
            data["responsableFlete"] = int(t.freight_responsibility)
        if t.incoterm:
            data["condicionNegociacion"] = t.incoterm
        if t.manifest_number:
            data["numeroManifiesto"] = t.manifest_number
        if t.transport_start_date:
            data["fechaInicio"] = t.transport_start_date.strftime("%Y-%m-%d")
        if t.transport_end_date:
            data["fechaFin"] = t.transport_end_date.strftime("%Y-%m-%d")

        # Departure point
        if t.departure_address:
            data["salida"] = {
                "direccion": t.departure_address,
                "numeroCasa": t.departure_house or 0,
                "departamento": t.departure_department or 0,
                "distrito": t.departure_district or 0,
                "ciudad": t.departure_city or 0,
            }

        # Transporter
        if t.transporter_name:
            data["transportista"] = {
                "naturaleza": t.transporter_nature or "1",
                "nombre": t.transporter_name,
                "ruc": t.transporter_ruc or "",
                "dv": t.transporter_dv or "",
                "choferDocumento": t.driver_doc_number or "",
                "choferNombre": t.driver_name or "",
            }

        # Vehicles
        if t.vehicle_ids:
            data["vehiculos"] = [
                {
                    "tipo": v.vehicle_type,
                    "marca": v.brand,
                    "numero": v.plate_number,
                }
                for v in t.vehicle_ids
            ]

        # Deliveries
        if t.delivery_ids:
            data["entregas"] = [
                {
                    "direccion": d.address,
                    "numeroCasa": d.house_number or 0,
                    "departamento": d.department,
                    "distrito": d.district or 0,
                    "ciudad": d.city,
                }
                for d in t.delivery_ids
            ]

        return data

    def _prepare_autofactura_data(self):
        """Preparar datos de Autofactura Electrónica (Grupo E — gCamAE)."""
        return {
            "tipoConstancia": int(self.l10n_py_afe_constancia_type or "1"),
            "numeroConstancia": self.l10n_py_afe_constancia_number or "",
            "numeroControl": self.l10n_py_afe_constancia_control or "",
            "tipoDocumentoVendedor": int(self.l10n_py_afe_vendor_doc_type or "1"),
            "numeroDocumentoVendedor": self.l10n_py_afe_vendor_doc_number or "",
            "nombreVendedor": self.l10n_py_afe_vendor_name or "",
            "direccionVendedor": self.l10n_py_afe_vendor_address or "",
            "numeroCasaVendedor": self.l10n_py_afe_vendor_house or 0,
            "departamentoVendedor": self.l10n_py_afe_vendor_department or 0,
            "distritoVendedor": self.l10n_py_afe_vendor_district or 0,
            "ciudadVendedor": self.l10n_py_afe_vendor_city or 0,
            "direccionProvision": self.l10n_py_afe_provision_address or "",
            "departamentoProvision": self.l10n_py_afe_provision_department or 0,
            "distritoProvision": self.l10n_py_afe_provision_district or 0,
            "ciudadProvision": self.l10n_py_afe_provision_city or 0,
        }

    def _get_edi_sequence_number(self):
        """Obtener número de secuencia para EDI"""
        if self.l10n_py_invoice_number:
            return str(self.l10n_py_invoice_number).zfill(7)
        if self.name:
            number = "".join(filter(str.isdigit, self.name.split("/")[-1]))
            return number.zfill(7)[-7:]
        return "0000001"

    def _validate_afe_data(self, docs):
        """Validar datos específicos de Autofactura Electrónica (código 4)."""
        errors = []
        if len(docs) != 1:
            errors.append(
                self.env._("Autofactura: debe tener exactamente 1 documento asociado.")
            )
        elif docs[0].association_type != "3":
            errors.append(
                self.env._(
                    "Autofactura: el documento asociado debe "
                    "ser una constancia electrónica."
                )
            )
        required_fields = [
            ("l10n_py_afe_constancia_type", "el tipo de constancia"),
            ("l10n_py_afe_constancia_number", "el número de constancia"),
            ("l10n_py_afe_constancia_control", "el número de control"),
            ("l10n_py_afe_vendor_doc_number", "el número de documento del vendedor"),
            ("l10n_py_afe_vendor_name", "el nombre del vendedor"),
            ("l10n_py_afe_vendor_address", "la dirección del vendedor"),
        ]
        for field_name, desc in required_fields:
            if not getattr(self, field_name):
                errors.append(self.env._("Autofactura: %s es obligatorio.", desc))
        return errors

    def _validate_nre_data(self, docs):
        """Validar datos específicos de Nota de Remisión Electrónica
        (código 7). Extraído de ``_validate_edi_document_type`` para
        mantener la complejidad ciclomática de ese método bajo control."""
        errors = []
        if not self.l10n_py_nre_motive:
            errors.append(self.env._("Nota de Remisión: el motivo es obligatorio."))
        # Motivo "1" (traslado por venta) sin doc asociado → requer data estimada
        if (
            self.l10n_py_nre_motive == "1"
            and not docs
            and not self.l10n_py_nre_estimated_invoice_date
        ):
            errors.append(
                self.env._(
                    "NRE traslado por venta sin documento "
                    "asociado: debe indicar fecha estimada "
                    "de facturación."
                )
            )
        # Data estimada no puede exceder el mes de emisión
        if self.l10n_py_nre_estimated_invoice_date and self.invoice_date:
            est_date = self.l10n_py_nre_estimated_invoice_date
            inv_date = self.invoice_date
            # La fecha estimada no debe superar el mes siguiente
            if est_date.month > inv_date.month + 1 or (
                est_date.year > inv_date.year
                and not (inv_date.month == 12 and est_date.month == 1)
            ):
                errors.append(
                    self.env._(
                        "La fecha estimada de facturación no puede "
                        "exceder el mes siguiente al de emisión."
                    )
                )
        # Motivo "5" (entre locales) → RUC receptor = RUC emissor
        if self.l10n_py_nre_motive == "5":
            partner_ruc = self.partner_id.l10n_py_ruc or ""
            company_ruc = self.company_id.l10n_py_ruc or ""
            if partner_ruc != company_ruc:
                errors.append(
                    self.env._(
                        "Traslado entre locales: el RUC del "
                        "receptor debe coincidir con el del emisor."
                    )
                )
        return errors

    def _validate_edi_document_type(self):
        """Validar requisitos específicos por tipo de DTE.

        Llamado antes del envío EDI. Retorna lista de errores.
        """
        errors = []
        code = (
            self.l10n_latam_document_type_id.code
            if self.l10n_latam_document_type_id
            else ""
        )
        docs = self.l10n_py_associated_document_ids

        # AFE (code=4): exatamente 1 constância + datos vendedor
        if code == "4":
            errors.extend(self._validate_afe_data(docs))

        # NCE (code=5): exatamente 1 doc associado
        elif code == "5":
            if len(docs) != 1:
                errors.append(
                    self.env._(
                        "Nota de Crédito Electrónica: debe tener "
                        "exactamente 1 documento asociado."
                    )
                )

        # NDE (code=6): exatamente 1 doc associado
        elif code == "6":
            if len(docs) != 1:
                errors.append(
                    self.env._(
                        "Nota de Débito Electrónica: debe tener "
                        "exactamente 1 documento asociado."
                    )
                )

        # NRE (code=7): validações NRE
        elif code == "7":
            errors.extend(self._validate_nre_data(docs))

        # Exportación (Factura de Exportación): validaciones adicionales
        # exigidas en la práctica por la SET aunque el XSD los marque
        # como opcionales.
        if self._l10n_py_is_export():
            errors.extend(self._validate_export_data())

        return errors

    def _validate_nre_data(self, docs):
        """Validaciones específicas de la Nota de Remisión (code=7)."""
        errors = []
        if not self.l10n_py_nre_motive:
            errors.append(self.env._("Nota de Remisión: el motivo es obligatorio."))
        # Motivo "1" (traslado por venta) sin doc asociado → requer data estimada
        if (
            self.l10n_py_nre_motive == "1"
            and not docs
            and not self.l10n_py_nre_estimated_invoice_date
        ):
            errors.append(
                self.env._(
                    "NRE traslado por venta sin documento "
                    "asociado: debe indicar fecha estimada "
                    "de facturación."
                )
            )
        # Data estimada no puede exceder el mes de emisión
        if self.l10n_py_nre_estimated_invoice_date and self.invoice_date:
            est_date = self.l10n_py_nre_estimated_invoice_date
            inv_date = self.invoice_date
            # La fecha estimada no debe superar el mes siguiente
            if est_date.month > inv_date.month + 1 or (
                est_date.year > inv_date.year
                and not (inv_date.month == 12 and est_date.month == 1)
            ):
                errors.append(
                    self.env._(
                        "La fecha estimada de facturación no puede "
                        "exceder el mes siguiente al de emisión."
                    )
                )
        # Motivo "5" (entre locales) → RUC receptor = RUC emissor
        if self.l10n_py_nre_motive == "5":
            partner_ruc = self.partner_id.l10n_py_ruc or ""
            company_ruc = self.company_id.l10n_py_ruc or ""
            if partner_ruc != company_ruc:
                errors.append(
                    self.env._(
                        "Traslado entre locales: el RUC del "
                        "receptor debe coincidir con el del emisor."
                    )
                )

        return errors

    def _validate_export_data(self):
        """Validaciones de exportación exigidas en la práctica por la SET."""
        errors = []
        if (
            self.currency_id
            and self.currency_id.name != "PYG"
            and (self.l10n_py_exchange_rate or 0) <= 0
        ):
            errors.append(
                self.env._(
                    "Exportación en moneda extranjera requiere tipo de "
                    "cambio (l10n_py_exchange_rate) mayor a cero."
                )
            )
        if not self.partner_id.street:
            errors.append(
                self.env._(
                    "Exportación: la dirección del receptor del "
                    "exterior (dDirRec) es obligatoria."
                )
            )
        return errors

    def _validate_edi_data(self):
        """Validar datos antes de enviar a EDI"""
        errors = []

        # Validar datos de la empresa
        company = self.company_id
        if not company.l10n_py_ruc:
            errors.append(self.env._("Configure el RUC de la empresa"))

        # Validar datos del cliente (F15)
        partner = self.partner_id
        if partner.l10n_py_taxpayer_type == "1" and not partner.l10n_py_ruc:
            errors.append(self.env._("El cliente contribuyente debe tener RUC"))
        if partner.l10n_py_taxpayer_type == "2" and not partner.l10n_py_doc_number:
            errors.append(
                self.env._(
                    "El cliente no contribuyente debe tener número "
                    "de documento de identidad"
                )
            )

        if not partner.street:
            errors.append(self.env._("La dirección del cliente es obligatoria"))

        # Validar datos del diario
        journal = self.journal_id
        if not journal.l10n_py_authorization_id:
            errors.append(self.env._("Configure el timbrado en el diario"))

        if (
            journal.l10n_py_authorization_validity
            and journal.l10n_py_authorization_validity < fields.Date.today()
        ):
            errors.append(self.env._("El timbrado está vencido"))

        # Validar productos
        for line in self.invoice_line_ids.filtered(
            lambda line: line.display_type not in ("line_section", "line_note")
        ):
            if hasattr(line.product_id, "l10n_py_ncm_code") and (
                not line.product_id.l10n_py_ncm_code
            ):
                errors.append(
                    self.env._(
                        "El producto %s no tiene código NCM", line.product_id.name
                    )
                )
            # "Gravado parcial" (iAfecIVA=4) no tiene, hoy, ningún cálculo
            # real de la proporción gravada/exenta (dPropIVA) -- generar
            # el DE con este tipo emitiría un dPropIVA incorrecto de forma
            # silenciosa. Falla alto en vez de emitir un dato fiscal
            # incorrecto: ver _prepare_invoice_lines/dPropIVA.
            for tax in line.tax_ids:
                if tax.l10n_py_iva_affectation == "4":
                    errors.append(
                        self.env._(
                            "El producto %(product)s usa el impuesto "
                            "'%(tax)s' con afectación IVA 'Gravado "
                            "parcial', que este módulo todavía no sabe "
                            "calcular (no existe cálculo real de la "
                            "proporción gravada/exenta). Use otro tipo de "
                            "afectación o configure el cálculo antes de "
                            "generar el documento electrónico.",
                            product=line.product_id.name,
                            tax=tax.name,
                        )
                    )

        # Validar requisitos por tipo de documento (F03-F07)
        errors.extend(self._validate_edi_document_type())

        # Validar nominación obligatoria (> Gs. 7.000.000)
        _NOMINACION_THRESHOLD = 7000000
        if (
            self.currency_id.name == "PYG"
            and self.amount_total > _NOMINACION_THRESHOLD
            and partner.l10n_py_taxpayer_type == "2"
            and not partner.l10n_py_doc_number
        ):
            errors.append(
                self.env._(
                    "Facturas superiores a Gs. 7.000.000 no pueden "
                    "ser innominadas. Debe identificar al receptor."
                )
            )

        if errors:
            raise UserError("\n".join(errors))

        return True

    # ============== PUBLIC METHODS ==============

    def _get_edi_connector(self):
        """Buscar conector EDI de la empresa."""
        connector = (
            self.env["l10n_py.edi.connector"]
            .sudo()
            .search([("company_id", "=", self.company_id.id)], limit=1)
        )
        if not connector:
            raise UserError(
                self.env._("No hay un conector EDI configurado para esta empresa")
            )
        return connector

    def _target_new_tab(self, attachment_id):
        """Open an ir.attachment inline in a new browser tab."""
        if attachment_id:
            return {
                "type": "ir.actions.act_url",
                "url": f"/web/content/{attachment_id.id}/{attachment_id.name}",
                "target": "new",
            }

    def action_preview_xml(self):
        """Generar y mostrar XML sin firmar ni enviar (preview)."""
        self.ensure_one()
        self._validate_edi_data()
        document_data = self._prepare_edi_document_data()
        connector = self._get_edi_connector()
        xml_string = connector.preview_document(document_data)

        xml_bytes = xml_string.encode("utf-8")
        self.l10n_py_edi_xml = BinaryBytes(xml_bytes)
        self.l10n_py_edi_xml_filename = "preview.xml"

        attachment = self.env["ir.attachment"].create(
            {
                "name": f"preview_{self.name or self.id}.xml",
                "raw": xml_bytes,
                "mimetype": "text/xml",
                "res_model": self._name,
                "res_id": self.id,
            }
        )
        return self._target_new_tab(attachment)

    def action_preview_kude(self):
        """Generar KuDE (PDF) a partir del XML preview via pykude."""
        self.ensure_one()
        if not self.l10n_py_edi_xml:
            # Generate XML first
            self.action_preview_xml()
        if not self.l10n_py_edi_xml:
            raise UserError(self.env._("No hay XML disponible para generar el KuDE"))

        from pykude import auto_kude
        from pykude.kude_fe.config import KudeFeConfig

        xml_content = self.l10n_py_edi_xml.decode("utf-8")

        config = KudeFeConfig()
        if self.company_id.logo:
            config.logo = self.company_id.logo.content

        kude = auto_kude(xml=xml_content, config=config)
        pdf_bytes = kude.output()

        attachment = self.env["ir.attachment"].create(
            {
                "name": f"KUDE_preview_{self.name or self.id}.pdf",
                "raw": pdf_bytes,
                "mimetype": "application/pdf",
                "res_model": self._name,
                "res_id": self.id,
            }
        )
        return self._target_new_tab(attachment)

    def action_send_edi(self):
        """Enviar documento a sistema EDI"""
        self.ensure_one()

        # Validar datos
        self._validate_edi_data()

        # Preparar datos
        document_data = self._prepare_edi_document_data()

        # Obtener conector configurado
        connector = self._get_edi_connector()

        try:
            # Enviar documento
            self.l10n_py_edi_status = "sent"
            response = connector.send_document(document_data)

            # Procesar respuesta
            if response.get("success"):
                self._process_edi_response(response)
            else:
                self.l10n_py_edi_status = "rejected"
                self.l10n_py_edi_message = response.get("error", "Error desconocido")

        except Exception as e:
            _logger.error("Error enviando EDI: %s", str(e))
            self.l10n_py_edi_status = "error"
            self.l10n_py_edi_message = str(e)
            raise UserError(self.env._("Error enviando documento: %s", str(e))) from e

    def _process_edi_response(self, response):
        """Procesar respuesta exitosa del EDI"""
        self.ensure_one()

        result = response.get("result", {})

        # Guardar CDC y otros datos
        if result.get("deList"):
            de_data = result["deList"][0]
            self.write(
                {
                    "l10n_py_cdc": de_data.get("cdc"),
                    "l10n_py_qr_string": de_data.get("qr"),
                    "l10n_py_edi_status": "accepted",
                    "l10n_py_edi_batch_id": result.get("loteId"),
                    "l10n_py_edi_message": ("Documento aceptado exitosamente"),
                }
            )

            # Generar la imagen del QR a partir del enlace dCarQR
            self._l10n_py_generate_qr_image()

            # Guardar XML si viene
            if de_data.get("xml"):
                self.l10n_py_edi_xml = BinaryBytes(de_data["xml"].encode("utf-8"))
                self.l10n_py_edi_xml_filename = f"{self.l10n_py_cdc}.xml"

            # Auto-generar KuDE al aceptar
            try:
                self._generate_kude()
            except Exception as e:  # noqa: BLE001
                _logger.warning("Error generando KuDE: %s", str(e))

    def _l10n_py_generate_qr_image(self):
        """Genera la imagen PNG del QR (l10n_py_qr_code) desde el enlace."""
        from ..services.qr_generator import QRGenerator

        for move in self:
            if move.l10n_py_qr_string:
                image = QRGenerator.generate_image(move.l10n_py_qr_string)
                move.l10n_py_qr_code = BinaryBytes(image) if image else False

    def action_l10n_py_preview_qr(self):
        """Genera CDC + QR (firma local) SIN transmitir, para previsualizar.

        Útil para verificar el QR/KuDE en pruebas. El CDC generado es de
        previsualización; la emisión real lo regenera al transmitir.
        """
        self.ensure_one()
        self._validate_edi_data()
        document_data = self._prepare_edi_document_data()
        connector = self._get_edi_connector()
        result = connector.preview_qr(document_data)
        if not result or not result.get("qr"):
            raise UserError(
                self.env._(
                    "No se pudo generar el QR. Verifique el certificado y el "
                    "CSC/IdCSC configurados en el conector EDI."
                )
            )
        self.write(
            {
                "l10n_py_cdc": result.get("cdc"),
                "l10n_py_qr_string": result["qr"],
            }
        )
        self._l10n_py_generate_qr_image()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "type": "success",
                "title": self.env._("QR generado"),
                "message": self.env._("CDC y código QR de previsualización generados."),
                "sticky": False,
            },
        }

    def _validate_cancel_deadline(self):
        """Validar plazo de cancelación según tipo de documento SIFEN.

        FE/AFE: 48 horas, NCE/NDE/NRE: 168 horas (7 días).
        """
        if not self.invoice_date:
            return
        code = (
            self.l10n_latam_document_type_id.code
            if self.l10n_latam_document_type_id
            else ""
        )
        # FE(1) y AFE(4): 48h, NCE(5)/NDE(6)/NRE(7): 168h
        if code in ("1", "4"):
            max_hours = 48
        else:
            max_hours = 168

        emission_dt = fields.Datetime.from_string(str(self.invoice_date) + " 00:00:00")
        deadline = emission_dt + relativedelta(hours=max_hours)
        now = fields.Datetime.now()
        if now > deadline:
            raise UserError(
                self.env._(
                    "El plazo de cancelación ha expirado. "
                    "Límite: %(deadline)s (%(hours)s horas desde emisión).",
                    deadline=deadline,
                    hours=max_hours,
                )
            )

    def action_cancel_edi(self):
        """Cancelar documento electrónico"""
        self.ensure_one()

        if not self.l10n_py_cdc:
            raise UserError(self.env._("No se puede cancelar un documento sin CDC"))

        self._validate_cancel_deadline()

        connector = self._get_edi_connector()
        response = connector.cancel_document(self.l10n_py_cdc)
        if response.get("success"):
            self.l10n_py_edi_status = "cancelled"
            self.l10n_py_edi_message = f"Cancelado el {fields.Datetime.now()}"
        else:
            raise UserError(
                self.env._("Error cancelando documento: %s", response.get("error"))
            )

    def action_retry_edi(self):
        """Reintentar envío de documento"""
        self.ensure_one()

        if self.l10n_py_edi_status not in ["error", "rejected"]:
            raise UserError(
                self.env._(
                    "Solo se pueden reintentar documentos con error o rechazados"
                )
            )

        return self.action_send_edi()

    def action_download_xml(self):
        """Descargar XML del documento"""
        self.ensure_one()

        if not self.l10n_py_edi_xml:
            raise UserError(self.env._("No hay XML disponible para este documento"))

        return {
            "type": "ir.actions.act_url",
            "url": (
                f"/web/content/{self._name}/{self.id}/l10n_py_edi_xml/"
                f"{self.l10n_py_edi_xml_filename}?download=true"
            ),
            "target": "self",
        }

    def action_download_kude(self):
        """Descargar KUDE (PDF)"""
        self.ensure_one()

        if not self.l10n_py_kude_pdf:
            # Intentar generar KUDE
            self._generate_kude()

        if not self.l10n_py_kude_pdf:
            raise UserError(self.env._("No hay KUDE disponible para este documento"))

        return {
            "type": "ir.actions.act_url",
            "url": (
                f"/web/content/{self._name}/{self.id}/l10n_py_kude_pdf/"
                f"{self.l10n_py_kude_filename}?download=true"
            ),
            "target": "self",
        }

    def _generate_kude(self):
        """Generar KUDE (representación gráfica del DE) vía pykude."""
        self.ensure_one()
        if not self.l10n_py_edi_xml:
            return
        from pykude import auto_kude
        from pykude.kude_fe.config import KudeFeConfig

        xml_content = self.l10n_py_edi_xml.decode("utf-8")

        config = KudeFeConfig()
        if self.company_id.logo:
            config.logo = self.company_id.logo.content

        kude = auto_kude(xml=xml_content, config=config)
        pdf_bytes = kude.output()
        self.l10n_py_kude_pdf = BinaryBytes(pdf_bytes)
        self.l10n_py_kude_filename = f"KUDE_{self.l10n_py_cdc}.pdf"

    # ============== CRON METHODS ==============

    @api.model
    def _cron_check_edi_status(self):
        """Verificar estado de documentos enviados y procesar cola de contingencia.

        Prioriza documentos cercanos al plazo de 72h.
        """
        # 1. Procesar cola de contingencia (to_send pendientes)
        contingency_docs = self.search(
            [
                ("l10n_py_edi_status", "=", "to_send"),
                ("l10n_py_emission_type", "=", "2"),
            ],
            order="l10n_py_transmission_deadline asc",
        )
        for doc in contingency_docs:
            try:
                doc.action_send_edi()
            except Exception:  # noqa: BLE001
                _logger.warning("Error reenviando doc contingencia %s", doc.name)

        # 2. Verificar estado de documentos ya enviados
        pending_docs = self.search(
            [
                ("l10n_py_edi_status", "in", ["sent", "processing"]),
                ("l10n_py_edi_batch_id", "!=", False),
            ]
        )

        for doc in pending_docs:
            try:
                connector = (
                    self.env["l10n_py.edi.connector"]
                    .sudo()
                    .search([("company_id", "=", doc.company_id.id)], limit=1)
                )
                if not connector:
                    continue
                response = connector.check_status(doc.l10n_py_edi_batch_id)
                if response.get("success"):
                    # Actualizar estado según respuesta
                    pass
            except Exception as e:  # noqa: BLE001
                _logger.error(
                    "Error verificando estado EDI para %s: %s",
                    doc.name,
                    str(e),
                )
