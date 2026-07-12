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
            else False
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

    @api.depends("vat", "l10n_latam_identification_type_id")
    def _compute_l10n_py_ruc_fields(self):
        """Compute l10n_py_ruc and l10n_py_ruc_dv from vat field."""
        ruc_type = self.env.ref("l10n_py_base.it_ruc", raise_if_not_found=False)
        for partner in self:
            if (
                ruc_type
                and partner.l10n_latam_identification_type_id == ruc_type
                and partner.vat
            ):
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
        ruc_type = self.env.ref("l10n_py_base.it_ruc", raise_if_not_found=False)
        for partner in self:
            if partner.l10n_py_ruc:
                ruc_num = partner.l10n_py_ruc.strip()
                dv = str(RUCValidator._calculate_check_digit(ruc_num))
                partner.vat = f"{ruc_num}-{dv}"
                if ruc_type:
                    partner.l10n_latam_identification_type_id = ruc_type

    # ============== CREATE / WRITE ==============

    @api.model_create_multi
    def create(self, vals_list):
        ruc_type = self.env.ref("l10n_py_base.it_ruc", raise_if_not_found=False)
        for vals in vals_list:
            # Backward compat: convert l10n_py_ruc to vat + identification type
            if vals.get("l10n_py_ruc") and not vals.get("vat"):
                ruc_num = vals.pop("l10n_py_ruc").strip()
                dv = str(RUCValidator._calculate_check_digit(ruc_num))
                vals["vat"] = f"{ruc_num}-{dv}"
                if ruc_type:
                    vals.setdefault("l10n_latam_identification_type_id", ruc_type.id)
            self._format_vat_py(vals)
        return super().create(vals_list)

    def write(self, values):
        if any(
            f in values
            for f in ["vat", "l10n_latam_identification_type_id", "country_id"]
        ):
            for record in self:
                vat_values = {
                    "vat": values.get("vat", record.vat),
                    "l10n_latam_identification_type_id": values.get(
                        "l10n_latam_identification_type_id",
                        record.l10n_latam_identification_type_id.id,
                    ),
                    "country_id": values.get("country_id", record.country_id.id),
                }
                formatted = self._format_vat_py(vat_values)
                if formatted:
                    values["vat"] = formatted
        return super().write(values)

    def _format_vat_py(self, vals):
        """Format vat for RUC type: append DV if missing or incorrect.

        For create: modifies vals in-place.
        For write: returns formatted vat or None.
        """
        ruc_type = self.env.ref("l10n_py_base.it_ruc", raise_if_not_found=False)
        if not ruc_type or not vals.get("vat"):
            return None

        id_type_id = vals.get("l10n_latam_identification_type_id")
        if isinstance(id_type_id, int):
            is_ruc = id_type_id == ruc_type.id
        else:
            is_ruc = False

        if not is_ruc:
            return None

        vat = vals["vat"].strip()
        if "-" in vat:
            ruc_num = vat.split("-", 1)[0]
        else:
            ruc_num = "".join(c for c in vat if c.isdigit())

        if ruc_num and ruc_num.isdigit() and len(ruc_num) >= 6:
            dv = str(RUCValidator._calculate_check_digit(ruc_num))
            formatted = f"{ruc_num}-{dv}"
            vals["vat"] = formatted
            return formatted

        return None

    # ============== ONCHANGE METHODS ==============

    @api.onchange("l10n_latam_identification_type_id")
    def _onchange_l10n_py_identification_type(self):
        """Auto-set taxpayer type and doc_type based on identification type."""
        ruc_type = self.env.ref("l10n_py_base.it_ruc", raise_if_not_found=False)
        if not self.l10n_latam_identification_type_id:
            return

        if self.l10n_latam_identification_type_id == ruc_type:
            self.l10n_py_taxpayer_type = "1"
            self.l10n_py_doc_type = False
            self.l10n_py_doc_number = False
        else:
            type_map = self._get_identification_doc_type_map()
            doc_type = type_map.get(self.l10n_latam_identification_type_id.id)
            if doc_type:
                self.l10n_py_taxpayer_type = "2"
                self.l10n_py_doc_type = doc_type
                if self.vat:
                    self.l10n_py_doc_number = self.vat

    @api.onchange("vat")
    def _onchange_vat_l10n_py(self):
        """When vat changes for RUC type, auto-format with DV."""
        ruc_type = self.env.ref("l10n_py_base.it_ruc", raise_if_not_found=False)
        if ruc_type and self.l10n_latam_identification_type_id == ruc_type and self.vat:
            vat = self.vat.strip()
            if "-" in vat:
                ruc_num = vat.split("-", 1)[0]
            else:
                ruc_num = "".join(c for c in vat if c.isdigit())

            if ruc_num and ruc_num.isdigit() and len(ruc_num) >= 6:
                dv = str(RUCValidator._calculate_check_digit(ruc_num))
                self.vat = f"{ruc_num}-{dv}"
        elif self.vat and self.l10n_latam_identification_type_id:
            # Sync doc_number for non-RUC types
            type_map = self._get_identification_doc_type_map()
            if self.l10n_latam_identification_type_id.id in type_map:
                self.l10n_py_doc_number = self.vat

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
        """Validate Paraguay RUC/VAT number.

        Accepts formats: XXXXXXXX-D (RUC with DV) or any identification number.
        """
        if not vat:
            return False
        # Accept RUC format: digits with optional dash and DV
        clean = vat.replace("-", "").replace(" ", "")
        if clean.isdigit() and 6 <= len(clean) <= 9:
            # Validate DV if present
            if "-" in vat:
                parts = vat.split("-", 1)
                if len(parts) == 2 and parts[1].isdigit():
                    expected_dv = str(RUCValidator._calculate_check_digit(parts[0]))
                    return parts[1] == expected_dv
            return True
        # Accept non-numeric identification (passport, etc.)
        if len(vat) >= 1:
            return True
        return False

    # ============== HELPER METHODS ==============

    def _get_identification_doc_type_map(self):
        """Map identification type IDs to l10n_py_doc_type selection values."""
        result = {}
        for xml_id, doc_type in [
            ("l10n_py_base.it_ci", "1"),
            ("l10n_py_base.it_pasaporte", "2"),
            ("l10n_py_base.it_carnet_residencia", "3"),
        ]:
            rec = self.env.ref(xml_id, raise_if_not_found=False)
            if rec:
                result[rec.id] = doc_type
        return result

    @api.model
    def _formatting_address_fields(self):
        """Returns the list of address fields usable to format addresses."""
        return super()._formatting_address_fields() + ["l10n_py_neighborhood_name"]
