# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.exceptions import UserError
from odoo.tests import Form, tagged

from .common import SifendeCommon


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestRemisionYAutofactura(SifendeCommon):
    def city(self, code):
        return self.env["l10n_py.sifende.city"].search([("code", "=", code)])

    def errors(self, move):
        with self.assertRaises(UserError) as caught:
            move.action_send_edi()
        return str(caught.exception.args[0])

    def resolve(self, state_xmlid, name):
        state = self.env.ref(f"l10n_py_base.{state_xmlid}")
        return self.env["l10n_py.sifende.city"]._sifende_resolve_name(state, name).code

    # === Catálogo de ciudades ===

    def test_el_catalogo_trae_las_ciudades_de_sifende(self):
        self.assertEqual(self.env["l10n_py.sifende.city"].search_count([]), 6770)
        lambare = self.city(6106)
        self.assertEqual(
            (lambare.name, lambare.district_code, lambare.department_code),
            ("LAMBARE", 169, 12),
        )

    def test_el_codigo_de_ciudad_de_oca_no_es_el_de_sifende(self):
        self.assertEqual(self.city_code, "1107")
        self.assertEqual(self.city(1107).name, "PASO CORA")

    def test_las_ciudades_de_oca_se_resuelven_por_departamento_y_nombre(self):
        self.assertEqual(self.resolve("state_py_central", "LAMBARÉ"), 6106)
        self.assertEqual(self.resolve("state_py_canindeyu", "Curuguaty"), 4881)

    def test_las_abreviaturas_de_sifende_se_reconocen(self):
        self.assertEqual(self.resolve("state_py_caaguazu", "CORONEL OVIEDO"), 2886)

    def test_una_ciudad_desconocida_no_se_adivina(self):
        self.assertEqual(self.resolve("state_py_central", "Ciudad Inventada"), 0)
        self.assertEqual(self.resolve("state_py_central", "Curuguaty"), 0)

    def test_todos_los_departamentos_de_oca_tienen_su_codigo_de_sifende(self):
        cities = self.env["l10n_py.sifende.city"]
        states = self.env["res.country.state"].search(
            [("country_id", "=", self.country_py.id), ("l10n_py_code", "!=", False)]
        )
        for state in states:
            code = cities._sifende_department_code(state)
            self.assertTrue(code, state.name)
            self.assertTrue(cities.search([("department_code", "=", code)]), state.name)
        presidente_hayes = self.env.ref("l10n_py_base.state_py_presidente_hayes")
        self.assertEqual(cities._sifende_department_code(presidente_hayes), 15)

    # === Transporte creado desde el documento ===

    def test_el_transporte_creado_sin_documento_se_enlaza_al_guardar(self):
        move = self.make_move("nr", l10n_py_nre_motive="2")
        transport = self.env["l10n_py.transport"].create({"transport_mode": "1"})
        self.assertFalse(transport.move_id)
        move.l10n_py_transport_id = transport
        self.assertEqual(transport.move_id, move)

    def test_el_transporte_creado_con_el_documento_se_enlaza(self):
        transport = self.env["l10n_py.transport"].create({"transport_mode": "1"})
        move = self.make_move(
            "nr", l10n_py_nre_motive="2", l10n_py_transport_id=transport.id
        )
        self.assertEqual(transport.move_id, move)

    def test_un_usuario_de_facturacion_carga_el_transporte(self):
        user = self.env["res.users"].create(
            {
                "name": "Facturador",
                "login": "facturador_transporte",
                "company_id": self.company.id,
                "company_ids": [(6, 0, self.company.ids)],
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_user").id,
                            self.env.ref("account.group_account_invoice").id,
                        ],
                    )
                ],
            }
        )
        transport = (
            self.env["l10n_py.transport"]
            .with_user(user)
            .create(self.nre_transport_vals())
        )
        self.assertEqual(len(transport.vehicle_ids), 1)
        self.assertEqual(transport.display_name, "Carlos Benítez")

    def test_elegir_la_ciudad_fija_los_codigos_de_sifende(self):
        transport = self.env["l10n_py.transport"].create(self.nre_transport_vals())
        self.assertEqual(
            (
                transport.departure_department,
                transport.departure_district,
                transport.departure_city,
            ),
            (12, 169, 6106),
        )
        delivery = transport.delivery_ids
        self.assertEqual(
            (delivery.department, delivery.district, delivery.city), (12, 169, 6106)
        )
        self.assertEqual(delivery.sifende_city_id, self.city_sifende)

    def test_el_transporte_se_abre_y_se_guarda_en_el_formulario(self):
        with Form(self.env["l10n_py.transport"]) as form:
            form.transport_type = "2"
            form.sifende_departure_city_id = self.city_sifende
            form.sifende_transporter_address = "Calle 1"
        self.assertEqual(form.record.departure_city, 6106)

    # === Nota de remisión ===

    def test_una_nota_con_transportista_contribuyente_y_agente(self):
        dv = self.env["res.company"]._calculate_dv("80009401")
        move = self.make_nre(
            transporter_nature="1",
            transporter_name="Transportes del Este S.A.",
            transporter_ruc="80009401",
            transporter_dv=dv,
            freight_responsibility="4",
            sifende_agent_name="Agente Fluvial S.A.",
            sifende_agent_ruc="80009401",
            sifende_agent_dv=dv,
            sifende_agent_address="Puerto de Asunción",
        )
        carrier = self.sent_payload(move)["transporte"]["transportista"]
        self.assertEqual(carrier["naturaleza"], "CONTRIBUYENTE")
        self.assertEqual(
            (carrier["ruc"], carrier["digitoVerificador"]), ("80009401", dv)
        )
        self.assertNotIn("tipoDocumento", carrier)
        self.assertEqual(carrier["nombreAgente"], "Agente Fluvial S.A.")
        self.assertEqual(carrier["digitoVerificadorAgente"], dv)

    def test_una_importacion_lleva_el_despacho(self):
        move = self.make_nre(sifende_import_dispatch="1234567890123456")
        move.l10n_py_nre_motive = "4"
        transport = self.sent_payload(move)["transporte"]
        self.assertEqual(transport["numeroDespachoImportacion"], "1234567890123456")

    def test_una_nota_sin_transportista_dice_que_falta(self):
        move = self.make_nre(
            transporter_name=False,
            transporter_nature=False,
            sifende_transporter_document_type=False,
            sifende_transporter_document_number=False,
            sifende_transporter_address=False,
            driver_doc_number=False,
            driver_name=False,
            sifende_driver_address=False,
        )
        message = self.errors(move)
        self.assertIn("Nota de Remisión: indique el transportista", message)
        self.assertIn("domicilio fiscal del transportista", message)
        self.assertIn("documento del chofer", message)
        self.assertIn("dirección del chofer", message)
        self.assertFalse(self.fake.calls_to("POST", r"^/documento-electronico$"))

    def test_una_nota_sin_direccion_del_transportista_ni_del_chofer(self):
        move = self.make_nre(
            sifende_transporter_address=False, sifende_driver_address=False
        )
        message = self.errors(move)
        self.assertIn("indique el domicilio fiscal del transportista", message)
        self.assertIn("indique la dirección del chofer", message)

    def test_una_nota_sin_el_resto_de_los_datos_del_traslado(self):
        move = self.make_nre(
            transport_type=False,
            freight_responsibility=False,
            transport_start_date=False,
            transport_end_date=False,
            departure_address=False,
            sifende_departure_city_id=False,
            delivery_ids=[],
            vehicle_ids=[],
        )
        message = self.errors(move)
        for expected in (
            "responsable del flete",
            "propio o de un tercero",
            "fechas de inicio y fin",
            "dirección de salida",
            "Salida): indique la ciudad",
            "al menos un punto de entrega",
            "de 1 a 4 vehículos",
        ):
            self.assertIn(expected, message)

    def test_una_nota_con_un_vehiculo_mal_cargado(self):
        move = self.make_nre()
        move.l10n_py_transport_id.vehicle_ids.write({"plate_number": "AB1"})
        self.assertIn("matrícula del vehículo 1", self.errors(move))

    def air_vehicles(self, flight="LA1234"):
        return [
            (
                0,
                0,
                {
                    "vehicle_type": "AVION",
                    "brand": "BOEING",
                    "plate_number": "ABC1234",
                    "sifende_flight_number": flight,
                },
            )
        ]

    def test_una_nota_aerea_lleva_el_numero_de_vuelo(self):
        move = self.make_nre(transport_mode="3", vehicle_ids=self.air_vehicles())
        vehicle = self.sent_payload(move)["transporte"]["vehiculos"][0]
        self.assertEqual(vehicle["numeroVuelo"], "LA1234")

    def test_una_nota_terrestre_no_lleva_numero_de_vuelo(self):
        move = self.make_nre(vehicle_ids=self.air_vehicles())
        vehicle = self.sent_payload(move)["transporte"]["vehiculos"][0]
        self.assertNotIn("numeroVuelo", vehicle)

    def test_una_nota_aerea_sin_numero_de_vuelo_se_avisa(self):
        move = self.make_nre(transport_mode="3", vehicle_ids=self.air_vehicles(False))
        self.assertIn("número de vuelo del vehículo 1", self.errors(move))
        self.assertFalse(self.fake.calls_to("POST", r"^/documento-electronico$"))

    def test_una_nota_aerea_con_un_numero_de_vuelo_de_largo_incorrecto(self):
        move = self.make_nre(transport_mode="3", vehicle_ids=self.air_vehicles("LA12"))
        self.assertIn("número de vuelo del vehículo 1", self.errors(move))

    def test_una_nota_con_agente_intermediario_exige_sus_datos(self):
        move = self.make_nre(freight_responsibility="4")
        message = self.errors(move)
        self.assertIn("nombre del agente", message)
        self.assertIn("dirección del agente", message)
        self.assertIn("RUC y el DV del agente", message)

    def test_un_dv_que_no_corresponde_al_ruc_se_avisa(self):
        move = self.make_nre(
            transporter_nature="1",
            transporter_name="Transportes del Este S.A.",
            transporter_ruc="1231231",
            transporter_dv="1",
        )
        self.assertIn("el DV no corresponde al RUC", self.errors(move))

    def test_una_importacion_sin_despacho_se_avisa(self):
        move = self.make_nre()
        move.l10n_py_nre_motive = "4"
        self.assertIn("exige el despacho de importación", self.errors(move))

    def test_una_nota_con_una_ciudad_de_oca_en_el_departamento_equivocado(self):
        move = self.make_nre()
        move.l10n_py_transport_id.departure_city = 1107
        self.assertIn(
            "la ciudad PASO CORA - HORQUETA (CONCEPCION) no pertenece al "
            "departamento 12",
            self.errors(move),
        )

    def test_una_nota_a_un_cliente_sin_ubicacion_pide_la_ciudad_sifende(self):
        move = self.make_nre()
        self.partner.write(
            {"state_id": False, "city_id": False, "city": "Ciudad Inventada"}
        )
        message = self.errors(move)
        self.assertIn("necesita departamento y ciudad", message)
        self.assertIn("Ciudad SIFEN", message)
        self.assertFalse(self.fake.calls_to("POST", r"^/documento-electronico$"))

    def test_una_nota_a_un_cliente_con_ciudad_sifende_no_necesita_departamento(self):
        move = self.make_nre()
        self.partner.write(
            {
                "state_id": False,
                "city_id": False,
                "city": False,
                "l10n_py_sifende_city_id": self.city_sifende.id,
            }
        )
        receptor = self.sent_payload(move)["receptor"]
        self.assertEqual(receptor["ciudad"], "6106")

    def test_una_nota_a_un_cliente_innominado_se_avisa(self):
        move = self.make_nre()
        self.partner.write({"l10n_py_taxpayer_type": "2", "l10n_py_doc_type": "4"})
        self.assertIn("el receptor no puede ser innominado", self.errors(move))

    # === Autofactura ===

    def afe_vals(self, **extra):
        return {
            "l10n_py_afe_constancia_type": "1",
            "l10n_py_afe_constancia_number": "CONST-1",
            "l10n_py_afe_constancia_control": "CTRL-1",
            "l10n_py_afe_vendor_doc_type": "1",
            "l10n_py_afe_vendor_doc_number": "1234567",
            "l10n_py_afe_vendor_name": "María González",
            "l10n_py_afe_vendor_address": "Av. España",
            "l10n_py_afe_provision_address": "Ruta 1 km 20",
            **extra,
        }

    def make_afe(self, **vals):
        vals.setdefault("lines", [self.line(tax=self.tax_exempt)])
        return self.make_move("af", **self.afe_vals(**vals))

    def constancias(self, move):
        return move.l10n_py_associated_document_ids.filtered(
            lambda doc: doc.association_type == "3"
        )

    def test_la_constancia_de_la_autofactura_se_asocia_sola_al_confirmar(self):
        move = self.make_afe()
        constancia = self.constancias(move)
        self.assertEqual(move.l10n_py_associated_document_ids, constancia)
        self.assertEqual(
            (constancia.constancia_type, constancia.constancia_number),
            ("1", "CONST-1"),
        )

    def test_la_constancia_asociada_sigue_los_cambios_de_la_seccion(self):
        move = self.make_afe()
        constancia = self.constancias(move)
        move.l10n_py_afe_constancia_number = "CONST-2"
        move._l10n_py_sifende_link_origin_document()
        self.assertEqual(self.constancias(move), constancia)
        self.assertEqual(constancia.constancia_number, "CONST-2")

    def test_una_autofactura_sin_constancia_dice_que_documento_falta(self):
        move = self.make_afe(l10n_py_afe_constancia_number=False)
        self.assertFalse(move.l10n_py_associated_document_ids)
        message = self.errors(move)
        self.assertIn("falta la constancia electrónica", message)
        self.assertIn("sección Autofactura", message)
        self.assertNotIn("exactamente 1", message)

    def test_una_autofactura_con_iva_dice_que_lineas_deben_ser_exentas(self):
        move = self.make_afe(
            lines=[
                self.line(name="Resma", tax=self.tax_10),
                self.line(name="Cuaderno", tax=self.tax_exempt),
                self.line(name="Lápiz", tax=self.tax_5),
            ]
        )
        message = self.errors(move)
        self.assertIn(
            'Autofactura: los ítems deben ser exentos de IVA; la línea "Resma" '
            "tiene IVA 10%",
            message,
        )
        self.assertIn('la línea "Lápiz" tiene IVA 5%', message)
        self.assertNotIn("Cuaderno", message)
        self.assertFalse(self.fake.calls_to("POST", ".*"))

    def test_una_autofactura_con_microproductor_se_frena_antes_de_enviar(self):
        move = self.make_afe(
            l10n_py_afe_constancia_type="2",
            l10n_py_sifende_afe_vendor_city_id=self.city_sifende.id,
            l10n_py_sifende_afe_provision_city_id=self.city_sifende.id,
        )
        self.assertIn(
            "Autofactura: sólo se admite la constancia de no contribuyente, no "
            "«Microproductor»",
            self.errors(move),
        )
        self.assertFalse(self.fake.calls_to("POST", ".*"))

    def test_una_autofactura_exenta_con_constancia_de_no_contribuyente_no_se_frena(
        self,
    ):
        move = self.make_afe(
            l10n_py_sifende_afe_vendor_city_id=self.city_sifende.id,
            l10n_py_sifende_afe_provision_city_id=self.city_sifende.id,
        )
        self.assertEqual(move._l10n_py_sifende_autofactura_errors(), [])

    def test_una_autofactura_en_una_ciudad_cuyo_codigo_de_oca_difiere(self):
        self.assertNotEqual(self.city_code, str(self.city_sifende.code))
        move = self.make_afe(
            l10n_py_sifende_afe_vendor_city_id=self.city_sifende.id,
            l10n_py_sifende_afe_provision_city_id=self.city_sifende.id,
        )
        payload = self.sent_payload(move)
        for place in (payload["vendedor"]["domicilio"], payload["lugarOperacion"]):
            self.assertEqual(
                {k: place[k] for k in ("departamento", "codigoDistrito", "ciudad")},
                {"departamento": "12", "codigoDistrito": 169, "ciudad": "6106"},
            )

    def test_una_autofactura_con_el_codigo_de_ciudad_de_oca_se_frena_antes_de_enviar(
        self,
    ):
        move = self.make_afe(
            l10n_py_afe_vendor_department=12,
            l10n_py_afe_vendor_city=int(self.city_code),
            l10n_py_sifende_afe_provision_city_id=self.city_sifende.id,
        )
        self.assertIn(
            "Autofactura (vendedor): la ciudad PASO CORA - HORQUETA (CONCEPCION) "
            "no pertenece al departamento 12",
            self.errors(move),
        )
        self.assertFalse(self.fake.calls_to("POST", r"^/documento-electronico$"))

    def test_una_autofactura_sin_ciudades_dice_cuales_faltan(self):
        message = self.errors(self.make_afe())
        self.assertIn("Autofactura (vendedor): indique la ciudad", message)
        self.assertIn("Autofactura (lugar de provisión): indique la ciudad", message)

    def test_una_autofactura_exige_cedula_paraguaya_de_5_a_12_digitos(self):
        move = self.make_afe(
            l10n_py_afe_vendor_doc_type="2",
            l10n_py_afe_vendor_doc_number="12-34",
            l10n_py_sifende_afe_vendor_city_id=self.city_sifende.id,
            l10n_py_sifende_afe_provision_city_id=self.city_sifende.id,
        )
        message = self.errors(move)
        self.assertIn("cédula paraguaya", message)
        self.assertIn("de 5 a 12 dígitos", message)
