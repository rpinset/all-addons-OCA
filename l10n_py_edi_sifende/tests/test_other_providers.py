# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests import tagged

from odoo.addons.l10n_py_edi_base.models.edi_connector import (
    EDIConnector as BaseConnector,
)

from .common import SifendeCommon


@tagged("post_install", "-at_install", "l10n_py_edi_sifende")
class TestOtherProviders(SifendeCommon):
    """Un conector que no es Sifende conserva el comportamiento de l10n_py_edi_base."""

    def setUp(self):
        super().setUp()
        field = self.env["l10n_py.edi.connector"]._fields["provider_type"]
        for attribute, value in (
            ("selection", [*field.selection, ("otro", "Otro")]),
            ("_selection", {**field._selection, "otro": "Otro"}),
        ):
            patcher = patch.object(field, attribute, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.connector.provider_type = "otro"

    def test_los_metodos_publicos_llegan_al_conector_base(self):
        with self.assertRaisesRegex(UserError, "no implementa el envío"):
            self.connector.send_document({})
        with self.assertRaisesRegex(UserError, "no implementa la consulta"):
            self.connector.check_status(" ")
        with self.assertRaisesRegex(UserError, "no implementa la cancelación"):
            self.connector.cancel_document("1")
        with self.assertRaisesRegex(UserError, "no implementa la inutilización"):
            self.connector.inutilize_range({})
        with self.assertRaisesRegex(UserError, "no implementa la previsualización"):
            self.connector.preview_document({})
        with self.assertRaisesRegex(UserError, "no implementa la prueba de conexión"):
            self.connector.test_connection()

    def test_el_diccionario_no_lleva_la_clave_sifende(self):
        data = self.make_move("fe")._prepare_edi_document_data()
        self.assertNotIn("sifende", data)
        self.assertNotIn("sifende", data["items"][0])

    def test_el_envio_sigue_el_flujo_sincronico_de_oca(self):
        move = self.make_move("fe")
        response = {
            "success": True,
            "result": {
                "deList": [{"cdc": "0" * 44, "qr": "https://qr", "xml": "<x/>"}],
                "loteId": "L1",
            },
        }
        with (
            patch.object(BaseConnector, "send_document", return_value=response),
            patch.object(type(move), "_generate_kude"),
        ):
            move.action_send_edi()
        self.assertEqual(move.l10n_py_edi_status, "accepted")
        self.assertEqual(move.l10n_py_edi_batch_id, "L1")
        self.assertFalse(self.fake.calls)

    def test_el_reintento_no_toca_el_contador_de_sifende(self):
        move = self.make_move("fe")
        move.l10n_py_edi_status = "error"
        with patch.object(type(move), "action_send_edi", return_value=None):
            move.action_retry_edi()
        self.assertEqual(move.l10n_py_sifende_intento, 0)

    def test_el_cron_de_sifende_ignora_a_la_empresa(self):
        move = self.make_move("fe")
        move.write({"l10n_py_edi_status": "processing", "l10n_py_cdc": "1" * 44})
        self.env["account.move"]._cron_sifende_check_status()
        self.assertFalse(self.fake.calls)
        self.assertEqual(move.l10n_py_edi_status, "processing")
