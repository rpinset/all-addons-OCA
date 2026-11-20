# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import date

from lxml import etree

from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import CDC, SifendeCommon

NEW_VALUES = {
    "l10n_py_emission_type": "2",
    "l10n_py_transaction_type": "2",
    "l10n_py_presence_type": "2",
    "l10n_py_exchange_rate_condition": "2",
    "l10n_py_receipt_id": "OTRO-ID",
    "l10n_py_contingency_motive": "Corte de internet",
    "l10n_py_nre_motive": "6",
    "l10n_py_nre_estimated_invoice_date": date(2030, 1, 1),
    "l10n_py_sifende_motivo_emision": "3",
    "l10n_py_sifende_responsable_emision": "2",
    "l10n_py_sifende_km_recorrido": 99,
    "l10n_py_afe_constancia_type": "2",
    "l10n_py_afe_constancia_number": "123",
    "l10n_py_afe_constancia_control": "456",
    "l10n_py_afe_vendor_doc_type": "2",
    "l10n_py_afe_vendor_doc_number": "789",
    "l10n_py_afe_vendor_name": "Otro vendedor",
    "l10n_py_afe_vendor_address": "Otra calle",
    "l10n_py_afe_vendor_house": 5,
    "l10n_py_afe_vendor_department": 1,
    "l10n_py_afe_vendor_district": 2,
    "l10n_py_afe_vendor_city": 3,
    "l10n_py_afe_provision_address": "Otra provisión",
    "l10n_py_afe_provision_department": 1,
    "l10n_py_afe_provision_district": 2,
    "l10n_py_afe_provision_city": 3,
}


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestFrozenFiscal(SifendeCommon):
    def accepted(self, move=None):
        move = move or self.make_move("fe")
        move.write({"l10n_py_edi_status": "accepted", "l10n_py_cdc": CDC})
        return move

    def test_los_datos_fiscales_se_pueden_editar_antes_de_enviar(self):
        move = self.make_move("fe")
        move.write(NEW_VALUES)
        self.assertEqual(move.l10n_py_presence_type, "2")
        self.assertEqual(move.l10n_py_receipt_id, "OTRO-ID")

    def test_los_datos_fiscales_no_se_editan_con_el_documento_aceptado(self):
        move = self.accepted()
        for name, value in NEW_VALUES.items():
            with self.subTest(name), self.assertRaisesRegex(UserError, "fiscales"):
                move.write({name: value})

    def test_los_datos_fiscales_no_se_editan_con_el_documento_procesando(self):
        move = self.make_move("fe")
        self.route_emission(self.emission_response())
        move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "processing")
        with self.assertRaisesRegex(UserError, "fiscales"):
            move.l10n_py_presence_type = "3"

    def test_el_tipo_de_emision_y_el_de_transaccion_quedan_como_estaban(self):
        move = self.accepted()
        with self.assertRaises(UserError):
            move.write({"l10n_py_emission_type": "2", "l10n_py_transaction_type": "5"})
        self.assertEqual(move.l10n_py_emission_type, "1")
        self.assertEqual(move.l10n_py_transaction_type, "1")

    def test_el_mismo_valor_no_cuenta_como_cambio(self):
        move = self.accepted(
            self.make_move("fe", l10n_py_nre_estimated_invoice_date=date(2030, 1, 1))
        )
        move.write(
            {
                "l10n_py_presence_type": "1",
                "l10n_py_receipt_id": False,
                "l10n_py_contingency_motive": "",
                "l10n_py_nre_estimated_invoice_date": "2030-01-01",
            }
        )

    def test_lo_que_el_conector_escribe_al_aceptar_no_se_bloquea(self):
        move = self.accepted()
        move.write(
            {
                "l10n_py_edi_status": "cancelled",
                "l10n_py_edi_message": "Cancelado",
                "l10n_py_qr_string": "https://ekuatia.set.gov.py/consultas/qr",
            }
        )
        self.assertEqual(move.l10n_py_edi_status, "cancelled")

    def test_el_transporte_no_se_cambia_con_el_documento_aceptado(self):
        move = self.accepted(self.make_nre())
        other = self.env["l10n_py.transport"].create(self.nre_transport_vals())
        with self.assertRaisesRegex(UserError, "fiscales"):
            move.l10n_py_transport_id = other

    def test_el_transporte_y_sus_hijos_no_se_editan_con_el_documento_aceptado(self):
        move = self.accepted(self.make_nre())
        transport = move.l10n_py_transport_id
        vehicle, delivery = transport.vehicle_ids, transport.delivery_ids
        with self.assertRaisesRegex(UserError, "fiscales"):
            transport.driver_name = "Otro chofer"
        with self.assertRaisesRegex(UserError, "fiscales"):
            transport.sifende_driver_address = "Otra calle"
        with self.assertRaisesRegex(UserError, "fiscales"):
            vehicle.plate_number = "ZZZ999"
        with self.assertRaisesRegex(UserError, "fiscales"):
            delivery.address = "Otra calle"
        with self.assertRaisesRegex(UserError, "fiscales"):
            self.env["l10n_py.transport.vehicle"].create(
                {
                    "transport_id": transport.id,
                    "vehicle_type": "CAMION",
                    "brand": "ISUZU",
                    "plate_number": "XYZ123",
                }
            )
        with self.assertRaisesRegex(UserError, "fiscales"):
            delivery.unlink()
        with self.assertRaisesRegex(UserError, "fiscales"):
            vehicle.unlink()
        with self.assertRaisesRegex(UserError, "fiscales"):
            transport.unlink()
        self.assertEqual(transport.driver_name, "Carlos Benítez")
        self.assertEqual(move.l10n_py_transport_id, transport)

    def test_el_transporte_se_edita_antes_de_enviar_y_sin_conector(self):
        move = self.make_nre()
        transport = move.l10n_py_transport_id
        transport.driver_name = "Otro chofer"
        transport.vehicle_ids.plate_number = "ZZZ999"
        transport.delivery_ids.address = "Otra calle"
        self.accepted(move)
        self.connector.unlink()
        transport.driver_name = "Chofer sin conector"
        self.assertEqual(transport.driver_name, "Chofer sin conector")

    def test_el_transporte_compartido_queda_congelado_por_cualquier_documento(self):
        sent = self.accepted(self.make_nre())
        transport = sent.l10n_py_transport_id
        other = self.make_move("nr")
        self.env.cr.execute(
            "UPDATE account_move SET l10n_py_transport_id = %s WHERE id = %s",
            (transport.id, other.id),
        )
        other.invalidate_recordset(["l10n_py_transport_id"])
        with self.assertRaisesRegex(UserError, "fiscales"):
            transport.driver_name = "Otro chofer"

    def test_los_documentos_asociados_no_se_tocan_con_el_documento_aceptado(self):
        move = self.make_move("fe")
        associated = self.associate(move)
        self.accepted(move)
        with self.assertRaisesRegex(UserError, "fiscales"):
            self.associate(move, cdc="0" * 44)
        with self.assertRaisesRegex(UserError, "fiscales"):
            associated.cdc = "1" * 44
        with self.assertRaisesRegex(UserError, "fiscales"):
            associated.unlink()

    def test_los_documentos_asociados_se_editan_antes_de_enviar(self):
        move = self.make_move("fe")
        associated = self.associate(move)
        associated.cdc = "1" * 44
        associated.unlink()
        self.assertFalse(move.l10n_py_associated_document_ids)

    def test_la_vista_marca_los_datos_fiscales_como_solo_lectura(self):
        arch = self.env["account.move"].get_view(
            self.env.ref("account.view_move_form").id
        )["arch"]
        tree = etree.fromstring(arch)
        names = (
            *NEW_VALUES,
            "l10n_py_transport_id",
            "l10n_py_associated_document_ids",
            "l10n_py_sifende_afe_vendor_city_id",
            "l10n_py_sifende_afe_provision_city_id",
        )
        for name in names:
            nodes = tree.xpath(f"//field[@name='{name}']")
            self.assertTrue(nodes, name)
            for node in nodes:
                if node.get("invisible") == "1":
                    continue
                self.assertIn(
                    "l10n_py_sifende_frozen", node.get("readonly") or "", name
                )
