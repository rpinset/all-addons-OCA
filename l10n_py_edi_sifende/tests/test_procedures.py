# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import tagged

from .common import CDC, FakeResponse, SifendeCommon, problem

OCA_INUTILIZATION_LOGGER = (
    "odoo.addons.l10n_py_edi_base.models.l10n_py_number_inutilization"
)

EVENT_OK = FakeResponse(200, {"estadoEvento": "APROBADO"})


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestProcedures(SifendeCommon):
    def make_user(self, login, *groups):
        return self.env["res.users"].create(
            {
                "name": login,
                "login": login,
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

    def accepted_move(self):
        move = self.make_move("fe", invoice_date=fields.Date.today())
        move.write({"l10n_py_edi_status": "accepted", "l10n_py_cdc": CDC})
        return move

    def inutilization(self, number_from, number_to=None):
        return self.env["l10n_py.number.inutilization"].create(
            {
                "authorization_id": self.auths["fe"].id,
                "number_from": number_from,
                "number_to": number_to or number_from,
                "motive": "Documento rechazado que cambió",
            }
        )

    # === Cancelación ===

    def cancel_button(self, user=None):
        move = self.env["account.move"]
        if user:
            move = move.with_user(user)
        arch = move.get_view(view_type="form")["arch"]
        buttons = etree.fromstring(arch).xpath("//button[@string='Cancelar EDI']")
        return buttons[0] if buttons else None

    def test_el_boton_cancelar_edi_abre_el_asistente_del_motivo(self):
        action = self.env.ref("l10n_py_edi_sifende.action_l10n_py_edi_cancel_wizard")
        button = self.cancel_button()
        self.assertEqual(button.get("type"), "action")
        self.assertEqual(button.get("name"), str(action.id))
        self.assertEqual(action.res_model, "l10n_py.edi.cancel.wizard")
        self.assertEqual(action.target, "new")

    def test_el_boton_cancelar_edi_es_de_facturacion(self):
        biller = self.make_user("facturador_ui", "account.group_account_invoice")
        reader = self.make_user("auditor_ui", "account.group_account_readonly")
        self.assertIsNotNone(self.cancel_button(biller))
        self.assertIsNone(self.cancel_button(reader))

    def test_cancelar_desde_el_asistente_pide_el_motivo_y_lo_envia(self):
        move = self.accepted_move()
        self.fake.add("POST", "/cancelar$", EVENT_OK)
        action = self.env.ref("l10n_py_edi_sifende.action_l10n_py_edi_cancel_wizard")
        wizard = (
            self.env[action.res_model]
            .with_context(active_id=move.id, active_model="account.move")
            .create({"motive": "Error en el monto facturado"})
        )
        self.assertEqual(wizard.invoice_id, move)
        wizard.action_cancel()
        self.assertEqual(move.l10n_py_edi_status, "cancelled")
        self.assertEqual(
            self.fake.calls_to("POST", "/cancelar$")[0].json,
            {"motivo": "Error en el monto facturado"},
        )

    def test_en_sandbox_el_boton_cancelar_edi_se_oculta(self):
        move = self.accepted_move()
        self.assertFalse(move.l10n_py_sifende_sandbox)
        self.connector.sifende_api_key = "sk_sandbox_clave-ficticia"
        move.invalidate_recordset()
        self.assertTrue(move.l10n_py_sifende_sandbox)
        self.assertIn("l10n_py_sifende_sandbox", self.cancel_button().get("invisible"))

    def test_el_ambiente_sandbox_que_informa_sifende_tambien_cuenta(self):
        move = self.accepted_move()
        self.connector.sifende_ambiente = "SANDBOX"
        self.assertTrue(move.l10n_py_sifende_sandbox)

    def test_cancelar_en_sandbox_avisa_sin_llamar_a_sifende(self):
        move = self.accepted_move()
        self.connector.sifende_api_key = "sk_sandbox_clave-ficticia"
        with self.assertRaisesRegex(UserError, "SANDBOX"):
            move.action_cancel_edi()
        self.assertFalse(self.fake.calls_to("POST", ".*"))
        self.assertEqual(move.l10n_py_edi_status, "accepted")

    # === Inutilización ===

    def test_la_inutilizacion_tiene_menu_para_el_responsable_contable(self):
        action = self.env.ref("l10n_py_edi_base.action_l10n_py_number_inutilization")
        domain = [("action", "=", f"ir.actions.act_window,{action.id}")]
        menu = self.env["ir.ui.menu"].search(domain)
        root = self.env.ref("l10n_py_edi_base.menu_l10n_py_edi_root")
        self.assertEqual(menu.parent_id, root)
        self.assertEqual(root.parent_id, self.env.ref("account.menu_finance"))
        self.assertEqual(
            menu.complete_name.split("/", 1)[1],
            "Facturación Electrónica/Inutilización de números",
        )
        manager = self.make_user("gerente_ui", "account.group_account_manager")
        biller = self.make_user("facturador_menu", "account.group_account_invoice")
        self.assertIn(menu.id, menu.with_user(manager)._visible_menu_ids())
        self.assertNotIn(menu.id, menu.with_user(biller)._visible_menu_ids())

    def test_se_puede_inutilizar_el_numero_de_un_documento_rechazado(self):
        move = self.make_move("fe")
        move.l10n_py_edi_status = "rejected"
        self.inutilization(move.l10n_py_invoice_number)

    def test_no_se_puede_inutilizar_el_numero_de_un_documento_vigente(self):
        for status in ("to_send", "sent", "processing", "accepted", "cancelled"):
            move = self.make_move("fe")
            move.l10n_py_edi_status = status
            with self.assertRaisesRegex(ValidationError, "ya fueron usados"):
                self.inutilization(move.l10n_py_invoice_number)

    def test_procedimiento_de_un_rechazado_que_cambio(self):
        rejected = self.make_move("fe")
        rejected.l10n_py_edi_status = "rejected"
        number = rejected.l10n_py_invoice_number
        inutilization = self.inutilization(number)
        self.fake.add("POST", "/inutilizar$", EVENT_OK)
        inutilization.action_send()
        self.assertEqual(inutilization.state, "accepted")
        rejected.button_draft()
        rejected.button_cancel()
        self.assertEqual(rejected.state, "cancel")
        replacement = self.make_move("fe")
        self.assertEqual(replacement.l10n_py_invoice_number, number + 1)

    # === Clave de idempotencia de los eventos ===

    def fails(self, method):
        # sin assertRaises: su savepoint desharía la clave confirmada aparte
        try:
            method()
        except UserError:
            return
        self.fail("Se esperaba un UserError")

    def event_keys(self, pattern):
        return [
            c.headers["Idempotency-Key"] for c in self.fake.calls_to("POST", pattern)
        ]

    def test_reintentar_la_cancelacion_tras_un_503_usa_la_misma_clave(self):
        move = self.accepted_move()
        self.fake.add(
            "POST", "/cancelar$", problem("idempotency-upstream-unknown", 503)
        )
        for _ in range(2):
            self.fails(move.action_cancel_edi)
        keys = self.event_keys("/cancelar$")
        self.assertEqual(len(keys), 6)
        self.assertEqual(len(set(keys)), 1)
        self.assertEqual(move.l10n_py_sifende_event_key, keys[0])
        self.fake.add("POST", "/cancelar$", EVENT_OK)
        move.action_cancel_edi()
        self.assertEqual(self.event_keys("/cancelar$")[-1], keys[0])
        self.assertFalse(move.l10n_py_sifende_event_key)

    def test_una_cancelacion_rechazada_por_la_api_usa_clave_nueva_al_reintentar(self):
        move = self.accepted_move()
        self.fake.add("POST", "/cancelar$", problem("validation-error", 400, "Plazo"))
        with self.assertRaises(UserError):
            move.action_cancel_edi()
        self.assertFalse(move.l10n_py_sifende_event_key)
        self.fake.add("POST", "/cancelar$", EVENT_OK)
        move.action_cancel_edi()
        first, second = self.event_keys("/cancelar$")
        self.assertNotEqual(first, second)

    def test_una_cancelacion_rechazada_con_200_falla_y_olvida_la_clave(self):
        move = self.accepted_move()
        self.fake.add(
            "POST",
            "/cancelar$",
            FakeResponse(
                200,
                {"estadoEvento": "RECHAZADO", "mensajeRespuesta": "[4003] Plazo"},
            ),
        )
        with self.assertRaisesRegex(UserError, r"\[4003\] Plazo"):
            move.action_cancel_edi()
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertFalse(move.l10n_py_sifende_event_key)

    def test_una_cancelacion_sin_estado_aprobado_no_se_da_por_cancelada(self):
        move = self.accepted_move()
        for body in (
            {},
            {"estadoEvento": "PENDIENTE"},
            {"estadoEvento": "INDETERMINADA"},
            {"estadoEvento": "OTRO"},
        ):
            with self.subTest(body):
                self.fake.add("POST", "/cancelar$", FakeResponse(200, body))
                self.fails(move.action_cancel_edi)
                self.assertEqual(move.l10n_py_edi_status, "accepted")
                self.assertTrue(move.l10n_py_sifende_event_key)
        keys = self.event_keys("/cancelar$")
        self.assertEqual(len(keys), 4)
        self.assertEqual(len(set(keys)), 1)
        self.assertEqual(move.l10n_py_sifende_event_key, keys[0])
        self.fake.add("POST", "/cancelar$", EVENT_OK)
        move.action_cancel_edi()
        self.assertEqual(self.event_keys("/cancelar$")[-1], keys[0])
        self.assertEqual(move.l10n_py_edi_status, "cancelled")
        self.assertFalse(move.l10n_py_sifende_event_key)

    def test_una_inutilizacion_sin_estado_aprobado_se_reintenta_con_la_misma_clave(
        self,
    ):
        inutilization = self.inutilization(
            self.make_move("fe").l10n_py_invoice_number + 5
        )
        with self.assertLogs(OCA_INUTILIZATION_LOGGER, "WARNING"):
            for body in ({}, {"estadoEvento": "PENDIENTE"}):
                self.fake.add("POST", "/inutilizar$", FakeResponse(200, body))
                self.fails(inutilization.action_send)
                inutilization.state = "draft"
        keys = self.event_keys("/inutilizar$")
        self.assertEqual(len(keys), 2)
        self.assertEqual(len(set(keys)), 1)
        self.assertEqual(inutilization.l10n_py_sifende_event_key, keys[0])
        self.fake.add("POST", "/inutilizar$", EVENT_OK)
        inutilization.action_send()
        self.assertEqual(inutilization.state, "accepted")
        self.assertFalse(inutilization.l10n_py_sifende_event_key)

    def test_una_inutilizacion_rechazada_con_200_falla_y_olvida_la_clave(self):
        inutilization = self.inutilization(5)
        self.fake.add(
            "POST",
            "/inutilizar$",
            FakeResponse(
                200,
                {"estadoEvento": "RECHAZADO", "mensajeRespuesta": "[4068] Rango"},
            ),
        )
        with (
            self.assertLogs(OCA_INUTILIZATION_LOGGER, "WARNING"),
            self.assertRaisesRegex(UserError, r"\[4068\] Rango"),
        ):
            inutilization.action_send()
        self.assertFalse(inutilization.l10n_py_sifende_event_key)

    def test_reintentar_la_inutilizacion_tras_un_503_usa_la_misma_clave(self):
        inutilization = self.inutilization(
            self.make_move("fe").l10n_py_invoice_number + 5
        )
        self.fake.add(
            "POST", "/inutilizar$", problem("idempotency-upstream-unknown", 503)
        )
        with self.assertLogs(OCA_INUTILIZATION_LOGGER, "WARNING"):
            for _ in range(2):
                self.fails(inutilization.action_send)
                inutilization.state = "draft"
        self.assertEqual(len(set(self.event_keys("/inutilizar$"))), 1)
        self.fake.add("POST", "/inutilizar$", EVENT_OK)
        inutilization.action_send()
        self.assertEqual(inutilization.state, "accepted")
        self.assertFalse(inutilization.l10n_py_sifende_event_key)

    def pending_inutilization(self):
        inutilization = self.inutilization(
            self.make_move("fe").l10n_py_invoice_number + 5
        )
        self.fake.add(
            "POST", "/inutilizar$", problem("idempotency-upstream-unknown", 503)
        )
        with self.assertLogs(OCA_INUTILIZATION_LOGGER, "WARNING"):
            self.fails(inutilization.action_send)
        inutilization.state = "draft"
        self.assertTrue(inutilization.l10n_py_sifende_event_key)
        return inutilization

    def test_una_inutilizacion_pendiente_no_cambia_su_solicitud(self):
        inutilization = self.pending_inutilization()
        number = inutilization.number_from
        for values in (
            {"number_from": number + 2, "number_to": number + 2},
            {"number_to": number + 1},
            {"motive": "Otro motivo distinto"},
            {"authorization_id": self.auths["nc"].id},
        ):
            with self.subTest(values), self.assertRaisesRegex(UserError, "pendiente"):
                inutilization.write(values)
        self.assertEqual(inutilization.number_from, number)
        self.assertEqual(inutilization.number_to, number)

    def test_la_inutilizacion_pendiente_reenvia_el_rango_original(self):
        inutilization = self.pending_inutilization()
        number = inutilization.number_from
        inutilization.write({"number_from": number, "motive": inutilization.motive})
        self.fake.add("POST", "/inutilizar$", EVENT_OK)
        inutilization.action_send()
        call = self.fake.calls_to("POST", "/inutilizar$")[-1]
        self.assertEqual(call.json["numeroInicio"], str(number).zfill(7))
        self.assertEqual(inutilization.state, "accepted")

    def test_una_inutilizacion_sin_clave_pendiente_se_edita(self):
        inutilization = self.inutilization(5)
        inutilization.write({"number_from": 6, "number_to": 7})
        self.assertEqual(inutilization.quantity, 2)

    def test_una_inutilizacion_rechazada_por_la_api_se_puede_corregir(self):
        inutilization = self.inutilization(5)
        self.fake.add("POST", "/inutilizar$", problem("validation-error", 400, "Dato"))
        with self.assertLogs(OCA_INUTILIZATION_LOGGER, "WARNING"):
            self.fails(inutilization.action_send)
        inutilization.write({"state": "draft", "number_from": 6, "number_to": 6})
        self.assertEqual(inutilization.number_from, 6)

    def test_la_vista_de_la_inutilizacion_bloquea_la_solicitud_pendiente(self):
        arch = self.env["l10n_py.number.inutilization"].get_view(view_type="form")[
            "arch"
        ]
        tree = etree.fromstring(arch)
        for name in ("authorization_id", "number_from", "number_to", "motive"):
            node = tree.xpath(f"//field[@name='{name}']")[0]
            self.assertIn("l10n_py_sifende_event_key", node.get("readonly"), name)

    def test_una_inutilizacion_rechazada_por_la_api_muestra_su_mensaje(self):
        inutilization = self.inutilization(5)
        self.fake.add(
            "POST",
            "/inutilizar$",
            problem(
                "evento-inutilizacion-error",
                400,
                "El número fin debe ser mayor al número inicio (código SIFEN 4068)",
            ),
        )
        with (
            self.assertLogs(OCA_INUTILIZATION_LOGGER, "WARNING"),
            self.assertRaisesRegex(UserError, "debe ser mayor al número inicio"),
        ):
            inutilization.action_send()
        self.assertFalse(inutilization.l10n_py_sifende_event_key)

    def test_la_inutilizacion_envia_la_serie_del_timbrado(self):
        inutilization = self.inutilization(5)
        self.fake.add("POST", "/inutilizar$", EVENT_OK)
        inutilization.action_send()
        self.assertNotIn("serie", self.fake.calls_to("POST", "/inutilizar$")[0].json)
        inutilization = self.inutilization(6)
        inutilization.authorization_id.series = "AB"
        inutilization.action_send()
        self.assertEqual(
            self.fake.calls_to("POST", "/inutilizar$")[1].json["serie"], "AB"
        )
