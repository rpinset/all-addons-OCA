# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from unittest.mock import patch

from odoo import fields
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.service.model import get_public_method
from odoo.tests import tagged

from .common import CDC, FakeResponse, SifendeCommon

CANCEL_OK = FakeResponse(200, {"estadoEvento": "APROBADO"})
TAXPAYER = FakeResponse(
    200,
    {
        "ruc": "80009401",
        "ambiente": "DEV",
        "estadoConfiguracion": {"listoParaEmitir": True},
    },
)
INUTILIZATION = {
    "timbrado": "12345678",
    "establecimiento": "001",
    "punto": "001",
    "numeroDesde": "0000005",
    "numeroHasta": "0000005",
    "tipoDocumento": 1,
    "motivo": "Número saltado por error de sistema",
}


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestSecurity(SifendeCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other_company = cls.env["res.company"].create({"name": "Otra empresa"})
        cls.other_connector = cls.env["l10n_py.edi.connector"].create(
            {
                "name": "Sifende otra empresa",
                "provider_type": "sifende",
                "sifende_api_key": "sk_test_otra-empresa",
                "company_id": cls.other_company.id,
            }
        )

    def make_user(self, login, *groups, companies=None):
        companies = companies or self.company
        return self.env["res.users"].create(
            {
                "name": login,
                "login": login,
                "company_id": companies[0].id,
                "company_ids": [(6, 0, companies.ids)],
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.env.ref(group).id
                            for group in ("base.group_user", *groups)
                        ],
                    )
                ],
            }
        )

    def as_user(self, user, connector=None):
        return (connector or self.connector).with_user(user)

    def assertNoRemoteCall(self):
        self.assertFalse(self.fake.calls_to("POST", ".*"))
        self.assertFalse(self.fake.calls_to("GET", "^/contribuyente$"))

    # === Operaciones fiscales del conector ===

    def test_un_usuario_interno_sin_rol_contable_no_cancela(self):
        user = self.make_user("interno_sin_rol")
        with self.assertRaises(AccessError):
            self.as_user(user).cancel_document(CDC, "Motivo de prueba")
        self.assertNoRemoteCall()

    def test_un_usuario_interno_sin_rol_contable_no_opera_el_conector(self):
        user = self.make_user("interno_sin_rol_ops")
        connector = self.as_user(user)
        for call in (
            lambda: connector.send_document({}),
            lambda: connector.check_status(CDC),
            lambda: connector.inutilize_range(INUTILIZATION),
            lambda: connector.test_connection(),
        ):
            with self.assertRaises(AccessError):
                call()
        self.assertFalse(self.fake.calls)

    def test_un_facturador_de_otra_empresa_no_toca_el_conector_ajeno(self):
        user = self.make_user("facturador", "account.group_account_invoice")
        with self.assertRaises(AccessError):
            self.as_user(user, self.other_connector).cancel_document(CDC, "Motivo")
        self.assertNoRemoteCall()

    def test_un_gerente_de_otra_empresa_no_prueba_el_conector_ajeno(self):
        user = self.make_user("gerente", "account.group_account_manager")
        with self.assertRaises(AccessError):
            self.as_user(user, self.other_connector).test_connection()
        self.assertFalse(self.fake.calls)

    def test_el_acceso_es_a_la_empresa_activa_aunque_el_usuario_tenga_ambas(self):
        user = self.make_user(
            "multiempresa",
            "account.group_account_invoice",
            companies=self.company | self.other_company,
        )
        connector = self.other_connector.with_user(user).with_context(
            allowed_company_ids=self.company.ids
        )
        with self.assertRaises(AccessError):
            connector.cancel_document(CDC, "Motivo")
        self.assertNoRemoteCall()

    def test_un_facturador_cancela_en_su_empresa(self):
        user = self.make_user("facturador_ok", "account.group_account_invoice")
        self.fake.add("POST", "/cancelar$", CANCEL_OK)
        result = self.as_user(user).cancel_document(CDC, "Motivo de prueba")
        self.assertTrue(result["success"])
        call = self.fake.calls_to("POST", "/cancelar$")[0]
        self.assertEqual(call.json, {"motivo": "Motivo de prueba"})

    def test_el_acceso_sudo_no_eleva_al_usuario(self):
        user = self.make_user("interno_sudo")
        with self.assertRaises(AccessError):
            self.as_user(user).sudo().cancel_document(CDC, "Motivo de prueba")
        self.assertNoRemoteCall()

    def test_la_consulta_de_estado_admite_facturacion_y_solo_lectura(self):
        self.fake.add(
            "GET",
            rf"/documento-electronico/status/{CDC}$",
            self.status_response("APROBADO"),
        )
        for login, group in (
            ("auditor", "account.group_account_readonly"),
            ("facturador_estado", "account.group_account_invoice"),
        ):
            user = self.make_user(login, group)
            self.assertTrue(self.as_user(user).check_status(CDC)["success"])

    def test_inutilizar_y_probar_la_conexion_son_del_responsable_contable(self):
        biller = self.make_user("facturador_inut", "account.group_account_invoice")
        manager = self.make_user("gerente_inut", "account.group_account_manager")
        with self.assertRaises(AccessError):
            self.as_user(biller).inutilize_range(INUTILIZATION)
        with self.assertRaises(AccessError):
            self.as_user(biller).test_connection()
        self.fake.add("POST", "/inutilizar$", CANCEL_OK)
        self.fake.add("GET", r"^/contribuyente$", TAXPAYER)
        self.assertTrue(self.as_user(manager).inutilize_range(INUTILIZATION)["success"])
        self.assertEqual(
            self.as_user(manager).test_connection()["params"]["type"], "success"
        )

    def test_el_cron_y_el_superusuario_operan_sin_rol(self):
        self.fake.add("POST", "/cancelar$", CANCEL_OK)
        self.assertTrue(self.connector.cancel_document(CDC, "Motivo")["success"])
        self.assertTrue(self.connector.sudo().cancel_document(CDC, "Motivo")["success"])

    def test_las_operaciones_del_protocolo_no_son_invocables_por_rpc(self):
        connector = self.env["l10n_py.edi.connector"]
        for name in (
            "send_document",
            "check_status",
            "cancel_document",
            "inutilize_range",
            "preview_document",
            "preview_qr",
            "_sifende_fetch_xml",
            "_sifende_fetch_kude",
        ):
            with self.assertRaises(AccessError, msg=name):
                get_public_method(connector, name)
        get_public_method(connector, "test_connection")

    def test_los_conectores_de_otra_empresa_no_se_leen(self):
        user = self.make_user("lector", "account.group_account_manager")
        connectors = self.env["l10n_py.edi.connector"].with_user(user).search([])
        self.assertEqual(connectors, self.connector)
        with self.assertRaises(AccessError):
            self.other_connector.with_user(user).name  # noqa: B018

    # === Desde el documento ===

    def accepted_move(self):
        move = self.make_move("fe", invoice_date=fields.Date.today())
        move.write({"l10n_py_edi_status": "accepted", "l10n_py_cdc": CDC})
        return move

    def test_cancelar_un_documento_exige_poder_escribirlo(self):
        move = self.accepted_move()
        auditor = self.make_user("auditor_doc", "account.group_account_readonly")
        with self.assertRaises(AccessError):
            move.with_user(auditor).action_cancel_edi()
        self.assertNoRemoteCall()
        self.assertEqual(move.l10n_py_edi_status, "accepted")

    def test_cancelar_un_documento_ajeno_a_la_empresa_activa_falla(self):
        move = self.accepted_move()
        user = self.make_user(
            "facturador_ajeno",
            "account.group_account_invoice",
            companies=self.other_company,
        )
        with self.assertRaises(AccessError):
            move.with_user(user).action_cancel_edi()
        self.assertNoRemoteCall()

    def test_un_facturador_cancela_desde_el_documento(self):
        move = self.accepted_move()
        biller = self.make_user("facturador_doc", "account.group_account_invoice")
        self.fake.add("POST", "/cancelar$", CANCEL_OK)
        move.with_user(biller).action_cancel_edi()
        self.assertEqual(move.l10n_py_edi_status, "cancelled")

    def test_descargar_el_kude_exige_poder_escribir_el_documento(self):
        move = self.accepted_move()
        auditor = self.make_user("auditor_kude", "account.group_account_readonly")
        with self.assertRaises(AccessError):
            move.with_user(auditor).action_download_kude()
        self.assertFalse(self.fake.calls_to("GET", "/kude$"))

    def test_enviar_la_inutilizacion_exige_poder_escribirla(self):
        inutilization = self.env["l10n_py.number.inutilization"].create(
            {
                "authorization_id": self.auths["fe"].id,
                "number_from": 5,
                "number_to": 5,
                "motive": "Número saltado por error de sistema",
            }
        )
        biller = self.make_user("facturador_inut_doc", "account.group_account_invoice")
        with self.assertRaises(AccessError):
            inutilization.with_user(biller).action_send()
        self.assertNoRemoteCall()
        manager = self.make_user("gerente_inut_doc", "account.group_account_manager")
        self.fake.add("POST", "/inutilizar$", CANCEL_OK)
        inutilization.with_user(manager).action_send()
        self.assertEqual(inutilization.state, "accepted")

    # === Transportes entre empresas ===

    def transport_of_other_company(self):
        move = self.make_nre()
        biller = self.make_user(
            "facturador_transporte",
            "account.group_account_invoice",
            companies=self.other_company,
        )
        env = self.env(
            user=biller, context={"allowed_company_ids": biller.company_ids.ids}
        )
        return move.l10n_py_transport_id, env

    def test_un_facturador_no_modifica_transportes_de_otra_empresa(self):
        transport, env = self.transport_of_other_company()
        with self.assertRaises(AccessError):
            transport.with_env(env).write({"driver_name": "Modificado"})
        with self.assertRaises(AccessError):
            transport.with_env(env).unlink()
        self.assertEqual(transport.driver_name, "Carlos Benítez")

    def test_un_facturador_no_modifica_vehiculos_ni_entregas_de_otra_empresa(self):
        transport, env = self.transport_of_other_company()
        vehicle, delivery = transport.vehicle_ids, transport.delivery_ids
        with self.assertRaises(AccessError):
            vehicle.with_env(env).write({"plate_number": "ZZZ999"})
        with self.assertRaises(AccessError):
            vehicle.with_env(env).unlink()
        with self.assertRaises(AccessError):
            delivery.with_env(env).write({"address": "Otra calle"})
        with self.assertRaises(AccessError):
            delivery.with_env(env).unlink()
        with self.assertRaises(AccessError):
            env["l10n_py.transport.vehicle"].create(
                {
                    "transport_id": transport.id,
                    "vehicle_type": "CAMION",
                    "brand": "ISUZU",
                    "plate_number": "XYZ123",
                }
            )
        self.assertEqual(vehicle.plate_number, "ABC1234")
        self.assertTrue(delivery.exists())

    def test_los_transportes_de_otra_empresa_no_se_leen(self):
        transport, env = self.transport_of_other_company()
        found = env["l10n_py.transport"].search([])
        self.assertNotIn(transport, found)
        with self.assertRaises(AccessError):
            transport.with_env(env).driver_name  # noqa: B018

    def test_el_acceso_al_transporte_es_a_la_empresa_activa(self):
        transport, _env = self.transport_of_other_company()
        user = self.make_user(
            "multiempresa_transporte",
            "account.group_account_invoice",
            companies=self.company | self.other_company,
        )
        active = transport.with_user(user).with_context(
            allowed_company_ids=self.other_company.ids
        )
        with self.assertRaises(AccessError):
            active.write({"driver_name": "Modificado"})
        transport.with_user(user).with_context(
            allowed_company_ids=self.company.ids
        ).write({"driver_name": "Modificado"})

    def test_un_facturador_edita_el_transporte_de_su_empresa(self):
        move = self.make_nre()
        transport = move.l10n_py_transport_id
        biller = self.make_user("facturador_propio", "account.group_account_invoice")
        transport.with_user(biller).write({"driver_name": "Otro chofer"})
        transport.vehicle_ids.with_user(biller).write({"plate_number": "ZZZ999"})
        self.assertEqual(transport.vehicle_ids.plate_number, "ZZZ999")

    def test_un_transporte_sin_documento_solo_lo_edita_quien_lo_creo(self):
        creator = self.make_user("creador_transporte", "account.group_account_invoice")
        colleague = self.make_user("colega_transporte", "account.group_account_invoice")
        transport = (
            self.env["l10n_py.transport"]
            .with_user(creator)
            .create(self.nre_transport_vals())
        )
        transport.write({"driver_name": "Otro chofer"})
        with self.assertRaises(AccessError):
            transport.with_user(colleague).write({"driver_name": "Modificado"})
        with self.assertRaises(AccessError):
            transport.vehicle_ids.with_user(colleague).unlink()

    # === Destino de la API key ===

    def test_la_url_es_del_mismo_grupo_que_la_api_key(self):
        fields = self.env["l10n_py.edi.connector"]._fields
        self.assertEqual(
            fields["sifende_base_url"].groups, fields["sifende_api_key"].groups
        )

    def test_un_responsable_contable_no_cambia_el_destino_de_la_api_key(self):
        manager = self.make_user("contador", "account.group_account_manager")
        with self.assertRaises(AccessError):
            self.connector.with_user(manager).write(
                {"sifende_base_url": "https://colector.example"}
            )
        self.fake.add("GET", r"^/contribuyente$", TAXPAYER)
        self.as_user(manager).test_connection()
        self.assertTrue(
            self.fake.calls_to("GET", "^/contribuyente$")[0].url.startswith(
                "https://api.sifende.com.py/"
            )
        )

    def test_un_responsable_contable_crea_un_conector_con_la_url_por_defecto(self):
        manager = self.make_user(
            "contador_alta",
            "account.group_account_manager",
            companies=self.other_company,
        )
        self.other_connector.unlink()
        connector = (
            self.env["l10n_py.edi.connector"]
            .with_user(manager)
            .with_context(allowed_company_ids=self.other_company.ids)
            .create(
                {
                    "name": "Nuevo",
                    "provider_type": "sifende",
                    "company_id": self.other_company.id,
                }
            )
        )
        self.assertEqual(connector._sifende_base_url(), "https://api.sifende.com.py")

    def test_la_vista_oculta_la_url_a_quien_no_es_administrador(self):
        manager = self.make_user("contador_vista", "account.group_account_manager")
        arch = (
            self.env["l10n_py.edi.connector"]
            .with_user(manager)
            .get_view(view_type="form")["arch"]
        )
        self.assertNotIn("sifende_base_url", arch)

    def test_la_url_exige_https_salvo_en_localhost(self):
        for url in (
            "http://api.sifende.com.py",
            "ftp://x.example",
            "api.sifende.com.py",
        ):
            with self.assertRaises(ValidationError, msg=url):
                self.connector.sifende_base_url = url
        for url in (
            "https://api.sifende.com.py",
            "http://localhost:8080",
            "http://127.0.0.1:8080/",
        ):
            self.connector.sifende_base_url = url

    def test_la_api_key_no_viaja_a_una_url_sin_https(self):
        with patch.object(
            type(self.connector),
            "_sifende_base_url",
            return_value="http://colector.example",
        ):
            with self.assertRaisesRegex(UserError, "HTTPS"):
                self.connector.test_connection()
        self.assertFalse(self.fake.calls)
