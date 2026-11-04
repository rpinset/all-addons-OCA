# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from .common import MercadoLibreCommon


class TestMercadoLibreBinding(MercadoLibreCommon):
    def test_state_helpers_write_the_expected_values(self):
        binding = self.env["mercadolibre.binding"]
        with patch.object(type(binding), "write", return_value=True) as write:
            binding.mark_synced()
            binding.mark_error("boom")
            binding.button_retry()
        synced, failed, pending = (call.args[0] for call in write.call_args_list)
        self.assertEqual(synced["state"], "synced")
        self.assertFalse(synced["error_message"])
        self.assertTrue(synced["sync_date"])
        self.assertEqual(failed, {"state": "error", "error_message": "boom"})
        self.assertEqual(pending, {"state": "pending", "error_message": False})
