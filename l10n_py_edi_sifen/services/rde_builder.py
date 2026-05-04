# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

"""
RDeBuilder: Converts invoice_data dict → pysifen RDe binding object.

Mapping follows SIFEN v150 Manual Técnico.
"""

import logging
from datetime import datetime
from decimal import Decimal

from pysifen.de.bindings.v150.fe_types_v141 import (
    TcCondNeg,
    TdCondTiCam,
    TdDcondCred,
    TdDesModTrans,
    TdDesTimp,
    TdDesTiPag,
    TdDesTtrans,
    TiModTrans,
    TiRespFlete,
    TiTimp,
    TiTiPago,
    TiTtrans,
)
from pysifen.de.bindings.v150.fe_v141 import (
    RDe,
    TdDcondOpe,
    TdDesAfecIva,
    TdDesIndPresValue,
    TdDesMotEmi,
    TdDesTiDe,
    TdDesTipDocAso,
    TdDesTipEmi,
    TDe,
    TgActEco,
    TgCamAe,
    TgCamCond,
    TgCamDeasoc,
    TgCamEnt,
    TgCamFe,
    TgCamFuFd,
    TgCamItem,
    TgCamIva,
    TgCamNcde,
    TgCamNre,
    TgCamSal,
    TgCamTrans,
    TgCopeDe,
    TgCuotas,
    TgDaGoc,
    TgDatRec,
    TgDtim,
    TgDtipDe,
    TgEmis,
    TgOpeCom,
    TgPagCont,
    TgPagCred,
    TgPagCredICondCred,
    TgTotSub,
    TgTransp,
    TgValorItem,
    TgVehTras,
    TiRespEmiNr,
)
from pysifen.de.bindings.v150.monedas_v100 import CMondT
from pysifen.de.bindings.v150.xmldsig_core_schema import (
    CanonicalizationMethod,
    Signature,
    SignatureMethod,
    SignatureValue,
    SignedInfo,
)

_logger = logging.getLogger(__name__)

# === Lookup tables for SIFEN description enums ===

_TIP_EMI_DESC = {1: TdDesTipEmi.NORMAL, 2: TdDesTipEmi.CONTINGENCIA}

# Types 4 (AFE) and 7 (NRE) don't have entries in TdDesTiDe —
# pysifen only defines FE, NCE, NDE descriptions.
_TI_DE_DESC = {
    1: TdDesTiDe.FACTURA_ELECTR_NICA,
    4: TdDesTiDe.FACTURA_ELECTR_NICA,  # AFE uses FE description
    5: TdDesTiDe.NOTA_DE_CR_DITO_ELECTR_NICA,
    6: TdDesTiDe.NOTA_DE_D_BITO_ELECTR_NICA,
    7: TdDesTiDe.FACTURA_ELECTR_NICA,  # NRE — no specific desc in enum
}

_IND_PRES_DESC = {
    1: TdDesIndPresValue.OPERACI_N_PRESENCIAL,
    2: TdDesIndPresValue.OPERACI_N_ELECTR_NICA,
    3: TdDesIndPresValue.OPERACI_N_TELEMARKETING,
    4: TdDesIndPresValue.VENTA_A_DOMICILIO,
    5: TdDesIndPresValue.OPERACI_N_BANCARIA,
}

_COND_OPE_DESC = {1: TdDcondOpe.CONTADO, 2: TdDcondOpe.CR_DITO}

_MOT_EMI_DESC = {
    1: TdDesMotEmi.ANULACI_N,
    2: TdDesMotEmi.DEVOLUCI_N,
    3: TdDesMotEmi.DESCUENTO,
    4: TdDesMotEmi.BONIFICACI_N,
    5: TdDesMotEmi.CR_DITO_INCOBRABLE,
    6: TdDesMotEmi.RECUPERO_DE_COSTO,
    7: TdDesMotEmi.RECUPERO_DE_GASTO,
    8: TdDesMotEmi.AJUSTE_DE_PRECIO,
}

_AFEC_IVA_DESC = {
    1: TdDesAfecIva.GRAVADO_IVA,
    2: TdDesAfecIva.EXONERADO_ART_83_LEY_125_91,
    3: TdDesAfecIva.EXENTO,
    4: TdDesAfecIva.GRAVADO_PARCIAL_GRAV_EXENTO,
}

_TIP_DOC_ASO_DESC = {
    1: TdDesTipDocAso.ELECTR_NICO,
    2: TdDesTipDocAso.IMPRESO,
}

# Map ISO 4217 currency name → pysifen CMondT enum
_CURRENCY_MAP = {m.value: m for m in CMondT}

# Payment type code → description enum
_TIP_PAGO_DESC = {
    1: TdDesTiPag.EFECTIVO,
    2: TdDesTiPag.CHEQUE,
    3: TdDesTiPag.TARJETA_DE_CR_DITO,
    4: TdDesTiPag.TARJETA_DE_D_BITO,
    5: TdDesTiPag.TRANSFERENCIA,
    6: TdDesTiPag.GIRO,
    7: TdDesTiPag.BILLETERA_ELECTR_NICA,
    8: TdDesTiPag.TARJETA_EMPRESARIAL,
    9: TdDesTiPag.VALE,
    10: TdDesTiPag.RETENCI_N,
    11: TdDesTiPag.ANTICIPO,
    12: TdDesTiPag.VALOR_FISCAL,
    13: TdDesTiPag.VALOR_COMERCIAL,
    14: TdDesTiPag.COMPENSACI_N,
    15: TdDesTiPag.PERMUTA,
    16: TdDesTiPag.PAGO_BANCARIO,
}

# Payment type code → TiTiPago enum
_TIP_PAGO_CODE = {i: TiTiPago(i) for i in range(1, 17)}

# Transport mode → description
_MOD_TRANS_DESC = {
    1: TdDesModTrans.TERRESTRE,
    2: TdDesModTrans.FLUVIAL,
    3: TdDesModTrans.A_REO,
    4: TdDesModTrans.MULTIMODAL,
}

# Transport type → description
_TIP_TRANS_DESC = {
    1: TdDesTtrans.PROPIO,
    2: TdDesTtrans.TERCERO,
}


def _get_currency_enum(currency_name: str) -> CMondT:
    """Map ISO currency name to CMondT enum, default PYG."""
    return _CURRENCY_MAP.get(currency_name, CMondT.PYG)


def _get_currency_desc(currency_name: str) -> str:
    """Get human description for currency."""
    _CURRENCY_DESC = {
        "PYG": "Guarani",
        "USD": "Dólar americano",
        "BRL": "Real",
        "EUR": "Euro",
        "ARS": "Peso argentino",
        "UYU": "Peso uruguayo",
    }
    return _CURRENCY_DESC.get(currency_name, currency_name)


class RDeBuilder:
    """Build pysifen RDe object from invoice_data dict."""

    def __init__(self, invoice_data: dict, company_data: dict, cdc: str):
        self.data = invoice_data
        self.company = company_data
        self.cdc = cdc

    def build(self) -> RDe:
        """Build complete RDe."""
        tde = TDe(
            Id=self.cdc,
            dDVId=self.cdc[-1] if len(self.cdc) == 43 else "",
            dFecFirma="",
            gOpeDE=self._build_gOpeDE(),
            gTimb=self._build_gTimb(),
            gDatGralOpe=self._build_gDatGralOpe(),
            gDtipDE=self._build_gDtipDE(),
            gTotSub=self._build_gTotSub(),
        )

        # Optional: transport data (Grupo G — NRE)
        transp_data = self.data.get("transporte")
        if transp_data:
            tde.gDtipDE.gTransp = self._build_gTransp(transp_data)

        # Optional: associated documents (Grupo H)
        assoc_docs = self.data.get("documentosAsociados", [])
        if assoc_docs:
            tde.gCamDEAsoc = self._build_gCamDEAsoc(assoc_docs)

        # Signature and gCamFuFD are required by the binding but filled
        # by pysifen at signing time.  For preview we use empty placeholders.
        empty_signature = Signature(
            SignedInfo=SignedInfo(
                CanonicalizationMethod=CanonicalizationMethod(Algorithm=""),
                SignatureMethod=SignatureMethod(Algorithm=""),
            ),
            SignatureValue=SignatureValue(),
        )
        return RDe(
            dVerFor="150",
            DE=tde,
            Signature=empty_signature,
            gCamFuFD=TgCamFuFd(dCarQR=""),
        )

    def _build_gOpeDE(self) -> TgCopeDe:
        """Grupo A: Operational data."""
        tip_emi = self.data.get("tipoEmision", 1)
        return TgCopeDe(
            iTipEmi=tip_emi,
            dDesTipEmi=_TIP_EMI_DESC.get(tip_emi, TdDesTipEmi.NORMAL),
            dCodSeg=self.data.get("codigoSeguridadAleatorio", "000000000"),
        )

    def _build_gTimb(self) -> TgDtim:
        """Grupo B: Timbrado / document identification."""
        ti_de = self.data.get("tipoDocumento", 1)
        return TgDtim(
            iTiDE=ti_de,
            dDesTiDE=_TI_DE_DESC.get(ti_de, TdDesTiDe.FACTURA_ELECTR_NICA),
            dNumTim=self.data.get("timbrado", ""),
            dEst=self.data.get("establecimiento", "001"),
            dPunExp=self.data.get("punto", "001"),
            dNumDoc=self.data.get("numero", "0000001"),
            dFeIniT=self.data.get("timbradoFechaInicio", ""),
            dFeFinT=self.data.get("timbradoFechaFin", ""),
        )

    def _build_gDatGralOpe(self) -> TgDaGoc:
        """Grupo C: General operation data (includes gOpeCom)."""
        fecha_str = self.data.get("fecha", datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        return TgDaGoc(
            dFeEmiDE=fecha_str,
            gOpeCom=self._build_gOpeCom(),
            gEmis=self._build_gEmis(),
            gDatRec=self._build_gDatRec(),
        )

    def _build_gOpeCom(self) -> TgOpeCom:
        """Grupo D: Commercial operation data (gOpeCom)."""
        currency_name = self.data.get("moneda", "PYG")
        cond_ti_cam = self.data.get("condicionTipoCambio", 1)
        tipo_cambio = self.data.get("tipoCambio", 0)

        ope_com = TgOpeCom(
            iTImp=TiTimp.VALUE_1,  # IVA
            dDesTImp=TdDesTimp.IVA,
            cMoneOpe=_get_currency_enum(currency_name),
            dDesMoneOpe=_get_currency_desc(currency_name),
        )

        # Transaction type (optional in gOpeCom)
        tip_tra = self.data.get("tipoTransaccion")
        if tip_tra:
            ope_com.iTipTra = tip_tra

        # Exchange rate condition — only when currency != PYG
        if currency_name != "PYG":
            ope_com.dCondTiCam = TdCondTiCam(cond_ti_cam)
            if tipo_cambio:
                ope_com.dTiCam = Decimal(str(tipo_cambio))

        return ope_com

    def _build_gEmis(self) -> TgEmis:
        """Grupo D: Emitter (company) data."""
        return TgEmis(
            dRucEm=self.company.get("ruc", ""),
            dDVEmi=self.company.get("dv", ""),
            iTipCont=self.company.get("tipoContribuyente", "2"),
            dNomEmi=self.company.get("razonSocial", ""),
            dNomFanEmi=self.company.get("nombreFantasia", ""),
            dDirEmi=self.company.get("direccion", ""),
            dNumCas=int(self.company.get("numeroCasa", 0)),
            cDepEmi=self.company.get("departamento", 1),
            dDesDepEmi=self.company.get("departamentoDescripcion", ""),
            cDisEmi=str(self.company.get("distrito", 0)) or None,
            cCiuEmi=str(self.company.get("ciudad", "")),
            dDesCiuEmi=self.company.get("ciudadDescripcion", ""),
            dTelEmi=self.company.get("telefono", ""),
            dEmailE=self.company.get("email", ""),
            gActEco=[
                TgActEco(
                    cActEco=self.company.get("actividadEconomicaCodigo", ""),
                    dDesActEco=self.company.get("actividadEconomica", ""),
                )
            ],
        )

    def _build_gDatRec(self) -> TgDatRec:
        """Grupo D: Receiver (customer) data."""
        cliente = self.data.get("cliente", {})
        rec = TgDatRec(
            iNatRec=cliente.get("naturalezaReceptor", "1"),
            iTiOpe=cliente.get("tipoOperacion", "1"),
            cPaisRec=cliente.get("pais", "PRY"),
            dDesPaisRe=cliente.get("paisDescripcion", "Paraguay"),
            dNomRec=cliente.get("razonSocial", ""),
            dNomFanRec=cliente.get("nombreFantasia", ""),
            dDirRec=cliente.get("direccion", ""),
        )
        if cliente.get("ruc"):
            rec.dRucRec = cliente["ruc"]
        if cliente.get("dvReceptor"):
            rec.dDVRec = cliente["dvReceptor"]
        if cliente.get("tipoContribuyente"):
            rec.iTiContRec = cliente["tipoContribuyente"]
        if cliente.get("departamento"):
            rec.cDepRec = cliente["departamento"]
        if cliente.get("ciudad"):
            rec.cCiuRec = cliente["ciudad"]
        if cliente.get("email"):
            rec.dEmailRec = cliente["email"]
        if cliente.get("telefono"):
            rec.dTelRec = cliente["telefono"]
        if cliente.get("celular"):
            rec.dCelRec = cliente["celular"]
        if cliente.get("documentoTipo"):
            rec.iTipIDRec = str(cliente["documentoTipo"])
        if cliente.get("documentoNumero"):
            rec.dNumIDRec = cliente["documentoNumero"]
        return rec

    def _build_gDtipDE(self) -> TgDtipDe:
        """Grupo E: Document type specifics + items."""
        dtip = TgDtipDe()

        doc_type = self.data.get("tipoDocumento", 1)

        # Factura electrónica (tipo 1)
        if doc_type == 1:
            factura = self.data.get("factura", {})
            presencia = factura.get("presencia", 1)
            dtip.gCamFE = TgCamFe(
                iIndPres=presencia,
                dDesIndPres=_IND_PRES_DESC.get(
                    presencia, TdDesIndPresValue.OPERACI_N_PRESENCIAL
                ),
            )

        # Autofactura electrónica (tipo 4)
        elif doc_type == 4:
            factura = self.data.get("factura", {})
            presencia = factura.get("presencia", 1)
            dtip.gCamFE = TgCamFe(
                iIndPres=presencia,
                dDesIndPres=_IND_PRES_DESC.get(
                    presencia, TdDesIndPresValue.OPERACI_N_PRESENCIAL
                ),
            )
            # AFE-specific data
            afe_data = self.data.get("autofactura")
            if afe_data:
                dtip.gCamAE = self._build_gCamAE(afe_data)

        # Nota de crédito (tipo 5) or Nota de débito (tipo 6)
        elif doc_type in (5, 6):
            mot_emi = self.data.get("motivoEmision", 1)
            dtip.gCamNCDE = TgCamNcde(
                iMotEmi=str(mot_emi),
                dDesMotEmi=_MOT_EMI_DESC.get(mot_emi, TdDesMotEmi.ANULACI_N),
            )

        # Nota de remisión (tipo 7)
        elif doc_type == 7:
            remision = self.data.get("remision", {})
            dtip.gCamNRE = TgCamNre(
                iMotEmiNR=remision.get("motivo", 1),
                iRespEmiNR=TiRespEmiNr.VALUE_1,
            )

        # Payment condition (lives inside gDtipDE)
        cond = self.data.get("condicion", {})
        cond_ope = cond.get("tipo", 1)
        cam_cond = TgCamCond(
            iCondOpe=cond_ope,
            dDCondOpe=_COND_OPE_DESC.get(cond_ope, TdDcondOpe.CONTADO),
        )

        # Payment details
        if cond_ope == 1:
            # Contado — build gPaConEIni
            cam_cond.gPaConEIni = self._build_gPaConEIni(cond)
        elif cond_ope == 2:
            # Crédito — build gPagCred
            cam_cond.gPagCred = self._build_gPagCred(cond)

        dtip.gCamCond = cam_cond

        # Items
        dtip.gCamItem = self._build_gCamItems()

        return dtip

    def _build_gPaConEIni(self, cond: dict) -> list:
        """Build cash payment entries (gPaConEIni → TgPagCont[])."""
        entregas = cond.get("entregas", [])
        result = []
        for entrega in entregas:
            tipo_pago = entrega.get("tipo", 1)
            currency_name = entrega.get("moneda", "PYG")
            pag_cont = TgPagCont(
                iTiPago=_TIP_PAGO_CODE.get(tipo_pago, TiTiPago.VALUE_1),
                dDesTiPag=_TIP_PAGO_DESC.get(tipo_pago, TdDesTiPag.EFECTIVO),
                dMonTiPag=Decimal(str(entrega.get("monto", 0))),
                cMoneTiPag=_get_currency_enum(currency_name),
                dDMoneTiPag=_get_currency_desc(currency_name),
            )
            # Exchange rate for payment if not PYG
            if currency_name != "PYG":
                tipo_cambio = self.data.get("tipoCambio", 0)
                if tipo_cambio:
                    pag_cont.dTiCamTiPag = Decimal(str(tipo_cambio))
            result.append(pag_cont)
        return result

    def _build_gPagCred(self, cond: dict) -> TgPagCred:
        """Build credit payment data (gPagCred → TgPagCred)."""
        credito = cond.get("credito", {})
        tipo_cred = credito.get("tipo", 1)  # 1=Plazo, 2=Cuotas

        pag_cred = TgPagCred(
            iCondCred=TgPagCredICondCred(tipo_cred),
            dDCondCred=(TdDcondCred.PLAZO if tipo_cred == 1 else TdDcondCred.CUOTA),
        )

        if credito.get("plazo"):
            pag_cred.dPlazoCre = credito["plazo"]
        if credito.get("cuotas"):
            pag_cred.dCuotas = credito["cuotas"]

        # Build installments
        cuotas_data = credito.get("infoCuotas", [])
        cuotas_list = []
        for cuota in cuotas_data:
            g_cuota = TgCuotas(
                dMonCuota=Decimal(str(cuota.get("monto", 0))),
            )
            if cuota.get("vencimiento"):
                g_cuota.dVencCuo = cuota["vencimiento"]
            cuotas_list.append(g_cuota)
        if cuotas_list:
            pag_cred.gCuotas = cuotas_list

        return pag_cred

    def _build_gCamAE(self, afe_data: dict) -> TgCamAe:
        """Build Autofactura data (Grupo E — gCamAE)."""
        return TgCamAe(
            iTipCons=afe_data.get("tipoConstancia", 1),
            dDesTipCons=str(afe_data.get("tipoConstancia", 1)),
            dNumCons=afe_data.get("numeroConstancia", ""),
            dNumControl=afe_data.get("numeroControl", ""),
            iTipIDVen=str(afe_data.get("tipoDocumentoVendedor", 1)),
            dDTipIDVen=str(afe_data.get("tipoDocumentoVendedor", 1)),
            dNumIDVen=afe_data.get("numeroDocumentoVendedor", ""),
            dNomVen=afe_data.get("nombreVendedor", ""),
            dDirVen=afe_data.get("direccionVendedor", ""),
            dNumCasVen=afe_data.get("numeroCasaVendedor", 0),
            cDepVen=afe_data.get("departamentoVendedor", 1),
            dDesDepVen=str(afe_data.get("departamentoVendedor", 1)),
            cCiuVen=afe_data.get("ciudadVendedor", 1),
            dDesCiuVen=str(afe_data.get("ciudadVendedor", 1)),
            dDirProv=afe_data.get("direccionProvision", ""),
            cDepProv=afe_data.get("departamentoProvision", 1),
            dDesDepProv=str(afe_data.get("departamentoProvision", 1)),
            cDisProv=afe_data.get("distritoProvision", 1),
            dDesDisProv=str(afe_data.get("distritoProvision", 1)),
            cCiuProv=afe_data.get("ciudadProvision", 1),
            dDesCiuProv=str(afe_data.get("ciudadProvision", 1)),
        )

    def _build_gTransp(self, transp_data: dict) -> TgTransp:
        """Grupo G: Transport data."""
        mod_trans = transp_data.get("modalidad", 1)
        transp = TgTransp(
            iModTrans=TiModTrans(mod_trans),
            dDesModTrans=_MOD_TRANS_DESC.get(mod_trans, TdDesModTrans.TERRESTRE),
        )

        # Transport type
        tip_trans = transp_data.get("tipo")
        if tip_trans:
            transp.iTipTrans = TiTtrans(tip_trans)
            transp.dDesTipTrans = _TIP_TRANS_DESC.get(tip_trans, TdDesTtrans.PROPIO)

        # Freight responsibility
        resp_flete = transp_data.get("responsableFlete")
        if resp_flete:
            transp.iRespFlete = TiRespFlete(resp_flete)

        # Incoterm
        cond_neg = transp_data.get("condicionNegociacion")
        if cond_neg:
            transp.cCondNeg = TcCondNeg(cond_neg)

        # Manifest number
        if transp_data.get("numeroManifiesto"):
            transp.dNuManif = transp_data["numeroManifiesto"]

        # Dates
        if transp_data.get("fechaInicio"):
            transp.dIniTras = transp_data["fechaInicio"]
        if transp_data.get("fechaFin"):
            transp.dFinTras = transp_data["fechaFin"]

        # Departure point (gCamSal)
        salida = transp_data.get("salida")
        if salida:
            transp.gCamSal = TgCamSal(
                dDirLocSal=salida.get("direccion", ""),
                dNumCasSal=salida.get("numeroCasa", 0),
                cDepSal=salida.get("departamento", 1),
                dDesDepSal=str(salida.get("departamento", 1)),
                cCiuSal=salida.get("ciudad", 1),
                dDesCiuSal=str(salida.get("ciudad", 1)),
            )

        # Delivery points (gCamEnt[])
        entregas = transp_data.get("entregas", [])
        if entregas:
            transp.gCamEnt = [
                TgCamEnt(
                    dDirLocEnt=e.get("direccion", ""),
                    dNumCasEnt=e.get("numeroCasa", 0),
                    cDepEnt=e.get("departamento", 1),
                    dDesDepEnt=str(e.get("departamento", 1)),
                    cCiuEnt=e.get("ciudad", 1),
                    dDesCiuEnt=str(e.get("ciudad", 1)),
                )
                for e in entregas
            ]

        # Vehicles (gVehTras[])
        vehiculos = transp_data.get("vehiculos", [])
        if vehiculos:
            transp.gVehTras = [
                TgVehTras(
                    dTiVehTras=_MOD_TRANS_DESC.get(mod_trans, TdDesModTrans.TERRESTRE),
                    dMarVeh=v.get("marca", ""),
                    dNroIDVeh=v.get("numero", ""),
                )
                for v in vehiculos
            ]

        # Transporter (gCamTrans)
        transportista = transp_data.get("transportista")
        if transportista:
            cam_trans = TgCamTrans(
                iNatTrans=transportista.get("naturaleza", "1"),
                dNomTrans=transportista.get("nombre", ""),
                dNumIDChof=transportista.get("choferDocumento", ""),
                dNomChof=transportista.get("choferNombre", ""),
            )
            if transportista.get("ruc"):
                cam_trans.dRucTrans = transportista["ruc"]
            if transportista.get("dv"):
                cam_trans.dDVTrans = transportista["dv"]
            transp.gCamTrans = cam_trans

        return transp

    def _build_gCamItems(self) -> list:
        """Grupo E8: Invoice line items."""
        items = []
        for item_data in self.data.get("items", []):
            iva_tipo = item_data.get("ivaTipo", 1)
            iva_rate = item_data.get("iva", 10)
            base_gravada = Decimal(str(item_data.get("baseGravada", 0)))
            liquidacion_iva = Decimal(str(item_data.get("liquidacionIva", 0)))
            precio = Decimal(str(item_data.get("precioUnitario", 0)))
            cantidad = Decimal(str(item_data.get("cantidad", 1)))
            total_item = precio * cantidad

            item = TgCamItem(
                dCodInt=item_data.get("codigo", ""),
                dDesProSer=item_data.get("descripcion", ""),
                cUniMed=item_data.get("unidadMedida", 77),
                dDesUniMed="UNI",
                dCantProSer=cantidad,
                gValorItem=TgValorItem(
                    dPUniProSer=precio,
                    dDescItem=Decimal("0"),
                    dTotOpeItem=total_item,
                ),
                gCamIVA=TgCamIva(
                    iAfecIVA=iva_tipo,
                    dDesAfecIVA=_AFEC_IVA_DESC.get(iva_tipo, TdDesAfecIva.GRAVADO_IVA),
                    dPropIVA=item_data.get("ivaBase", 100),
                    dTasaIVA=iva_rate,
                    dBasGravIVA=base_gravada,
                    dLiqIVAItem=liquidacion_iva,
                ),
            )
            if item_data.get("ncm"):
                item.dNCM = item_data["ncm"]
            items.append(item)
        return items

    def _build_gTotSub(self) -> TgTotSub:
        """Grupo F: Totals."""
        totales = self.data.get("totales", {})
        return TgTotSub(
            dSubExe=Decimal(str(totales.get("totalExento", 0))),
            dSub5=Decimal(str(totales.get("totalGravado5", 0))),
            dSub10=Decimal(str(totales.get("totalGravado10", 0))),
            dTotOpe=Decimal(str(totales.get("totalOperacion", 0))),
            dTotDesc=Decimal("0"),
            dPorcDescTotal=Decimal("0"),
            dDescTotal=Decimal("0"),
            dAnticipo=Decimal("0"),
            dRedon=Decimal("0"),
            dTotGralOpe=Decimal(str(totales.get("totalPYG", 0))),
            dTotIVA=Decimal(str(totales.get("totalIva", 0))),
            dIVA5=Decimal(str(totales.get("liquidacionIva5", 0))),
            dIVA10=Decimal(str(totales.get("liquidacionIva10", 0))),
            dBaseGrav5=Decimal(str(totales.get("baseGravada5", 0))),
            dBaseGrav10=Decimal(str(totales.get("baseGravada10", 0))),
            dTBasGraIVA=Decimal(str(totales.get("totalBaseGravada", 0))),
        )

    def _build_gCamDEAsoc(self, docs: list) -> list:
        """Grupo H: Associated documents."""
        result = []
        for doc in docs:
            tip_doc_aso = doc.get("tipoAsociacion", 1)
            assoc = TgCamDeasoc(
                iTipDocAso=tip_doc_aso,
                dDesTipDocAso=_TIP_DOC_ASO_DESC.get(
                    tip_doc_aso, TdDesTipDocAso.ELECTR_NICO
                ),
            )
            if doc.get("cdc"):
                assoc.dCdCDERef = doc["cdc"]
            if doc.get("timbrado"):
                assoc.dNTimDI = doc["timbrado"]
            if doc.get("establecimiento"):
                assoc.dEstDocAso = doc["establecimiento"]
            if doc.get("punto"):
                assoc.dPExpDocAso = doc["punto"]
            if doc.get("numero"):
                assoc.dNumDocAso = doc["numero"]
            if doc.get("fecha"):
                assoc.dFecEmiDI = doc["fecha"]
            result.append(assoc)
        return result
