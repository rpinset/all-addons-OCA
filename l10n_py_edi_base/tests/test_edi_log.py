# l10n_py_edi_base/tests/test_edi_log.py

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "l10n_py")
class TestEDILog(TransactionCase):
    """Tests para l10n_py.edi.log"""

    def test_log_operation_success(self):
        """Crear log de operación exitosa"""
        log = self.env["l10n_py.edi.log"].log_operation(
            operation_type="send",
            provider="factpy",
            execution_time=150.5,
            success=True,
        )
        self.assertTrue(log)
        self.assertTrue(log.success)
        self.assertFalse(log.error)

    def test_log_operation_error(self):
        """Crear log de operación con error"""
        log = self.env["l10n_py.edi.log"].log_operation(
            operation_type="send",
            provider="factpy",
            execution_time=500.0,
            success=False,
            error_message="Connection timeout",
        )
        self.assertTrue(log)
        self.assertFalse(log.success)
        self.assertTrue(log.error)
        self.assertEqual(log.error_message, "Connection timeout")

    def test_error_computed(self):
        """Campo error computed correctamente"""
        log = self.env["l10n_py.edi.log"].create(
            {
                "operation_type": "send",
                "provider": "factpy",
                "status_code": 500,
                "success": False,
            }
        )
        self.assertTrue(log.error)

        log2 = self.env["l10n_py.edi.log"].create(
            {
                "operation_type": "send",
                "provider": "factpy",
                "status_code": 200,
                "success": True,
            }
        )
        self.assertFalse(log2.error)

    def test_duration_human_ms(self):
        """Formateo < 1000ms"""
        log = self.env["l10n_py.edi.log"].create(
            {
                "operation_type": "send",
                "provider": "factpy",
                "execution_time": 150.5,
            }
        )
        self.assertIn("ms", log.duration_human)

    def test_duration_human_seconds(self):
        """Formateo >= 1000ms"""
        log = self.env["l10n_py.edi.log"].create(
            {
                "operation_type": "send",
                "provider": "factpy",
                "execution_time": 2500.0,
            }
        )
        self.assertIn("s", log.duration_human)
