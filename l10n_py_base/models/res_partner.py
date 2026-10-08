# l10n_py_base/models/res_partner.py

from odoo import api, fields, models

from ..validators.ruc_validator import RUCValidator


class ResPartner(models.Model):
    """Extensión de res.partner para Paraguay con campos fiscales"""

    _inherit = "res.partner"

    # ============== DEFAULT COUNTRY ==============

    country_id = fields.Many2one(
        comodel_name="res.country",
        default=lambda self: self._default_country_id(),
    )

    def _default_country_id(self):
        """Default country set to Paraguay if the current company is Paraguayan."""
        return (
            self.env.ref("base.py", raise_if_not_found=False)
            if self.env.company.country_id.code == "PY"
            else self.env["res.country"]
        )

    # ============== CAMPOS FISCALES PY ==============

    l10n_py_ruc = fields.Char(
        string="RUC",
        size=20,
        compute="_compute_l10n_py_ruc_fields",
        inverse="_inverse_l10n_py_ruc",
        store=True,
        help="Registro Único del Contribuyente (sin dígito verificador)",
    )

    l10n_py_ruc_dv = fields.Char(
        string="DV",
        size=1,
        compute="_compute_l10n_py_ruc_fields",
        store=True,
        help="Dígito verificador del RUC",
    )

    l10n_py_taxpayer_type = fields.Selection(
        [
            ("1", "Contribuyente"),
            ("2", "No Contribuyente"),
        ],
        string="Tipo de Contribuyente",
        help="Tipo de contribuyente según la SET",
    )

    l10n_py_fantasy_name = fields.Char(
        string="Nombre de Fantasía",
        help="Nombre comercial o de fantasía",
    )

    l10n_py_activity_description = fields.Char(
        string="Actividad Económica",
        help="Descripción de la actividad económica principal",
    )

    l10n_py_doc_type = fields.Selection(
        [
            ("1", "Cédula de Identidad"),
            ("2", "Pasaporte"),
            ("3", "Carnet de Residencia"),
            ("4", "Innominado"),
        ],
        string="Tipo de Documento de Identidad",
        help="Tipo de documento de identidad para no contribuyentes (SIFEN D024)",
    )

    l10n_py_doc_number = fields.Char(
        string="Número de Documento",
        size=20,
        help="Número de documento de identidad para no contribuyentes (SIFEN D025)",
    )

    # ============== CAMPOS DE UBICACIÓN (RELATED) ==============

    l10n_py_department_code = fields.Integer(
        string="Código Departamento SET",
        related="state_id.l10n_py_code",
        store=True,
        readonly=True,
        help="Código del departamento según SET",
    )

    l10n_py_city_code = fields.Char(
        string="Código Ciudad SET",
        related="city_id.l10n_py_code",
        store=True,
        readonly=True,
        help="Código de la ciudad según SET",
    )

    # ============== CAMPOS BARRIO ==============

    l10n_py_neighborhood_id = fields.Many2one(
        comodel_name="l10n_py.neighborhood",
        string="Barrio",
        domain="[('city_id', '=', city_id)]",
        help="Barrio o distrito del contacto",
    )

    l10n_py_neighborhood_name = fields.Char(
        string="Nombre del Barrio",
        related="l10n_py_neighborhood_id.name",
        store=True,
        readonly=True,
    )

    # ============== COMPUTE METHODS ==============

    def _l10n_py_is_ruc_partner(self):
        """Whether the tax number of the partner is a Paraguayan RUC.

        Odoo 20 removed ``l10n_latam_base`` and its identification types: the
        ``vat`` of a partner located in Paraguay is the RUC. Identity documents
        of non-taxpayers (CI, passport, residence card) live in
        ``l10n_py_doc_type`` and ``l10n_py_doc_number`` instead.
        """
        self.ensure_one()
        return bool(self.vat) and self.country_id == self.env.ref("base.py")

    @api.depends("vat", "country_id")
    def _compute_l10n_py_ruc_fields(self):
        """Compute l10n_py_ruc and l10n_py_ruc_dv from vat field."""
        for partner in self:
            if partner._l10n_py_is_ruc_partner():
                vat_clean = partner.vat.strip()
                if "-" in vat_clean:
                    parts = vat_clean.split("-", 1)
                    partner.l10n_py_ruc = parts[0]
                    partner.l10n_py_ruc_dv = parts[1]
                else:
                    ruc_num = "".join(c for c in vat_clean if c.isdigit())
                    partner.l10n_py_ruc = ruc_num
                    partner.l10n_py_ruc_dv = str(
                        RUCValidator._calculate_check_digit(ruc_num)
                    )
            else:
                partner.l10n_py_ruc = False
                partner.l10n_py_ruc_dv = False

    def _inverse_l10n_py_ruc(self):
        """When l10n_py_ruc is written directly, sync to vat field."""
        for partner in self:
            if partner.l10n_py_ruc:
                ruc_num = partner.l10n_py_ruc.strip()
                dv = str(RUCValidator._calculate_check_digit(ruc_num))
                partner.vat = f"{ruc_num}-{dv}"

    # ============== CREATE / WRITE ==============

    @api.model_create_multi
    def create(self, vals_list):
        country_py = self.env.ref("base.py")
        default_country_id = self._default_country_id().id
        for vals in vals_list:
            # Backward compat: convert l10n_py_ruc to vat
            if vals.get("l10n_py_ruc") and not vals.get("vat"):
                ruc_num = vals.pop("l10n_py_ruc").strip()
                dv = str(RUCValidator._calculate_check_digit(ruc_num))
                vals["vat"] = f"{ruc_num}-{dv}"
            country_id = vals.get("country_id", default_country_id)
            if vals.get("vat") and country_id == country_py.id:
                vals["vat"] = self._format_ruc(vals["vat"])
        return super().create(vals_list)

    def write(self, values):
        if "vat" in values or "country_id" in values:
            country_py = self.env.ref("base.py")
            for record in self:
                vat = values.get("vat", record.vat)
                country_id = values.get("country_id", record.country_id.id)
                if vat and country_id == country_py.id:
                    values["vat"] = self._format_ruc(vat)
        return super().write(values)

    @api.model
    def format_vat_py(self, vat):
        """Keep the RUC as typed instead of letting the core compact it.

        The core formats the VAT through ``format_vat_<cc>`` and falls back to
        the python-stdnum ``compact()``, which strips the hyphen of
        ``NNNNNNNN-D``. ``_format_ruc`` would then take the whole compacted
        number (check digit included) as the RUC base and append a new, wrong
        check digit.
        """
        return vat.strip() if vat else vat

    @api.model
    def _format_ruc(self, vat):
        """Return the RUC with its check digit (``NNNNNNNN-D``).

        The check digit is appended when missing and recomputed when informed.
        A value that is not a plain RUC number is returned untouched.
        """
        vat = vat.strip()
        if "-" in vat:
            ruc_num = vat.split("-", 1)[0]
        else:
            ruc_num = "".join(c for c in vat if c.isdigit())
        if ruc_num and ruc_num.isdigit() and len(ruc_num) >= 6:
            dv = str(RUCValidator._calculate_check_digit(ruc_num))
            return f"{ruc_num}-{dv}"
        return vat

    # ============== ONCHANGE METHODS ==============

    @api.onchange("l10n_py_doc_type")
    def _onchange_l10n_py_doc_type(self):
        """A partner identified by an identity document is a non-taxpayer."""
        if self.l10n_py_doc_type:
            self.l10n_py_taxpayer_type = "2"

    @api.onchange("vat", "country_id")
    def _onchange_vat_l10n_py(self):
        """When the RUC changes, auto-format it with the check digit."""
        if self._l10n_py_is_ruc_partner():
            self.vat = self._format_ruc(self.vat)
            self.l10n_py_taxpayer_type = "1"
            self.l10n_py_doc_type = False
            self.l10n_py_doc_number = False

    @api.onchange("l10n_py_neighborhood_id")
    def _onchange_l10n_py_neighborhood_id(self):
        """Actualizar ciudad y código postal cuando cambia el barrio"""
        if self.l10n_py_neighborhood_id:
            if not self.city_id:
                self.city_id = self.l10n_py_neighborhood_id.city_id
            if not self.zip and self.l10n_py_neighborhood_id.zipcode:
                self.zip = self.l10n_py_neighborhood_id.zipcode

    @api.onchange("city_id")
    def _onchange_city_id(self):
        """Limpiar barrio si cambia la ciudad y no coincide"""
        if (
            self.l10n_py_neighborhood_id
            and self.city_id
            and self.l10n_py_neighborhood_id.city_id != self.city_id
        ):
            self.l10n_py_neighborhood_id = False

    @api.onchange("state_id")
    def _onchange_state_id_l10n_py(self):
        """Limpiar ciudad y barrio si cambia el departamento y no coinciden"""
        if self.state_id:
            if self.city_id and self.city_id.state_id != self.state_id:
                self.city_id = False
                self.l10n_py_neighborhood_id = False
            elif self.l10n_py_neighborhood_id:
                nb_state = self.l10n_py_neighborhood_id.city_id.state_id
                if nb_state != self.state_id:
                    self.l10n_py_neighborhood_id = False

    @api.onchange("zip")
    def _onchange_zip_l10n_py(self):
        """Buscar barrio por código postal y auto-completar ubicación"""
        if self.zip and self.country_id and self.country_id.code == "PY":
            zipcode = self.zip.strip()
            # Buscar match exato primeiro, depois por zipcode padded com zeros
            neighborhood = self.env["l10n_py.neighborhood"].search(
                [("zipcode", "=", zipcode)], limit=1
            )
            if not neighborhood:
                # Tentar com padding (ex: "1001" → "001001")
                zipcode_padded = zipcode.zfill(6)
                neighborhood = self.env["l10n_py.neighborhood"].search(
                    [("zipcode", "=", zipcode_padded)], limit=1
                )
            if not neighborhood:
                # Tentar busca por prefixo (ex: "1001" encontra "001001")
                neighborhood = self.env["l10n_py.neighborhood"].search(
                    [("zipcode", "=like", f"%{zipcode}")], limit=1
                )
            if neighborhood:
                self.l10n_py_neighborhood_id = neighborhood
                self.city_id = neighborhood.city_id
                self.state_id = neighborhood.city_id.state_id

    # ============== VAT VALIDATION ==============

    def check_vat_py(self, vat):
        """Validate a Paraguayan RUC, check digit included.

        The core calls this hook for the ``vat`` of partners located in
        Paraguay.
        """
        if not vat:
            return False
        return RUCValidator.validate(vat)[0]

    @api.model
    def _formatting_address_fields(self):
        """Returns the list of address fields usable to format addresses."""
        return super()._formatting_address_fields() + ["l10n_py_neighborhood_name"]
