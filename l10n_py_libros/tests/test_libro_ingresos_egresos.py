from odoo.tests import tagged

from .test_libro_common import LibroCommonCase


@tagged("post_install", "-at_install", "l10n_py", "l10n_py_libros")
class TestLibroIngresosEgresos(LibroCommonCase):
    def _create_ingresos_line(self, libro, **vals):
        base_vals = {
            "libro_id": libro.id,
            "f_tipo_comprobante": "203",
            "f_fecha_emision": "2026-01-15",
            "f_numero_comprobante": "0000001",
            "f_tipo_identificacion": "11",
            "f_numero_identificacion": "80011111",
            "f_nombre_razon_social": "Cliente Ingresos Test",
            "f_monto_gravado": 1000,
            "f_monto_no_gravado_exonerado": 0,
            "f_monto_total": 1000,
            "f_imputa_ire": "S",
            "f_imputa_irp_rsp": "N",
            # D4 :424-433 - obligatorio sólo para el tipo 203 (default de
            # este fixture); no interfiere con otros tipos que sobrescriben
            # f_tipo_comprobante via **vals.
            "f_comprobante_asociado_numero": "001-001-0000001",
            "f_comprobante_asociado_timbrado": "12345678",
        }
        base_vals.update(vals)
        return self.env["l10n_py.libro.line"].create(base_vals)

    def _create_egresos_line(self, libro, **vals):
        base_vals = {
            "libro_id": libro.id,
            "f_tipo_comprobante": "201",
            "f_fecha_emision": "2026-01-15",
            "f_numero_comprobante": "0000001",
            "f_tipo_identificacion": "11",
            "f_numero_identificacion": "80022222",
            "f_nombre_razon_social": "Proveedor Egresos Test",
            "f_monto_total": 1000,
            "f_imputa_iva": "N",
            "f_imputa_ire": "S",
            "f_imputa_irp_rsp": "N",
            "f_no_imputa": "N",
            # D4 :521-546 - preenche todos os campos condicionais possíveis
            # (201 exige 17/18; 207/211 exigem 13/14; 206 exige 15) para que
            # os testes que sobrescrevem f_tipo_comprobante via **vals não
            # quebrem por falta de um campo condicional irrelevante ao caso
            # que estão testando.
            "f_comprobante_asociado_numero": "001-001-0000001",
            "f_comprobante_asociado_timbrado": "12345678",
            "f_numero_cuenta": "000123456",
            "f_banco": "Banco Egresos Test",
            "f_empleador_ips": "999999",
        }
        base_vals.update(vals)
        return self.env["l10n_py.libro.line"].create(base_vals)

    def test_ingresos_203_lancamento_manual(self):
        libro = self._create_libro("ingresos")
        line = self._create_ingresos_line(libro)
        self.assertEqual(line.state, "ok", line.error_message)
        self.assertEqual(line.tipo_registro, "ingresos")

    def test_ingresos_208_periodo_mm_aaaa(self):
        libro = self._create_libro("ingresos")
        line = self._create_ingresos_line(
            libro,
            f_tipo_comprobante="208",
            f_periodo_mm_aaaa="01/2026",
            f_monto_gravado=1000,
            f_monto_no_gravado_exonerado=0,
            f_monto_total=1000,
        )
        self.assertEqual(line.state, "ok", line.error_message)
        line.f_periodo_mm_aaaa = False
        self.assertEqual(line.state, "erro")

    def test_egresos_201_lancamento_manual(self):
        libro = self._create_libro("egresos")
        line = self._create_egresos_line(libro)
        self.assertEqual(line.state, "ok", line.error_message)
        self.assertEqual(line.tipo_registro, "egresos")

    def test_egresos_207_imputa_iva_s_permitido(self):
        libro = self._create_libro("egresos")
        line = self._create_egresos_line(
            libro, f_tipo_comprobante="207", f_imputa_iva="S"
        )
        self.assertEqual(line.state, "ok", line.error_message)

    def test_egresos_nao_207_imputa_iva_s_marca_erro(self):
        libro = self._create_libro("egresos")
        line = self._create_egresos_line(
            libro, f_tipo_comprobante="201", f_imputa_iva="S"
        )
        self.assertEqual(line.state, "erro")

    def test_nenhuma_obrigacao_imputada_marca_linha_em_erro(self):
        libro = self._create_libro("egresos")
        line = self._create_egresos_line(
            libro, f_imputa_iva="N", f_imputa_ire="N", f_imputa_irp_rsp="N"
        )
        self.assertEqual(line.state, "erro")

    def test_periodo_vazio_confirma_sem_arquivo(self):
        libro = self._create_libro("ingresos")
        libro.action_confirm()
        self.assertEqual(libro.state, "confirmed")
        self.assertFalse(libro.l10n_py_libro_attachment_ids)

    def test_egresos_ingresos_regras_condicionais_matriz(self):
        """Matriz D4 completa (spec gap R5.5/R6.4): cada regra condicional
        de Egresos/Ingresos coberta por um caso positivo e um negativo."""
        libro_egresos = self._create_libro("egresos")
        libro_ingresos = self._create_libro("ingresos")

        egresos_cases = [
            # (label, overrides, expect_ok)
            (
                "204_identificacion_fixa_11_ok",
                {"f_tipo_comprobante": "204", "f_tipo_identificacion": "11"},
                True,
            ),
            (
                "204_identificacion_distinta_de_11_erro",
                {"f_tipo_comprobante": "204", "f_tipo_identificacion": "12"},
                False,
            ),
            (
                "202_identificacion_fixa_17_ok",
                {"f_tipo_comprobante": "202", "f_tipo_identificacion": "17"},
                True,
            ),
            (
                "202_identificacion_distinta_de_17_erro",
                {"f_tipo_comprobante": "202", "f_tipo_identificacion": "11"},
                False,
            ),
            (
                "206_identificacion_numero_exentos_ok",
                {
                    "f_tipo_comprobante": "206",
                    "f_tipo_identificacion": False,
                    "f_numero_identificacion": False,
                    "f_periodo_mm_aaaa": "01/2026",
                },
                True,
            ),
            (
                "206_nombre_exento_ok",
                {
                    "f_tipo_comprobante": "206",
                    "f_nombre_razon_social": False,
                    "f_periodo_mm_aaaa": "01/2026",
                },
                True,
            ),
            (
                "209_nombre_requerido_erro",
                {
                    "f_tipo_comprobante": "209",
                    "f_tipo_identificacion": "13",
                    "f_nombre_razon_social": False,
                },
                False,
            ),
            (
                "208_numero_no_requerido_ok",
                {
                    "f_tipo_comprobante": "208",
                    "f_numero_comprobante": False,
                    "f_periodo_mm_aaaa": "01/2026",
                    "f_tipo_identificacion": "11",
                },
                True,
            ),
            (
                "201_numero_requerido_erro",
                {"f_tipo_comprobante": "201", "f_numero_comprobante": False},
                False,
            ),
            (
                "207_cuenta_banco_requeridos_ok",
                {"f_tipo_comprobante": "207", "f_imputa_iva": "S"},
                True,
            ),
            (
                "207_cuenta_banco_ausentes_erro",
                {
                    "f_tipo_comprobante": "207",
                    "f_imputa_iva": "S",
                    "f_numero_cuenta": False,
                    "f_banco": False,
                },
                False,
            ),
            (
                "209_cuenta_banco_no_requeridos_ok",
                {
                    "f_tipo_comprobante": "209",
                    "f_especificar_tipo_documento": "Otro",
                    "f_numero_cuenta": False,
                    "f_banco": False,
                },
                True,
            ),
            (
                "206_empleador_ips_requerido_erro",
                {
                    "f_tipo_comprobante": "206",
                    "f_periodo_mm_aaaa": "01/2026",
                    "f_empleador_ips": False,
                },
                False,
            ),
            (
                "206_empleador_ips_presente_ok",
                {"f_tipo_comprobante": "206", "f_periodo_mm_aaaa": "01/2026"},
                True,
            ),
            (
                "201_asociado_ausente_erro",
                {
                    "f_tipo_comprobante": "201",
                    "f_comprobante_asociado_numero": False,
                    "f_comprobante_asociado_timbrado": False,
                },
                False,
            ),
            (
                "209_fecha_anterior_2021_erro",
                {
                    "f_tipo_comprobante": "209",
                    "f_especificar_tipo_documento": "Otro",
                    "f_fecha_emision": "2020-12-31",
                },
                False,
            ),
            (
                "209_fecha_posterior_2021_ok",
                {
                    "f_tipo_comprobante": "209",
                    "f_especificar_tipo_documento": "Otro",
                    "f_fecha_emision": "2021-01-02",
                },
                True,
            ),
        ]
        for label, overrides, expect_ok in egresos_cases:
            with self.subTest(label):
                line = self._create_egresos_line(libro_egresos, **overrides)
                self.assertEqual(
                    line.state,
                    "ok" if expect_ok else "erro",
                    f"{label}: {line.error_message}",
                )

        ingresos_cases = [
            (
                "210_identificacion_permitida_ok",
                {
                    "f_tipo_comprobante": "210",
                    "f_tipo_identificacion": "12",
                    "f_especificar_tipo_documento": "Otro",
                },
                True,
            ),
            (
                "210_identificacion_no_permitida_erro",
                {
                    "f_tipo_comprobante": "210",
                    "f_tipo_identificacion": "14",
                    "f_especificar_tipo_documento": "Otro",
                },
                False,
            ),
            (
                "208_identificacion_fixa_11_ok",
                {
                    "f_tipo_comprobante": "208",
                    "f_tipo_identificacion": "11",
                    "f_numero_comprobante": False,
                    "f_periodo_mm_aaaa": "01/2026",
                },
                True,
            ),
            (
                "208_identificacion_distinta_de_11_erro",
                {
                    "f_tipo_comprobante": "208",
                    "f_tipo_identificacion": "12",
                    "f_numero_comprobante": False,
                    "f_periodo_mm_aaaa": "01/2026",
                },
                False,
            ),
            (
                "208_numero_no_requerido_ok",
                {
                    "f_tipo_comprobante": "208",
                    "f_tipo_identificacion": "11",
                    "f_numero_comprobante": False,
                    "f_periodo_mm_aaaa": "01/2026",
                },
                True,
            ),
            (
                "203_numero_requerido_erro",
                {"f_tipo_comprobante": "203", "f_numero_comprobante": False},
                False,
            ),
            (
                "210_nombre_exento_ident_12_ok",
                {
                    "f_tipo_comprobante": "210",
                    "f_tipo_identificacion": "12",
                    "f_nombre_razon_social": False,
                    "f_especificar_tipo_documento": "Otro",
                },
                True,
            ),
            (
                "210_nombre_requerido_ident_13_erro",
                {
                    "f_tipo_comprobante": "210",
                    "f_tipo_identificacion": "13",
                    "f_nombre_razon_social": False,
                    "f_especificar_tipo_documento": "Otro",
                },
                False,
            ),
            (
                "203_asociado_ausente_erro",
                {
                    "f_tipo_comprobante": "203",
                    "f_comprobante_asociado_numero": False,
                    "f_comprobante_asociado_timbrado": False,
                },
                False,
            ),
            (
                "210_fecha_anterior_2021_erro",
                {
                    "f_tipo_comprobante": "210",
                    "f_tipo_identificacion": "11",
                    "f_especificar_tipo_documento": "Otro",
                    "f_fecha_emision": "2020-06-01",
                },
                False,
            ),
            (
                "210_fecha_posterior_2021_ok",
                {
                    "f_tipo_comprobante": "210",
                    "f_tipo_identificacion": "11",
                    "f_especificar_tipo_documento": "Otro",
                    "f_fecha_emision": "2021-06-01",
                },
                True,
            ),
        ]
        for label, overrides, expect_ok in ingresos_cases:
            with self.subTest(label):
                line = self._create_ingresos_line(libro_ingresos, **overrides)
                self.assertEqual(
                    line.state,
                    "ok" if expect_ok else "erro",
                    f"{label}: {line.error_message}",
                )
