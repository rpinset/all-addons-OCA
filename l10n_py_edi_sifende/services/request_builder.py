# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import re
from decimal import ROUND_HALF_UP, Decimal

from odoo.exceptions import UserError

PLACEHOLDER_ADDRESS = "N/A"
PYG = "PYG"

# l10n_py_doc_type de OCA (1 CI, 2 pasaporte, 3 carnet, 4 innominado) -> tiTipDocRec
OCA_DOC_TYPE_TO_SIFEN = {1: 1, 2: 2, 3: 4, 4: 5}
# l10n_py_nre_motive de OCA (4 importación, 5 entre locales, 6 otros) -> iMotivTras
OCA_NRE_MOTIVE_TO_SIFEN = {1: 1, 2: 2, 3: 3, 4: 5, 5: 7, 6: 99}
SIFEN_MOTIVE_OTHER = 99
SIFEN_CARD_OTHER = 99
SIFEN_CARD_PROCESSING_OTHER = 9
CARD_PAYMENT_TYPES = (3, 4)
CHEQUE_PAYMENT_TYPE = 2
PRINTED_DOC_VEHICLE_PLATE = 2
AIR_TRANSPORT = "AEREO"

NCM_RE = re.compile(r"^(?=.*[1-9])\d{6,8}$")
PYG_ROUNDING_STEP = Decimal(50)


def _money(value, decimals):
    value = Decimal(str(value)).quantize(Decimal(10) ** -decimals, ROUND_HALF_UP)
    return int(value) if decimals == 0 else float(value)


def _number(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def _prune(value):
    if isinstance(value, dict):
        cleaned = {k: _prune(v) for k, v in value.items()}
        return {
            k: v for k, v in cleaned.items() if v is not None and v not in ("", {}, [])
        }
    if isinstance(value, list):
        return [_prune(v) for v in value]
    return value


def _phone(value):
    cleaned = re.sub(r"[^\d+]", "", value or "")
    return cleaned if 6 <= len(cleaned) <= 15 else None


def _extra(entity):
    return entity.get("sifende") or {}


class SifendeRequestBuilder:
    """Traduce el dict de `_prepare_edi_document_data` al request de Sifende."""

    def __init__(self, env, enum_name):
        self.env = env
        self._enum_name = enum_name

    def build(self, data):
        code = int(data["tipoDocumento"])
        extra = data.get("sifende") or {}
        request = self._header(data, code)
        if code == 7:
            request.update(self._remision(data, extra))
        elif code == 4:
            request.update(self._autofactura(data, extra))
        else:
            request.update(self._comercial(data, extra, code))
        return _prune(request)

    def _name(self, category, code, fallback=None):
        name = self._enum_name(category, int(code))
        if name:
            return name
        if fallback:
            return fallback
        raise UserError(
            self.env._(
                "El catálogo de Sifende no tiene el valor %(code)s en «%(cat)s».",
                code=code,
                cat=category,
            )
        )

    def _int(self, value, label):
        try:
            return int(value)
        except (TypeError, ValueError) as e:
            raise UserError(
                self.env._(
                    "%(label)s debe ser numérico (valor actual: «%(value)s»).",
                    label=label,
                    value=value,
                )
            ) from e

    def _header(self, data, code):
        header = {
            "tipoDocumento": self._name("tipoDocumento", code),
            "fechaEmision": data["fecha"],
            "tipoEmision": self._name("tipoEmision", data["tipoEmision"]),
            "numeroEstablecimiento": self._int(
                data["establecimiento"], "El establecimiento"
            ),
            "puntoExpedicion": self._int(data["punto"], "El punto de expedición"),
            "numeroDocumento": self._int(data["numero"], "El número de documento"),
            "numeroTimbrado": self._int(data.get("timbrado"), "El timbrado"),
            "codigoSeguridad": data["codigoSeguridadAleatorio"],
        }
        if code != 7:
            header["monedaOperacion"] = data["moneda"]
            if data["moneda"] != PYG and data.get("tipoCambio"):
                header["tipoCambio"] = _number(data["tipoCambio"])
        return header

    # === Factura, nota de crédito y nota de débito ===

    def _comercial(self, data, extra, code):
        request = {
            "receptor": self._receptor(data, extra),
            "items": [
                self._item(item, data["moneda"]) for item in data.get("items") or []
            ],
        }
        if code == 1:
            request["tipoTransaccion"] = self._name(
                "tipoTransaccion", data["tipoTransaccion"]
            )
            request["indicadorPresencia"] = self._name(
                "indicadorPresencia", data["factura"]["presencia"]
            )
            request.update(self._condicion(data, extra))
            documents = self._associated(data.get("documentosAsociados"))
            request["documentosAsociados"] = documents
            if data.get("transporte"):
                request["transporte"] = self._transporte(
                    data["transporte"], extra.get("transporte")
                )
        else:
            if not extra.get("motivoEmision"):
                raise UserError(self.env._("Falta el motivo de emisión de la nota."))
            request["motivoEmision"] = self._name(
                "motivoEmision", extra["motivoEmision"]
            )
            documents = self._associated(data.get("documentosAsociados"))
            if documents:
                request["documentoAsociado"] = documents[0]
        return request

    def _item(self, item, currency):
        extra_item = _extra(item)
        unit_code = extra_item.get("unidadMedida") or item.get("unidadMedida") or 77
        iva_type = int(item["ivaTipo"])
        result = {
            "codigo": item["codigo"],
            "descripcion": item["descripcion"],
            "cantidad": _number(item["cantidad"]),
            "unidadMedida": self._name("unidadMedida", unit_code),
            "precioUnitario": _number(
                extra_item.get("precioUnitario", item["precioUnitario"])
            ),
            "afectacionTributaria": self._name("afectacionIVA", iva_type),
            "tasaIVA": int(item["iva"]),
        }
        result.update(self._discount(result["precioUnitario"], extra_item, currency))
        if iva_type == 4:
            result["propIVA"] = _number(item["ivaBase"])
        ncm = str(item.get("ncm") or "")
        if NCM_RE.match(ncm):
            result["ncm"] = ncm
        return result

    @staticmethod
    def _discount(unit_price, extra_item, currency):
        percent = extra_item.get("descuentoParticularPorcentaje")
        if not percent:
            return {}
        # en PYG Sifende redondea a entero el descuento derivado del porcentaje
        amount = Decimal(str(unit_price)) * Decimal(str(percent)) / 100
        amount = amount.quantize(Decimal(10) ** -8, ROUND_HALF_UP)
        if currency == PYG and amount != amount.quantize(Decimal(1), ROUND_HALF_UP):
            return {"descuentoParticular": _number(float(amount))}
        return {"descuentoParticularPorcentaje": percent}

    def _receptor(self, data, extra, address_required=False):
        customer = data["cliente"]
        extra_customer = extra.get("cliente") or {}
        nature = int(customer["naturalezaReceptor"])
        operation = int(customer["tipoOperacion"])
        address = (customer.get("direccion") or "").strip()
        if address.upper() == PLACEHOLDER_ADDRESS:
            address = ""
        receptor = {
            "tipoContribuyente": self._name("naturalezaReceptor", nature),
            "tipoOperacion": self._name("tipoOperacion", operation),
            "nombreRazonSocial": customer["razonSocial"],
            "direccion": address[:255],
            "numeroCasa": self._int(
                customer.get("numeroCasa") or 0, "El número de casa"
            ),
            "telefono": _phone(customer.get("telefono") or customer.get("celular")),
            "pais": customer.get("pais"),
        }
        if nature == 1:
            receptor["tipoContribuyenteReceptor"] = self._name(
                "tipoContribuyenteReceptor", customer["tipoContribuyente"]
            )
            receptor["numeroDocumento"] = customer["ruc"]
            receptor["digitoVerificador"] = customer["dvReceptor"]
        else:
            oca_type = int(customer.get("documentoTipo") or 1)
            receptor["tipoDocumento"] = self._name(
                "tipoDocumentoReceptor", OCA_DOC_TYPE_TO_SIFEN.get(oca_type, oca_type)
            )
            receptor["numeroDocumento"] = customer.get("documentoNumero")
        fantasy = customer.get("nombreFantasia")
        if fantasy and fantasy != customer["razonSocial"] and len(fantasy) >= 4:
            receptor["nombreFantasia"] = fantasy
        email = extra_customer.get("email") or customer.get("email")
        if email and "@" in email:
            receptor["email"] = email
        client_code = extra_customer.get("codigoCliente")
        if client_code and 3 <= len(client_code) <= 15:
            receptor["codigoCliente"] = client_code
        if operation != 4:
            self._receptor_location(receptor, extra_customer)
            if not (
                address and receptor.get("departamento") and receptor.get("ciudad")
            ):
                if address_required:
                    raise UserError(
                        self.env._(
                            "El receptor necesita dirección, departamento y ciudad: "
                            "complete la dirección e indique la «Ciudad SIFEN» en el "
                            "contacto."
                        )
                    )
                # SIFEN rechaza la dirección sin departamento ni ciudad (1324, 1327)
                receptor.pop("direccion", None)
                receptor.pop("numeroCasa", None)
        return receptor

    def _receptor_location(self, receptor, extra_customer):
        geography = extra_customer.get("geografia")
        if geography:
            receptor["departamento"] = self._name(
                "departamento", geography["departamento"]
            )
            receptor["codigoDistrito"] = geography["distrito"]
            receptor["ciudad"] = str(geography["ciudad"])

    def _condicion(self, data, extra):
        condition = data["condicion"]
        currency = data["moneda"]
        decimals = extra.get("decimales", 0 if currency == PYG else 2)
        if int(condition["tipo"]) == 1:
            entregas = condition.get("entregas") or []
            amounts = self._distribute(
                [entrega["monto"] for entrega in entregas],
                self._fiscal_total(extra, currency, decimals),
                decimals,
            )
            return {
                "condicionOperacion": self._name("condicionOperacion", 1),
                "pagos": [
                    self._pago(entrega, data, amount)
                    for entrega, amount in zip(entregas, amounts, strict=True)
                ],
            }
        return {
            "condicionOperacion": self._name("condicionOperacion", 2),
            "credito": self._credito(condition["credito"], extra, decimals, currency),
        }

    def _pago(self, entrega, data, amount):
        payment_type = int(entrega["tipo"])
        pago = {
            "tipoPago": self._name("tipoPago", payment_type),
            "montoPago": amount,
            "monedaPago": entrega["moneda"],
        }
        if entrega["moneda"] != PYG and data.get("tipoCambio"):
            pago["tipoCambio"] = _number(data["tipoCambio"])
        if payment_type == CHEQUE_PAYMENT_TYPE:
            pago["cheque"] = {
                "numeroCheque": entrega["cheque"]["numeroCheque"],
                "bancoCheque": entrega["cheque"]["bancoCheque"].strip(),
            }
        if payment_type in CARD_PAYMENT_TYPES:
            brand = int(
                ((data.get("sifende") or {}).get("tarjeta") or {}).get("tipoTarjeta")
                or SIFEN_CARD_OTHER
            )
            pago["tarjeta"] = {
                "tipoTarjeta": self._name("tipoTarjeta", brand),
                "formaProcesamientoPago": self._name(
                    "formaProcesamientoPago", SIFEN_CARD_PROCESSING_OTHER
                ),
            }
            # Sifende deriva la descripción del catálogo y la exige solo con OTRO
            if brand == SIFEN_CARD_OTHER:
                pago["tarjeta"]["descripcionTipoTarjeta"] = "Otro"
        return pago

    def _credito(self, credit, extra, decimals, currency=PYG):
        installments = credit.get("infoCuotas") or []
        if len(installments) < 2:
            return {
                "condicionCredito": self._name("condicionCredito", 1),
                "plazoCredito": credit.get("plazo"),
            }
        amounts = self._installment_amounts(
            installments,
            extra.get("montoTotal"),
            decimals,
            self._fiscal_total(extra, currency, decimals),
        )
        return {
            "condicionCredito": self._name("condicionCredito", 2),
            "cuotas": len(installments),
            "detalleCuotas": [
                {"monto": amount, "fechaVencimiento": quota["vencimiento"]}
                for amount, quota in zip(amounts, installments, strict=True)
            ],
        }

    @staticmethod
    def _fiscal_total(extra, currency, decimals):
        """Total que Sifende exige cubrir: en PYG baja a múltiplos de 50."""
        total = extra.get("totalOperacion", extra.get("montoTotal"))
        if total is None:
            return None
        total = Decimal(str(total)).quantize(Decimal(10) ** -decimals, ROUND_HALF_UP)
        return total - total % PYG_ROUNDING_STEP if currency == PYG else total

    @staticmethod
    def _distribute(amounts, target, decimals):
        """Reparte `target` en proporción a `amounts`; la última absorbe el resto."""
        unit = Decimal(10) ** -decimals
        values = [Decimal(str(amount)) for amount in amounts]
        total = sum(values)
        if target is None or not total:
            return [_money(value, decimals) for value in values]
        shares = [
            (value * target / total).quantize(unit, ROUND_HALF_UP) for value in values
        ]
        shares[-1] = target - sum(shares[:-1])
        return [_money(share, decimals) for share in shares]

    def _installment_amounts(self, installments, total, decimals, fiscal_total=None):
        unit = Decimal(10) ** -decimals
        amounts = [
            Decimal(str(quota["monto"])).quantize(unit, ROUND_HALF_UP)
            for quota in installments
        ]
        if total is not None:
            residue = Decimal(str(total)).quantize(unit, ROUND_HALF_UP) - sum(amounts)
            # solo el redondeo va a la última; una diferencia mayor es un dato roto
            if abs(residue) > unit * len(amounts):
                raise UserError(
                    self.env._("Las cuotas del plazo de pago no suman el total.")
                )
            amounts[-1] += residue
        return self._distribute(amounts, fiscal_total, decimals)

    def _associated(self, documents):
        result = []
        for doc in documents or []:
            kind = int(doc["tipoAsociacion"])
            if kind == 1:
                result.append(
                    {
                        "tipoDocumento": self._name("tipoDocumentoAsociado", 1),
                        "cdc": doc["cdc"],
                    }
                )
            elif kind == 2:
                result.append(
                    {
                        "tipoDocumento": self._name("tipoDocumentoAsociado", 2),
                        "numeroTimbrado": doc["timbrado"],
                        "establecimiento": doc["establecimiento"],
                        "puntoExpedicion": doc["punto"],
                        "numeroDocumento": doc["numero"],
                        "tipoDocumentoImpreso": self._name(
                            "tipoDocumentoImpreso", doc["tipoDocumentoImpreso"]
                        ),
                        "fechaEmision": doc["fecha"],
                    }
                )
        return result

    # === Nota de remisión ===

    def _remision(self, data, extra):
        remision = data.get("remision") or {}
        extra_remision = extra.get("remision") or {}
        oca_motive = int(remision.get("motivo") or 1)
        motive = OCA_NRE_MOTIVE_TO_SIFEN[oca_motive]
        request = {
            "receptor": self._receptor(data, extra, address_required=True),
            "items": [
                {
                    "codigo": item["codigo"],
                    "descripcion": item["descripcion"],
                    "cantidad": _number(item["cantidad"]),
                    "unidadMedida": self._name(
                        "unidadMedida", _extra(item).get("unidadMedida") or 77
                    ),
                    "ncm": item["ncm"]
                    if NCM_RE.match(str(item.get("ncm") or ""))
                    else None,
                }
                for item in data.get("items") or []
            ],
            "motivoTraslado": self._name("motivoTraslado", motive),
            "responsableEmision": self._name(
                "responsableEmision", extra_remision.get("responsableEmision") or 1
            ),
            "kilometrosRecorrido": extra_remision.get("kilometrosRecorrido"),
            "fechaFacturaFutura": remision.get("fechaEstimada"),
            "documentosAsociados": self._associated(data.get("documentosAsociados")),
        }
        if motive == SIFEN_MOTIVE_OTHER:
            request["descripcionMotivoTraslado"] = self.env._(
                "Otros motivos de traslado"
            )
        if data.get("transporte"):
            request["transporte"] = self._transporte(
                data["transporte"], extra.get("transporte")
            )
        return request

    def _transporte(self, transport, extra=None):
        extra = extra or {}
        mode = self._name("modalidadTransporte", transport["modalidad"])
        result = {
            "modalidad": mode,
            "incoterm": transport.get("condicionNegociacion"),
            "numeroManifiesto": transport.get("numeroManifiesto"),
            "numeroDespachoImportacion": extra.get("numeroDespachoImportacion"),
            "fechaInicioTraslado": transport.get("fechaInicio"),
            "fechaFinTraslado": transport.get("fechaFin"),
        }
        if transport.get("tipo"):
            result["tipoTransporte"] = self._name("tipoTransporte", transport["tipo"])
        if transport.get("responsableFlete"):
            result["responsableFlete"] = self._name(
                "responsableFlete", transport["responsableFlete"]
            )
        if transport.get("salida"):
            result["salida"] = self._local(transport["salida"], extra.get("salida"))
        if transport.get("entregas"):
            result["entregas"] = [
                self._local(delivery, _extra(delivery))
                for delivery in transport["entregas"]
            ]
        if transport.get("vehiculos"):
            result["vehiculos"] = [
                {
                    "tipoVehiculo": v.get("tipo"),
                    "marca": v.get("marca"),
                    "tipoIdentificacion": PRINTED_DOC_VEHICLE_PLATE,
                    "matricula": (v.get("numero") or "").strip(),
                    "numeroVuelo": _extra(v).get("numeroVuelo")
                    if mode == AIR_TRANSPORT
                    else None,
                }
                for v in transport["vehiculos"]
            ]
        if transport.get("transportista"):
            result["transportista"] = self._transportista(
                transport["transportista"], extra.get("transportista") or {}
            )
        return result

    def _transportista(self, carrier, extra):
        result = {
            "naturaleza": self._name("naturalezaReceptor", carrier["naturaleza"]),
            "nombreRazonSocial": carrier.get("nombre"),
            "domicilioFiscal": extra.get("domicilioFiscal"),
            "numeroDocumentoConductor": carrier.get("choferDocumento"),
            "nombreConductor": carrier.get("choferNombre"),
            "direccionConductor": extra.get("direccionConductor"),
            "nombreAgente": extra.get("nombreAgente"),
            "rucAgente": extra.get("rucAgente"),
            "digitoVerificadorAgente": extra.get("digitoVerificadorAgente"),
            "direccionAgente": extra.get("direccionAgente"),
        }
        if int(carrier["naturaleza"]) == 1:
            result["ruc"] = carrier.get("ruc")
            result["digitoVerificador"] = carrier.get("dv")
        else:
            document_type = extra.get("tipoDocumento")
            if document_type:
                result["tipoDocumento"] = self._name(
                    "tipoDocumentoTransportista", document_type
                )
            result["numeroDocumento"] = extra.get("numeroDocumento")
        return result

    def _local(self, place, geography):
        if not geography:
            raise UserError(
                self.env._("Falta la ciudad de «%s».", place.get("direccion"))
            )
        return {
            "direccion": place.get("direccion"),
            "numeroCasa": place.get("numeroCasa") or 0,
            "departamento": self._name("departamento", geography["departamento"]),
            "codigoDistrito": geography["distrito"],
            "ciudad": str(geography["ciudad"]),
        }

    # === Autofactura ===

    def _autofactura(self, data, extra):
        auto = data["autofactura"]
        extra_auto = extra.get("autofactura") or {}
        currency = data["moneda"]
        decimals = extra.get("decimales", 0 if currency == PYG else 2)
        doc_type = int(auto["tipoDocumentoVendedor"])
        nature = 1 if doc_type in (1, 4) else 2
        payment = (data["condicion"].get("entregas") or [{}])[0]
        payment_type = int(payment.get("tipo") or 1)
        amount = self._distribute(
            [payment.get("monto") or extra.get("montoTotal") or 0],
            self._fiscal_total(extra, currency, decimals),
            decimals,
        )[0]
        condition_payment = {
            "tipo": self._name("condicionOperacion", 1),
            "tipoPago": self._name("tipoPago", payment_type),
            "monedaPago": currency,
            "montoPago": amount,
        }
        if payment_type == CHEQUE_PAYMENT_TYPE:
            cheque = payment["cheque"]
            # la autofactura exige 8 dígitos exactos; la factura los completa Sifende
            condition_payment["numeroCheque"] = cheque["numeroCheque"].zfill(8)
            condition_payment["bancoCheque"] = cheque["bancoCheque"].strip()
        if currency != PYG and data.get("tipoCambio"):
            condition_payment["tipoCambio"] = _number(data["tipoCambio"])
        return {
            "tipoTransaccion": self._name("tipoTransaccion", data["tipoTransaccion"]),
            "vendedor": {
                "naturaleza": self._name(
                    "naturalezaVendedor", nature, _SELLER_NATURE[nature]
                ),
                "tipoDocumento": self._name("tipoDocumentoTransportista", doc_type),
                "numeroDocumento": auto["numeroDocumentoVendedor"],
                "nombre": auto["nombreVendedor"],
                "numeroCasa": auto["numeroCasaVendedor"],
                "domicilio": self._domicilio(
                    auto["direccionVendedor"], extra_auto.get("vendedor")
                ),
            },
            "lugarOperacion": self._domicilio(
                auto["direccionProvision"], extra_auto.get("provision")
            ),
            "constancia": {
                "tipo": self._name("tipoConstancia", auto["tipoConstancia"])
            },
            "condicionPago": condition_payment,
            "items": [
                {
                    "codigo": item["codigo"],
                    "descripcion": item["descripcion"],
                    "cantidad": _number(item["cantidad"]),
                    "unidadMedida": self._name(
                        "unidadMedida", _extra(item).get("unidadMedida") or 77
                    ),
                    "precioUnitario": _number(
                        round(
                            item["precioUnitario"]
                            * (
                                1
                                - (
                                    _extra(item).get("descuentoParticularPorcentaje")
                                    or 0
                                )
                                / 100
                            ),
                            8,
                        )
                    ),
                }
                for item in data.get("items") or []
            ],
        }

    def _domicilio(self, address, geography):
        if not geography:
            raise UserError(self.env._("Falta la ciudad de «%s».", address))
        return {
            "direccion": address,
            "departamento": str(geography["departamento"]),
            "codigoDistrito": geography["distrito"],
            "ciudad": str(geography["ciudad"]),
        }


_SELLER_NATURE = {1: "NO_CONTRIBUYENTE", 2: "EXTRANJERO"}
