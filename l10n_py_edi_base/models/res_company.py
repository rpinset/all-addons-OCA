# l10n_py_edi_base/models/res_company.py

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    # ============== CAMPOS EDI PARAGUAY ==============

    l10n_py_ruc = fields.Char(
        string="RUC",
        size=8,
        help="Registro Único del Contribuyente sin dígito verificador",
    )

    l10n_py_dv = fields.Char(
        string="DV",
        size=1,
        compute="_compute_dv",
        store=True,
        help="Dígito Verificador del RUC",
    )

    l10n_py_ruc_full = fields.Char(
        string="RUC Completo",
        compute="_compute_ruc_full",
        store=True,
        help="RUC con dígito verificador",
    )

    l10n_py_trade_name = fields.Char(
        string="Nombre Fantasía",
        help="Nombre comercial o de fantasía de la empresa",
    )

    l10n_py_economic_activity_code = fields.Char(
        string="Código Actividad Económica",
        size=8,
        help="Código de actividad económica principal según SET",
    )

    l10n_py_economic_activity = fields.Char(
        string="Descripción Actividad Económica",
        help="Descripción de la actividad económica principal",
    )

    # ============== CAMPOS DE UBICACIÓN (RELACIONADOS) ==============

    l10n_py_department_code = fields.Integer(
        string="Código Departamento SET",
        related="partner_id.l10n_py_department_code",
        store=True,
        readonly=True,
        help="Código del departamento según SET",
    )

    l10n_py_district_code = fields.Integer(
        string="Código Distrito SET",
        help="Código del distrito según SET",
    )

    l10n_py_city_code = fields.Char(
        string="Código Ciudad SET",
        related="partner_id.l10n_py_city_code",
        store=True,
        readonly=True,
        help="Código de la ciudad según SET",
    )

    # ============== COMPUTE METHODS ==============

    @api.depends("l10n_py_ruc")
    def _compute_dv(self):
        """Calcular dígito verificador del RUC"""
        for company in self:
            if company.l10n_py_ruc:
                company.l10n_py_dv = self._calculate_dv(company.l10n_py_ruc)
            else:
                company.l10n_py_dv = False

    @api.depends("l10n_py_ruc", "l10n_py_dv")
    def _compute_ruc_full(self):
        """Calcular RUC completo con DV"""
        for company in self:
            if company.l10n_py_ruc and company.l10n_py_dv:
                company.l10n_py_ruc_full = f"{company.l10n_py_ruc}-{company.l10n_py_dv}"
            else:
                company.l10n_py_ruc_full = False

    # ============== PRIVATE METHODS ==============

    @staticmethod
    def _calculate_dv(ruc):
        """Calcular dígito verificador del RUC paraguayo (Módulo 11 SET)

        Algoritmo:
        1. Pad RUC a 9 dígitos con ceros a la izquierda
        2. Aplicar pesos [2,3,4,5,6,7,8,9] cíclicamente de izquierda a derecha
        3. Encontrar DV (0-9) tal que la suma ponderada total mod 11 == 0
        """
        if not ruc or not ruc.isdigit():
            return False

        ruc = ruc.replace("-", "").strip()

        if len(ruc) < 6:
            return False

        weights = [2, 3, 4, 5, 6, 7, 8, 9]
        ruc_padded = ruc.zfill(9)

        partial_sum = 0
        for i, digit in enumerate(ruc_padded):
            partial_sum += int(digit) * weights[i % 8]

        # DV en posición 9 tiene peso = weights[9 % 8] = weights[1] = 3
        # Encontrar DV tal que (partial_sum + DV * 3) % 11 == 0
        # Inverso modular: inv(3, 11) = 4
        remainder = partial_sum % 11
        dv = ((11 - remainder) % 11 * 4) % 11

        if dv >= 10:
            dv = 0

        return str(dv)
