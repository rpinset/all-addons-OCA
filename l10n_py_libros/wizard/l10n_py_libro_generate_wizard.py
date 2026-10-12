# l10n_py_libros/wizard/l10n_py_libro_generate_wizard.py

from odoo import fields, models

TIPO_REGISTROS = ("ventas", "compras", "ingresos", "egresos")


class L10nPyLibroGenerateWizard(models.TransientModel):
    _name = "l10n_py.libro.generate.wizard"
    _description = "Generar/Exportar Libros DNIT"

    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )
    obligacion = fields.Selection(
        [("955", "955 - Mensual"), ("956", "956 - Anual")],
        required=True,
        default="955",
    )
    year = fields.Integer(required=True, default=lambda self: fields.Date.today().year)
    month = fields.Integer(default=lambda self: fields.Date.today().month)
    incluir_ventas = fields.Boolean(default=True)
    incluir_compras = fields.Boolean(default=True)
    incluir_ingresos = fields.Boolean(default=False)
    incluir_egresos = fields.Boolean(default=False)

    def action_generate(self):
        self.ensure_one()
        Libro = self.env["l10n_py.libro"]
        month_value = self.month if self.obligacion == "955" else 0
        resultados = []
        for tipo_registro in TIPO_REGISTROS:
            if not self[f"incluir_{tipo_registro}"]:
                continue
            libro = Libro.search(
                [
                    ("company_id", "=", self.company_id.id),
                    ("tipo_registro", "=", tipo_registro),
                    ("obligacion", "=", self.obligacion),
                    ("year", "=", self.year),
                    ("month", "=", month_value),
                ],
                limit=1,
            )
            if not libro:
                libro = Libro.create(
                    {
                        "company_id": self.company_id.id,
                        "tipo_registro": tipo_registro,
                        "obligacion": self.obligacion,
                        "year": self.year,
                        "month": month_value,
                    }
                )
            if tipo_registro in ("ventas", "compras"):
                libro.action_generate_lines()
            resultados.append(libro)

        libros = self.env["l10n_py.libro"].browse([lib.id for lib in resultados])
        return {
            "type": "ir.actions.act_window",
            "name": self.env._("Libros generados"),
            "res_model": "l10n_py.libro",
            "view_mode": "list,form",
            "domain": [("id", "in", libros.ids)],
        }
