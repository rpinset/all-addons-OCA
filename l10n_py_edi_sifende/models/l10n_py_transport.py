# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

DOCUMENT_TYPES = [
    ("1", "Cédula paraguaya"),
    ("2", "Pasaporte"),
    ("3", "Cédula extranjera"),
    ("4", "Carnet de residencia"),
]


class Transport(models.Model):
    _inherit = "l10n_py.transport"

    # el diálogo de "Crear y editar" no conoce el documento; se enlaza al guardarlo
    move_id = fields.Many2one(required=False)
    freight_responsibility = fields.Selection(
        selection_add=[("5", "Transporte propio (E905)")]
    )
    sifende_transporter_document_type = fields.Selection(
        DOCUMENT_TYPES, string="Tipo de documento del transportista (E985)"
    )
    sifende_transporter_document_number = fields.Char(
        string="Documento del transportista (E987)", size=20
    )
    sifende_transporter_address = fields.Char(
        string="Domicilio fiscal del transportista (E992)", size=150
    )
    sifende_driver_address = fields.Char(string="Dirección del chofer (E993)", size=255)
    sifende_agent_name = fields.Char(string="Nombre del agente (E994)", size=60)
    sifende_agent_ruc = fields.Char(string="RUC del agente (E995)", size=8)
    sifende_agent_dv = fields.Char(string="DV del agente (E996)", size=1)
    sifende_agent_address = fields.Char(string="Dirección del agente (E997)", size=255)
    sifende_import_dispatch = fields.Char(
        string="Despacho de importación (E908)", size=16
    )
    sifende_departure_city_id = fields.Many2one(
        "l10n_py.sifende.city",
        string="Ciudad de salida",
        compute="_compute_sifende_departure_city_id",
        inverse="_inverse_sifende_departure_city_id",
    )

    # el transporte de un documento enviado es del documento: lo firmó SIFEN
    def _l10n_py_sifende_check_editable(self, moves=None, frozen=True):
        moves = (moves or self.env["account.move"]) | self.move_id
        referencing = (
            self.env["account.move"]
            .sudo()
            .search([("l10n_py_transport_id", "in", self.ids)])
        )
        moves |= self.env["account.move"].browse(referencing.ids)
        for move in moves:
            if not move._l10n_py_sifende_connector():
                continue
            move.check_access("write")
            if frozen and move._l10n_py_sifende_frozen():
                raise move._l10n_py_sifende_frozen_error(fiscal=True)

    @api.model_create_multi
    def create(self, vals_list):
        moves = self.env["account.move"].browse(
            [vals["move_id"] for vals in vals_list if vals.get("move_id")]
        )
        self.browse()._l10n_py_sifende_check_editable(moves)
        return super().create(vals_list)

    def write(self, vals):
        moves = self.env["account.move"].browse(vals.get("move_id"))
        adopting = set(vals) == {"move_id"} and not self.move_id
        self._l10n_py_sifende_check_editable(moves, frozen=not adopting)
        return super().write(vals)

    def unlink(self):
        self._l10n_py_sifende_check_editable()
        return super().unlink()

    @api.depends("departure_city")
    def _compute_sifende_departure_city_id(self):
        cities = self.env["l10n_py.sifende.city"]
        for transport in self:
            transport.sifende_departure_city_id = cities._sifende_by_code(
                transport.departure_city
            )

    def _inverse_sifende_departure_city_id(self):
        for transport in self:
            department, district, city = (
                transport.sifende_departure_city_id._sifende_ints()
            )
            transport.departure_department = department
            transport.departure_district = district
            transport.departure_city = city

    @api.depends(
        "move_id.name", "move_id.l10n_py_sifende_document_name", "transporter_name"
    )
    def _compute_display_name(self):
        for transport in self:
            move = transport.move_id
            parts = [
                move.l10n_py_sifende_document_name or move.name,
                transport.transporter_name,
            ]
            transport.display_name = " - ".join(p for p in parts if p) or self.env._(
                "Transporte nuevo"
            )


class TransportChild(models.AbstractModel):
    _name = "l10n_py.sifende.transport.child"
    _description = "Guarda de edición de los hijos del transporte"

    @api.model_create_multi
    def create(self, vals_list):
        transports = self.env["l10n_py.transport"].browse(
            [vals["transport_id"] for vals in vals_list if vals.get("transport_id")]
        )
        transports._l10n_py_sifende_check_editable()
        return super().create(vals_list)

    def write(self, vals):
        transports = self.transport_id | self.env["l10n_py.transport"].browse(
            vals.get("transport_id")
        )
        transports._l10n_py_sifende_check_editable()
        return super().write(vals)

    def unlink(self):
        self.transport_id._l10n_py_sifende_check_editable()
        return super().unlink()


class TransportVehicle(models.Model):
    _name = "l10n_py.transport.vehicle"
    _inherit = ["l10n_py.transport.vehicle", "l10n_py.sifende.transport.child"]

    sifende_flight_number = fields.Char(string="Número de vuelo (E967)", size=6)


class TransportDelivery(models.Model):
    _name = "l10n_py.transport.delivery"
    _inherit = ["l10n_py.transport.delivery", "l10n_py.sifende.transport.child"]

    # se completan desde la ciudad elegida, después del INSERT
    department = fields.Integer(required=False)
    city = fields.Integer(required=False)
    sifende_city_id = fields.Many2one(
        "l10n_py.sifende.city",
        string="Ciudad",
        compute="_compute_sifende_city_id",
        inverse="_inverse_sifende_city_id",
    )

    @api.depends("city")
    def _compute_sifende_city_id(self):
        cities = self.env["l10n_py.sifende.city"]
        for delivery in self:
            delivery.sifende_city_id = cities._sifende_by_code(delivery.city)

    def _inverse_sifende_city_id(self):
        for delivery in self:
            delivery.department, delivery.district, delivery.city = (
                delivery.sifende_city_id._sifende_ints()
            )
