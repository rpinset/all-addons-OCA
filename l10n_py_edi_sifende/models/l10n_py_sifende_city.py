# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import re
import unicodedata

from odoo import api, fields, models

# los códigos de OCA no coinciden con los de SIFEN desde Canindeyú en adelante
DEPARTMENT_CODES = {
    "CAPITAL": 1,
    "ASUNCION": 1,
    "CONCEPCION": 2,
    "SAN PEDRO": 3,
    "CORDILLERA": 4,
    "GUAIRA": 5,
    "CAAGUAZU": 6,
    "CAAZAPA": 7,
    "ITAPUA": 8,
    "MISIONES": 9,
    "PARAGUARI": 10,
    "ALTO PARANA": 11,
    "CENTRAL": 12,
    "NEEMBUCU": 13,
    "AMAMBAY": 14,
    "PTE HAYES": 15,
    "PRESIDENTE HAYES": 15,
    "BOQUERON": 16,
    "ALTO PARAGUAY": 17,
    "CANINDEYU": 18,
}
# el catálogo SIFEN abrevia los nombres que OCA escribe completos
ABBREVIATIONS = {
    "CNEL": "CORONEL",
    "GRAL": "GENERAL",
    "DR": "DOCTOR",
    "DRA": "DOCTORA",
    "PTE": "PRESIDENTE",
    "TTE": "TENIENTE",
    "CAP": "CAPITAN",
    "MCAL": "MARISCAL",
    "SGTO": "SARGENTO",
    "STA": "SANTA",
    "STO": "SANTO",
    "1RO": "PRIMERO",
    "1RA": "PRIMERA",
}
QUALIFIER_RE = re.compile(r"\([^)]*\)")


def normalize(text):
    text = unicodedata.normalize("NFD", QUALIFIER_RE.sub(" ", text or ""))
    text = "".join(char for char in text if not unicodedata.combining(char))
    tokens = re.sub(r"[^A-Z0-9]+", " ", text.upper()).split()
    return " ".join(ABBREVIATIONS.get(token, token) for token in tokens)


class SifendeCity(models.Model):
    _name = "l10n_py.sifende.city"
    _description = "Ciudad del catálogo SIFEN"
    _order = "department_code, district_code, code"
    _rec_names_search = ["name", "district_name", "department_name"]

    name = fields.Char(string="Ciudad", required=True, index=True)
    code = fields.Integer(string="Código de ciudad", required=True)
    district_code = fields.Integer(string="Código de distrito", required=True)
    district_name = fields.Char(string="Distrito", required=True)
    department_code = fields.Integer(string="Código de departamento", required=True)
    department_name = fields.Char(string="Departamento", required=True)

    _sql_constraints = [
        (
            "code_unique",
            "unique(code)",
            "El código de ciudad del catálogo SIFEN debe ser único.",
        )
    ]

    @api.depends("name", "district_name", "department_name")
    def _compute_display_name(self):
        for city in self:
            city.display_name = (
                f"{city.name} - {city.district_name} ({city.department_name})"
            )

    @api.model
    def _sifende_department_code(self, state):
        return DEPARTMENT_CODES.get(normalize(state.name)) if state else None

    @api.model
    def _sifende_resolve_name(self, state, city_name):
        # vacío si no hay una única ciudad; sin departamento busca en todo el país
        department = self._sifende_department_code(state)
        target = normalize(city_name)
        if not target or (state and not department):
            return self.browse()
        cities = self.search(
            [("department_code", "=", department)] if department else []
        )
        matches = cities.filtered(lambda city: normalize(city.name) == target)
        if len(matches) > 1:
            head = matches.filtered(
                lambda city: normalize(city.district_name) == target
            )
            matches = head or matches
        if (
            len(
                set(
                    zip(
                        matches.mapped("department_code"),
                        matches.mapped("district_code"),
                        strict=False,
                    )
                )
            )
            > 1
        ):
            return self.browse()
        return matches[:1]

    @api.model
    def _sifende_by_code(self, code):
        return self.search([("code", "=", code)], limit=1) if code else self.browse()

    def _sifende_ints(self):
        city = self[:1]
        return (city.department_code, city.district_code, city.code)

    def _sifende_codes(self):
        self.ensure_one()
        return {
            "departamento": self.department_code,
            "distrito": self.district_code,
            "ciudad": self.code,
        }

    @api.model
    def _sifende_check_codes(self, department, city):
        record = self._sifende_by_code(city)
        if not record:
            return self.env._(
                "la ciudad con código %(code)s no existe en el catálogo de SIFEN",
                code=city,
            )
        if department and record.department_code != department:
            return self.env._(
                "la ciudad %(city)s no pertenece al departamento %(department)s",
                city=record.display_name,
                department=department,
            )
        return None
