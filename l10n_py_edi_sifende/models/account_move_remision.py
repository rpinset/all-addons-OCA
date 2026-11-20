# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import re
from datetime import date

from odoo import api, fields, models

DOC_SELF_INVOICE = "4"
DOC_DELIVERY_NOTE = "7"
MOTIVE_IMPORT = "4"
FREIGHT_INTERMEDIARY = "4"
NON_CONTRIBUTOR = "2"
KM_MAX = 99999
MANIFEST_MAX = 15
VEHICLES_MAX = 4
SIFEN_START = date(2018, 11, 22)
IMPORT_DISPATCH_LENGTH = 16
FLIGHT_NUMBER_LENGTH = 6
AIR_TRANSPORT = "3"
DIGITS_RE = re.compile(r"\d+")


def _digits(value, minimum, maximum):
    return bool(DIGITS_RE.fullmatch(value or "")) and minimum <= len(value) <= maximum


class AccountMove(models.Model):
    _inherit = "account.move"  # pylint: disable=consider-merging-classes-inherited

    l10n_py_sifende_afe_vendor_city_id = fields.Many2one(
        "l10n_py.sifende.city",
        string="Ciudad del vendedor",
        compute="_compute_l10n_py_sifende_afe_vendor_city_id",
        inverse="_inverse_l10n_py_sifende_afe_vendor_city_id",
    )
    l10n_py_sifende_afe_provision_city_id = fields.Many2one(
        "l10n_py.sifende.city",
        string="Ciudad de provisión",
        compute="_compute_l10n_py_sifende_afe_provision_city_id",
        inverse="_inverse_l10n_py_sifende_afe_provision_city_id",
    )

    @api.depends("l10n_py_afe_vendor_city")
    def _compute_l10n_py_sifende_afe_vendor_city_id(self):
        cities = self.env["l10n_py.sifende.city"]
        for move in self:
            move.l10n_py_sifende_afe_vendor_city_id = cities._sifende_by_code(
                move.l10n_py_afe_vendor_city
            )

    def _inverse_l10n_py_sifende_afe_vendor_city_id(self):
        for move in self:
            (
                move.l10n_py_afe_vendor_department,
                move.l10n_py_afe_vendor_district,
                move.l10n_py_afe_vendor_city,
            ) = move.l10n_py_sifende_afe_vendor_city_id._sifende_ints()

    @api.depends("l10n_py_afe_provision_city")
    def _compute_l10n_py_sifende_afe_provision_city_id(self):
        cities = self.env["l10n_py.sifende.city"]
        for move in self:
            move.l10n_py_sifende_afe_provision_city_id = cities._sifende_by_code(
                move.l10n_py_afe_provision_city
            )

    def _inverse_l10n_py_sifende_afe_provision_city_id(self):
        for move in self:
            (
                move.l10n_py_afe_provision_department,
                move.l10n_py_afe_provision_district,
                move.l10n_py_afe_provision_city,
            ) = move.l10n_py_sifende_afe_provision_city_id._sifende_ints()

    # === Enlace del transporte creado desde el documento ===

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        moves._l10n_py_sifende_link_transport()
        return moves

    def write(self, vals):
        result = super().write(vals)
        if "l10n_py_transport_id" in vals:
            self._l10n_py_sifende_link_transport()
        return result

    def _l10n_py_sifende_link_transport(self):
        for move in self.filtered("l10n_py_transport_id"):
            if not move.l10n_py_transport_id.move_id:
                move.l10n_py_transport_id.move_id = move

    # === Datos adicionales para Sifende ===

    def _l10n_py_sifende_extra_data(self):
        extra = super()._l10n_py_sifende_extra_data()
        code = self.l10n_latam_document_type_id.code
        extra["cliente"]["geografia"] = self._l10n_py_sifende_partner_geography()
        if self.l10n_py_transport_id and (
            code == DOC_DELIVERY_NOTE or self._l10n_py_is_export()
        ):
            extra["transporte"] = self._l10n_py_sifende_transport_data()
        if code == DOC_SELF_INVOICE:
            extra["autofactura"] = {
                "vendedor": self._l10n_py_sifende_codes(self.l10n_py_afe_vendor_city),
                "provision": self._l10n_py_sifende_codes(
                    self.l10n_py_afe_provision_city
                ),
            }
        return extra

    def _l10n_py_sifende_codes(self, city_code):
        city = self.env["l10n_py.sifende.city"]._sifende_by_code(city_code)
        return city._sifende_codes() if city else None

    def _l10n_py_sifende_partner_geography(self):
        partner = self.partner_id
        city = partner.l10n_py_sifende_city_id
        if not city:
            city = self.env["l10n_py.sifende.city"]._sifende_resolve_name(
                partner.state_id, self._l10n_py_sifende_city_name()
            )
        return city._sifende_codes() if city else None

    def _prepare_transport_data(self):
        data = super()._prepare_transport_data()
        if self._l10n_py_sifende_connector():
            transport = self.l10n_py_transport_id
            for entry, delivery in zip(
                data.get("entregas", []), transport.delivery_ids, strict=True
            ):
                entry["sifende"] = self._l10n_py_sifende_codes(delivery.city)
            for entry, vehicle in zip(
                data.get("vehiculos", []), transport.vehicle_ids, strict=True
            ):
                entry["sifende"] = {
                    "numeroVuelo": vehicle.sifende_flight_number or None
                }
        return data

    def _l10n_py_sifende_transport_data(self):
        transport = self.l10n_py_transport_id
        carrier = {
            "tipoDocumento": int(transport.sifende_transporter_document_type or 0),
            "numeroDocumento": transport.sifende_transporter_document_number,
            "domicilioFiscal": transport.sifende_transporter_address,
            "direccionConductor": transport.sifende_driver_address,
            "nombreAgente": transport.sifende_agent_name,
            "rucAgente": transport.sifende_agent_ruc,
            "digitoVerificadorAgente": transport.sifende_agent_dv,
            "direccionAgente": transport.sifende_agent_address,
        }
        return {
            "numeroDespachoImportacion": transport.sifende_import_dispatch or None,
            "salida": self._l10n_py_sifende_codes(transport.departure_city),
            "transportista": {key: value for key, value in carrier.items() if value},
        }

    # === Constancia de la autofactura como documento asociado ===

    def _l10n_py_sifende_link_origin_document(self):
        result = super()._l10n_py_sifende_link_origin_document()
        self._l10n_py_sifende_link_constancia()
        return result

    def _l10n_py_sifende_link_constancia(self):
        for move in self:
            if (
                move.l10n_latam_document_type_id.code != DOC_SELF_INVOICE
                or not (
                    move.l10n_py_afe_constancia_type
                    and move.l10n_py_afe_constancia_number
                )
                or move._l10n_py_sifende_frozen()
            ):
                continue
            values = {
                "constancia_type": move.l10n_py_afe_constancia_type,
                "constancia_number": move.l10n_py_afe_constancia_number,
            }
            constancia = move.l10n_py_associated_document_ids.filtered(
                lambda doc: doc.association_type == "3"
            )[:1]
            if not constancia:
                self.env["l10n_py.associated.document"].sudo().create(
                    {"move_id": move.id, "association_type": "3", **values}
                )
            elif any(constancia[key] != value for key, value in values.items()):
                constancia.sudo().write(values)

    def _validate_afe_data(self, docs):
        errors = super()._validate_afe_data(docs)
        if not docs and errors and self._l10n_py_sifende_connector():
            errors[0] = self.env._(
                "Autofactura: falta la constancia electrónica como documento "
                "asociado. Indique su tipo y número en la sección Autofactura, o "
                "agréguela en Documentos Asociados."
            )
        return errors

    # === Validación previa al envío ===

    def _validate_edi_document_type(self):
        errors = super()._validate_edi_document_type()
        if not self._l10n_py_sifende_connector():
            return errors
        code = self.l10n_latam_document_type_id.code
        if code == DOC_DELIVERY_NOTE:
            errors.extend(self._l10n_py_sifende_remision_errors())
        elif code == DOC_SELF_INVOICE:
            errors.extend(self._l10n_py_sifende_autofactura_errors())
        elif self.l10n_py_transport_id and self._l10n_py_is_export():
            errors.extend(
                self._l10n_py_sifende_transport_errors(
                    self.env._("Factura de exportación"), strict=False
                )
            )
        return errors

    def _l10n_py_sifende_remision_errors(self):
        label = self.env._("Nota de Remisión")
        errors = []
        if self.l10n_py_sifende_km_recorrido > KM_MAX:
            errors.append(
                f"{label}: "
                + self.env._(
                    "los kilómetros del recorrido no pueden pasar de %(max)s.",
                    max=KM_MAX,
                )
            )
        partner = self.partner_id
        if partner.l10n_py_taxpayer_type == "2" and partner.l10n_py_doc_type == "4":
            errors.append(
                f"{label}: " + self.env._("el receptor no puede ser innominado.")
            )
        if partner.country_id.code == "PY" and not (
            self._l10n_py_sifende_partner_geography()
            or (partner.state_id and (partner.city_id or partner.city))
        ):
            errors.append(
                f"{label}: "
                + self.env._(
                    "el cliente necesita departamento y ciudad (o la «Ciudad SIFEN»)."
                )
            )
        if self.l10n_py_transport_id:
            errors.extend(self._l10n_py_sifende_transport_errors(label, strict=True))
        return errors

    def _l10n_py_sifende_geography_error(self, label, department, city):
        if not city:
            return f"{label}: " + self.env._("indique la ciudad.")
        problem = self.env["l10n_py.sifende.city"]._sifende_check_codes(
            department, city
        )
        return f"{label}: {problem}." if problem else None

    def _l10n_py_sifende_transport_errors(self, label, strict):
        transport = self.l10n_py_transport_id
        errors = self._l10n_py_sifende_trip_errors(label, transport, strict)
        errors.extend(self._l10n_py_sifende_place_errors(label, transport, strict))
        errors.extend(self._l10n_py_sifende_vehicle_errors(label, transport, strict))
        if strict or transport.transporter_name:
            errors.extend(self._l10n_py_sifende_carrier_errors(label, transport))
        errors.extend(self._l10n_py_sifende_agent_errors(label, transport))
        return errors

    def _l10n_py_sifende_trip_errors(self, label, transport, strict):
        errors = []

        def add(text):
            errors.append(f"{label}: {text}")

        if not transport.freight_responsibility:
            add(self.env._("indique el responsable del flete."))
        if strict and not transport.transport_type:
            add(self.env._("indique si el transporte es propio o de un tercero."))
        start, end = transport.transport_start_date, transport.transport_end_date
        if strict and not (start and end):
            add(self.env._("indique las fechas de inicio y fin del traslado."))
        elif bool(start) != bool(end):
            add(self.env._("indique juntas las fechas de inicio y fin del traslado."))
        elif start and end and end < start:
            add(self.env._("el fin del traslado no puede ser anterior al inicio."))
        if start and start <= SIFEN_START:
            add(self.env._("el inicio del traslado debe ser posterior al 22/11/2018."))
        if len(transport.manifest_number or "") > MANIFEST_MAX:
            add(self.env._("el manifiesto admite hasta 15 caracteres."))
        dispatch = transport.sifende_import_dispatch
        if self.l10n_py_nre_motive == MOTIVE_IMPORT and not dispatch:
            add(self.env._("la importación exige el despacho de importación."))
        if dispatch and len(dispatch) != IMPORT_DISPATCH_LENGTH:
            add(self.env._("el despacho de importación debe tener 16 caracteres."))
        return errors

    def _l10n_py_sifende_place_errors(self, label, transport, strict):
        errors = []

        def add(text):
            errors.append(f"{label}: {text}")

        def add_geography(place, department, city):
            problem = self._l10n_py_sifende_geography_error(
                f"{label} ({place})", department, city
            )
            if problem:
                errors.append(problem)

        if strict or transport.departure_address:
            if not transport.departure_address:
                add(self.env._("indique la dirección de salida."))
            add_geography(
                self.env._("Salida"),
                transport.departure_department,
                transport.departure_city,
            )
        deliveries = transport.delivery_ids
        if strict and not deliveries:
            add(self.env._("indique al menos un punto de entrega."))
        for number, delivery in enumerate(deliveries, 1):
            if not delivery.address:
                add(
                    self.env._(
                        "indique la dirección de la entrega %(number)s.", number=number
                    )
                )
            add_geography(
                self.env._("Entrega %(number)s", number=number),
                delivery.department,
                delivery.city,
            )
        return errors

    def _l10n_py_sifende_vehicle_errors(self, label, transport, strict):
        errors = []

        def add(text):
            errors.append(f"{label}: {text}")

        vehicles = transport.vehicle_ids
        if strict and not 1 <= len(vehicles) <= VEHICLES_MAX:
            add(self.env._("indique de 1 a 4 vehículos."))
        for number, vehicle in enumerate(vehicles, 1):
            if (
                transport.transport_mode == AIR_TRANSPORT
                and len(vehicle.sifende_flight_number or "") != FLIGHT_NUMBER_LENGTH
            ):
                add(
                    self.env._(
                        "el número de vuelo del vehículo %(number)s debe tener "
                        "6 caracteres.",
                        number=number,
                    )
                )
            if not 4 <= len(vehicle.vehicle_type or "") <= 10:
                add(
                    self.env._(
                        "el tipo del vehículo %(number)s admite de 4 a 10 caracteres.",
                        number=number,
                    )
                )
            if not 1 <= len(vehicle.brand or "") <= 10:
                add(
                    self.env._(
                        "la marca del vehículo %(number)s admite hasta 10 caracteres.",
                        number=number,
                    )
                )
            if not 6 <= len((vehicle.plate_number or "").strip()) <= 7:
                add(
                    self.env._(
                        "la matrícula del vehículo %(number)s admite de 6 a 7 "
                        "caracteres.",
                        number=number,
                    )
                )
        return errors

    def _l10n_py_sifende_carrier_errors(self, label, transport):
        errors = []

        def add(text):
            errors.append(f"{label}: {text}")

        if not 4 <= len(transport.transporter_name or "") <= 60:
            add(
                self.env._(
                    "indique el transportista: nombre de 4 a 60 caracteres, "
                    "documento y domicilio fiscal."
                )
            )
        if transport.transporter_nature != NON_CONTRIBUTOR:
            errors.extend(
                self._l10n_py_sifende_ruc_errors(
                    label,
                    self.env._("el RUC y el DV del transportista"),
                    transport.transporter_ruc,
                    transport.transporter_dv,
                )
            )
        else:
            if not transport.sifende_transporter_document_type:
                add(self.env._("indique el tipo de documento del transportista."))
            if not transport.sifende_transporter_document_number:
                add(self.env._("indique el número de documento del transportista."))
        if not transport.sifende_transporter_address:
            add(self.env._("indique el domicilio fiscal del transportista."))
        if not transport.driver_doc_number:
            add(self.env._("indique el documento del chofer."))
        if not 4 <= len(transport.driver_name or "") <= 60:
            add(self.env._("el nombre del chofer admite de 4 a 60 caracteres."))
        if not transport.sifende_driver_address:
            add(self.env._("indique la dirección del chofer."))
        return errors

    def _l10n_py_sifende_agent_errors(self, label, transport):
        fields_filled = (
            transport.sifende_agent_name,
            transport.sifende_agent_ruc,
            transport.sifende_agent_dv,
            transport.sifende_agent_address,
        )
        if not (
            any(fields_filled)
            or transport.freight_responsibility == FREIGHT_INTERMEDIARY
        ):
            return []
        errors = []
        if not 4 <= len(transport.sifende_agent_name or "") <= 60:
            errors.append(
                f"{label}: "
                + self.env._("el nombre del agente admite de 4 a 60 caracteres.")
            )
        if not transport.sifende_agent_address:
            errors.append(f"{label}: " + self.env._("indique la dirección del agente."))
        errors.extend(
            self._l10n_py_sifende_ruc_errors(
                label,
                self.env._("el RUC y el DV del agente"),
                transport.sifende_agent_ruc,
                transport.sifende_agent_dv,
            )
        )
        return errors

    def _l10n_py_sifende_ruc_errors(self, label, subject, ruc, dv):
        if not (_digits(ruc, 3, 8) and _digits(dv, 1, 1)):
            return [
                f"{label}: "
                + self.env._(
                    "%(subject)s son obligatorios: RUC de 3 a 8 dígitos y DV de 1.",
                    subject=subject,
                )
            ]
        if dv != self.env["res.company"]._calculate_dv(ruc):
            return [
                f"{label}: "
                + self.env._(
                    "%(subject)s no coinciden: el DV no corresponde al RUC.",
                    subject=subject,
                )
            ]
        return []

    def _l10n_py_sifende_autofactura_errors(self):
        label = self.env._("Autofactura")
        errors = []

        def add(text):
            errors.append(f"{label}: {text}")

        constancia_type = self.l10n_py_afe_constancia_type
        if constancia_type and constancia_type != "1":
            add(
                self.env._(
                    "sólo se admite la constancia de no contribuyente, no «%(type)s».",
                    type=dict(
                        self._fields[
                            "l10n_py_afe_constancia_type"
                        ]._description_selection(self.env)
                    ).get(constancia_type),
                )
            )
        for line in self.invoice_line_ids.filtered(
            lambda line: line.display_type == "product"
        ):
            rates = sorted({tax.amount for tax in line.tax_ids if tax.amount})
            if rates:
                add(
                    self.env._(
                        'los ítems deben ser exentos de IVA; la línea "%(line)s" '
                        "tiene IVA %(rates)s.",
                        line=line.name or line.product_id.display_name,
                        rates=", ".join(f"{rate:g}%" for rate in rates),
                    )
                )
        if self.l10n_py_afe_vendor_doc_type != "1":
            add(self.env._("el vendedor debe identificarse con cédula paraguaya."))
        if not _digits(self.l10n_py_afe_vendor_doc_number, 5, 12):
            add(
                self.env._(
                    "la cédula del vendedor debe tener de 5 a 12 dígitos, "
                    "sin puntos ni guiones."
                )
            )
        if not 4 <= len(self.l10n_py_afe_vendor_name or "") <= 60:
            add(self.env._("el nombre del vendedor admite de 4 a 60 caracteres."))
        if not self.l10n_py_afe_provision_address:
            add(self.env._("indique la dirección del lugar de provisión."))
        for place, department, city in (
            (
                self.env._("vendedor"),
                self.l10n_py_afe_vendor_department,
                self.l10n_py_afe_vendor_city,
            ),
            (
                self.env._("lugar de provisión"),
                self.l10n_py_afe_provision_department,
                self.l10n_py_afe_provision_city,
            ),
        ):
            problem = self._l10n_py_sifende_geography_error(
                f"{label} ({place})", department, city
            )
            if problem:
                errors.append(problem)
        return errors
