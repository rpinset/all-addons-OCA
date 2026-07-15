# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

"""
RDeBuilder: Converts invoice_data dict → RDe binding object (SIFEN v150).

Usa los bindings v150 de la librería pysifen (pysifen.de.bindings.de_v150),
generados desde el XSD oficial del SET, con nombres de campo en originalCase
(dSisFact, gValorRestaItem, dBasExe).
"""

import logging
from datetime import datetime
from decimal import Decimal

from pysifen.de.bindings.de_v150.de_types_v150 import (
    TcCondNeg,
    TdCondTiCam,
    TdDcondCred,
    TdDcondOpe,
    TdDesAfecIva,
    TdDesIndPresValue,
    TdDesModTrans,
    TdDesMotEmi,
    TdDesTiDe,
    TdDesTimp,
    TdDesTiPagValue,
    TdDesTipDocAso,
    TdDesTipEmi,
    TdDesTtrans,
    TiModTrans,
    TiRespEmiNr,
    TiRespFlete,
    TiTimp,
    TiTiPago,
    TiTtrans,
)
from pysifen.de.bindings.de_v150.de_v150 import (
    RDe,
    TDe,
    TgActEco,
    TgCamAe,
    TgCamCond,
    TgCamDeasoc,
    TgCamFe,
    TgCamFuFd,
    TgCamItem,
    TgCamIva,
    TgCamNcde,
    TgCamNre,
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
    TgValorRestaItem,
)
from pysifen.de.bindings.de_v150.monedas_v150 import CMondT
from pysifen.de.bindings.de_v150.xmldsig_core_schema import (
    CanonicalizationMethod,
    Signature,
    SignatureMethod,
    SignatureValue,
    SignedInfo,
)

_logger = logging.getLogger(__name__)

# === Lookup tables for SIFEN description enums ===

_TIP_EMI_DESC = {1: TdDesTipEmi.NORMAL, 2: TdDesTipEmi.CONTINGENCIA}

_TI_DE_DESC = {
    1: TdDesTiDe.FACTURA_ELECTR_NICA,
    4: TdDesTiDe.FACTURA_ELECTR_NICA,
    5: TdDesTiDe.NOTA_DE_CR_DITO_ELECTR_NICA,
    6: TdDesTiDe.NOTA_DE_D_BITO_ELECTR_NICA,
    7: TdDesTiDe.FACTURA_ELECTR_NICA,
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
    1: TdDesMotEmi.DEVOLUCI_N_Y_AJUSTE_DE_PRECIOS,
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
    2: TdDesAfecIva.EXONERADO_ART_100_LEY_6380_2019,
    3: TdDesAfecIva.EXENTO,
    4: TdDesAfecIva.GRAVADO_PARCIAL_GRAV_EXENTO,
}

_TIP_DOC_ASO_DESC = {
    1: TdDesTipDocAso.ELECTR_NICO,
    2: TdDesTipDocAso.IMPRESO,
}

_CURRENCY_MAP = {m.value: m for m in CMondT}

_TIP_PAGO_DESC = {
    1: TdDesTiPagValue.EFECTIVO,
    2: TdDesTiPagValue.CHEQUE,
    3: TdDesTiPagValue.TARJETA_DE_CR_DITO,
    4: TdDesTiPagValue.TARJETA_DE_D_BITO,
    5: TdDesTiPagValue.TRANSFERENCIA,
    6: TdDesTiPagValue.GIRO,
    7: TdDesTiPagValue.BILLETERA_ELECTR_NICA,
    8: TdDesTiPagValue.TARJETA_EMPRESARIAL,
    9: TdDesTiPagValue.VALE,
    10: TdDesTiPagValue.RETENCI_N,
    11: TdDesTiPagValue.PAGO_POR_ANTICIPO,
}

_TIP_PAGO_CODE = {i: TiTiPago(i) for i in range(1, 12)}

_MOD_TRANS_DESC = {
    1: TdDesModTrans.TERRESTRE,
    2: TdDesModTrans.FLUVIAL,
    3: TdDesModTrans.A_REO,
    4: TdDesModTrans.MULTIMODAL,
}

_TIP_TRANS_DESC = {
    1: TdDesTtrans.PROPIO,
    2: TdDesTtrans.TERCERO,
}


def _get_currency_enum(currency_name):
    return _CURRENCY_MAP.get(currency_name, CMondT.PYG)


def _get_currency_desc(currency_name):
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
    """Build SIFEN v150 RDe object from invoice_data dict."""

    def __init__(self, invoice_data, company_data, cdc):
        self.data = invoice_data
        self.company = company_data
        self.cdc = cdc

    def build(self):
        """Build complete RDe (v150)."""
        tde = TDe(
            Id=self.cdc,
            dDVId=self.cdc[-1],
            dFecFirma=self.data.get("fechaFirma", self.data.get("fecha", "")),
            dSisFact=int(self.data.get("sistemaFacturacion", 1)),
            gOpeDE=self._build_gOpeDE(),
            gTimb=self._build_gTimb(),
            gDatGralOpe=self._build_gDatGralOpe(),
            gDtipDE=self._build_gDtipDE(),
            gTotSub=self._build_gTotSub(),
        )

        transp_data = self.data.get("transporte")
        if transp_data:
            tde.gDtipDE.gTransp = self._build_gTransp(transp_data)

        assoc_docs = self.data.get("documentosAsociados", [])
        if assoc_docs:
            tde.gCamDEAsoc = self._build_gCamDEAsoc(assoc_docs)

        empty_signature = Signature(
            SignedInfo=SignedInfo(
                CanonicalizationMethod=CanonicalizationMethod(Algorithm=""),
                SignatureMethod=SignatureMethod(Algorithm=""),
            ),
            SignatureValue=SignatureValue(),
        )
        return RDe(
            dVerFor=150,
            DE=tde,
            Signature=empty_signature,
            gCamFuFD=TgCamFuFd(dCarQR=""),
        )

    def _build_gOpeDE(self):
        tip_emi = self.data.get("tipoEmision", 1)
        return TgCopeDe(
            iTipEmi=tip_emi,
            dDesTipEmi=_TIP_EMI_DESC.get(tip_emi, TdDesTipEmi.NORMAL),
            dCodSeg=self.data.get("codigoSeguridadAleatorio", "000000000"),
        )

    def _build_gTimb(self):
        ti_de = self.data.get("tipoDocumento", 1)
        gtimb = TgDtim(
            iTiDE=ti_de,
            dDesTiDE=_TI_DE_DESC.get(ti_de, TdDesTiDe.FACTURA_ELECTR_NICA),
            dNumTim=self.data.get("timbrado", ""),
            dEst=self.data.get("establecimiento", "001"),
            dPunExp=self.data.get("punto", "001"),
            dNumDoc=self.data.get("numero", "0000001"),
            dFeIniT=self.data.get("timbradoFechaInicio", ""),
        )
        return gtimb

    def _build_gDatGralOpe(self):
        fecha_str = self.data.get("fecha", datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        return TgDaGoc(
            dFeEmiDE=fecha_str,
            gOpeCom=self._build_gOpeCom(),
            gEmis=self._build_gEmis(),
            gDatRec=self._build_gDatRec(),
        )

    def _build_gOpeCom(self):
        currency_name = self.data.get("moneda", "PYG")
        cond_ti_cam = self.data.get("condicionTipoCambio", 1)
        tipo_cambio = self.data.get("tipoCambio", 0)

        ope_com = TgOpeCom(
            iTImp=TiTimp.VALUE_1,
            dDesTImp=TdDesTimp.IVA,
            cMoneOpe=_get_currency_enum(currency_name),
            dDesMoneOpe=_get_currency_desc(currency_name),
        )

        tip_tra = self.data.get("tipoTransaccion")
        if tip_tra:
            ope_com.iTipTra = tip_tra

        if currency_name != "PYG":
            ope_com.dCondTiCam = TdCondTiCam(cond_ti_cam)
            if tipo_cambio:
                ope_com.dTiCam = Decimal(str(tipo_cambio))

        return ope_com

    def _build_gEmis(self):
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
            cDisEmi=(
                int(self.company["distrito"]) if self.company.get("distrito") else None
            ),
            cCiuEmi=int(self.company.get("ciudad", 1) or 1),
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

    def _build_gDatRec(self):
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

    def _build_gDtipDE(self):
        dtip = TgDtipDe()
        doc_type = self.data.get("tipoDocumento", 1)

        if doc_type == 1:
            factura = self.data.get("factura", {})
            presencia = factura.get("presencia", 1)
            dtip.gCamFE = TgCamFe(
                iIndPres=presencia,
                dDesIndPres=_IND_PRES_DESC.get(
                    presencia, TdDesIndPresValue.OPERACI_N_PRESENCIAL
                ),
            )
        elif doc_type == 4:
            factura = self.data.get("factura", {})
            presencia = factura.get("presencia", 1)
            dtip.gCamFE = TgCamFe(
                iIndPres=presencia,
                dDesIndPres=_IND_PRES_DESC.get(
                    presencia, TdDesIndPresValue.OPERACI_N_PRESENCIAL
                ),
            )
            afe_data = self.data.get("autofactura")
            if afe_data:
                dtip.gCamAE = self._build_gCamAE(afe_data)
        elif doc_type in (5, 6):
            mot_emi = self.data.get("motivoEmision", 1)
            dtip.gCamNCDE = TgCamNcde(
                iMotEmi=str(mot_emi),
                dDesMotEmi=_MOT_EMI_DESC.get(
                    mot_emi, TdDesMotEmi.DEVOLUCI_N_Y_AJUSTE_DE_PRECIOS
                ),
            )
        elif doc_type == 7:
            remision = self.data.get("remision", {})
            dtip.gCamNRE = TgCamNre(
                iMotEmiNR=remision.get("motivo", 1),
                iRespEmiNR=TiRespEmiNr.VALUE_1,
            )

        cond = self.data.get("condicion", {})
        cond_ope = cond.get("tipo", 1)
        cam_cond = TgCamCond(
            iCondOpe=cond_ope,
            dDCondOpe=_COND_OPE_DESC.get(cond_ope, TdDcondOpe.CONTADO),
        )
        if cond_ope == 1:
            cam_cond.gPaConEIni = self._build_gPaConEIni(cond)
        elif cond_ope == 2:
            cam_cond.gPagCred = self._build_gPagCred(cond)
        dtip.gCamCond = cam_cond

        dtip.gCamItem = self._build_gCamItems()
        return dtip

    def _build_gPaConEIni(self, cond):
        entregas = cond.get("entregas", [])
        result = []
        for entrega in entregas:
            tipo_pago = entrega.get("tipo", 1)
            currency_name = entrega.get("moneda", "PYG")
            pag_cont = TgPagCont(
                iTiPago=_TIP_PAGO_CODE.get(tipo_pago, TiTiPago.VALUE_1),
                dDesTiPag=_TIP_PAGO_DESC.get(tipo_pago, TdDesTiPagValue.EFECTIVO),
                dMonTiPag=Decimal(str(entrega.get("monto", 0))),
                cMoneTiPag=_get_currency_enum(currency_name),
                dDMoneTiPag=_get_currency_desc(currency_name),
            )
            if currency_name != "PYG":
                tipo_cambio = self.data.get("tipoCambio", 0)
                if tipo_cambio:
                    pag_cont.dTiCamTiPag = Decimal(str(tipo_cambio))
            result.append(pag_cont)
        return result

    def _build_gPagCred(self, cond):
        credito = cond.get("credito", {})
        tipo_cred = credito.get("tipo", 1)
        pag_cred = TgPagCred(
            iCondCred=TgPagCredICondCred(tipo_cred),
            dDCondCred=(TdDcondCred.PLAZO if tipo_cred == 1 else TdDcondCred.CUOTA),
        )
        if credito.get("plazo"):
            pag_cred.dPlazoCre = credito["plazo"]
        if credito.get("cuotas"):
            pag_cred.dCuotas = credito["cuotas"]
        cuotas_list = []
        for cuota in credito.get("infoCuotas", []):
            g_cuota = TgCuotas(
                cMoneCuo=_get_currency_enum(cuota.get("moneda", "PYG")),
                dDMoneCuo=_get_currency_desc(cuota.get("moneda", "PYG")),
                dMonCuota=Decimal(str(cuota.get("monto", 0))),
            )
            if cuota.get("vencimiento"):
                g_cuota.dVencCuo = cuota["vencimiento"]
            cuotas_list.append(g_cuota)
        if cuotas_list:
            pag_cred.gCuotas = cuotas_list
        return pag_cred

    def _build_gCamAE(self, afe_data):
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

    def _build_gTransp(self, transp_data):
        mod_trans = transp_data.get("modalidad", 1)
        transp = TgTransp(
            iModTrans=TiModTrans(mod_trans),
            dDesModTrans=_MOD_TRANS_DESC.get(mod_trans, TdDesModTrans.TERRESTRE),
        )
        tip_trans = transp_data.get("tipo")
        if tip_trans:
            transp.iTipTrans = TiTtrans(tip_trans)
            transp.dDesTipTrans = _TIP_TRANS_DESC.get(tip_trans, TdDesTtrans.PROPIO)
        resp_flete = transp_data.get("responsableFlete")
        if resp_flete:
            transp.iRespFlete = TiRespFlete(resp_flete)
        cond_neg = transp_data.get("condicionNegociacion")
        if cond_neg:
            transp.cCondNeg = TcCondNeg(cond_neg)
        return transp

    def _build_gCamItems(self):
        items = []
        for item_data in self.data.get("items", []):
            iva_tipo = item_data.get("ivaTipo", 1)
            iva_rate = item_data.get("iva", 10)
            base_gravada = Decimal(str(item_data.get("baseGravada", 0)))
            liquidacion_iva = Decimal(str(item_data.get("liquidacionIva", 0)))
            precio = Decimal(str(item_data.get("precioUnitario", 0)))
            cantidad = Decimal(str(item_data.get("cantidad", 1)))
            total_item = precio * cantidad
            base_exenta = total_item if iva_tipo == 3 else Decimal("0")

            item = TgCamItem(
                dCodInt=item_data.get("codigo", ""),
                dDesProSer=item_data.get("descripcion", ""),
                cUniMed=item_data.get("unidadMedida", 77),
                dDesUniMed="UNI",
                dCantProSer=cantidad,
                gValorItem=TgValorItem(
                    dPUniProSer=precio,
                    dTotBruOpeItem=total_item,
                    gValorRestaItem=TgValorRestaItem(
                        dDescItem=Decimal("0"),
                        dTotOpeItem=total_item,
                    ),
                ),
                gCamIVA=TgCamIva(
                    iAfecIVA=iva_tipo,
                    dDesAfecIVA=_AFEC_IVA_DESC.get(iva_tipo, TdDesAfecIva.GRAVADO_IVA),
                    dPropIVA=item_data.get("ivaBase", 100),
                    dTasaIVA=iva_rate,
                    dBasGravIVA=base_gravada,
                    dLiqIVAItem=liquidacion_iva,
                    dBasExe=base_exenta,
                ),
            )
            if item_data.get("ncm"):
                item.dNCM = item_data["ncm"]
            items.append(item)
        return items

    def _build_gTotSub(self):
        totales = self.data.get("totales", {})
        return TgTotSub(
            dSubExe=Decimal(str(totales.get("totalExento", 0))),
            dSub5=Decimal(str(totales.get("totalGravado5", 0))),
            dSub10=Decimal(str(totales.get("totalGravado10", 0))),
            dTotOpe=Decimal(str(totales.get("totalOperacion", 0))),
            dTotDesc=Decimal("0"),
            dTotDescGlotem=Decimal("0"),
            dTotAntItem=Decimal("0"),
            dTotAnt=Decimal("0"),
            dPorcDescTotal=Decimal("0"),
            dDescTotal=Decimal("0"),
            dAnticipo=Decimal("0"),
            dRedon=Decimal("0"),
            dTotGralOpe=Decimal(str(totales.get("totalPYG", 0))),
            dIVA5=Decimal(str(totales.get("liquidacionIva5", 0))),
            dIVA10=Decimal(str(totales.get("liquidacionIva10", 0))),
            dTotIVA=Decimal(str(totales.get("totalIva", 0))),
            dBaseGrav5=Decimal(str(totales.get("baseGravada5", 0))),
            dBaseGrav10=Decimal(str(totales.get("baseGravada10", 0))),
            dTBasGraIVA=Decimal(str(totales.get("totalBaseGravada", 0))),
        )

    def _build_gCamDEAsoc(self, docs):
        result = []
        for doc in docs:
            tip_doc_aso = doc.get("tipoAsociacion", 1)
            cam_asoc = TgCamDeasoc(
                iTipDocAso=tip_doc_aso,
                dDesTipDocAso=_TIP_DOC_ASO_DESC.get(
                    tip_doc_aso, TdDesTipDocAso.ELECTR_NICO
                ),
            )
            if doc.get("cdc"):
                cam_asoc.d_cdcderef = doc["cdc"]
            if doc.get("timbrado"):
                cam_asoc.dNumTim = doc["timbrado"]
            result.append(cam_asoc)
        return result
