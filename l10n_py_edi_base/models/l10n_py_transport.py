# l10n_py_edi_base/models/l10n_py_transport.py

from odoo import fields, models


class Transport(models.Model):
    """Datos de transporte de mercaderías (Grupo G SIFEN)."""

    _name = "l10n_py.transport"
    _description = "Transporte de Mercaderías"

    move_id = fields.Many2one(
        "account.move",
        string="Documento",
        required=True,
        ondelete="cascade",
    )

    transport_mode = fields.Selection(
        [
            ("1", "Terrestre"),
            ("2", "Fluvial"),
            ("3", "Aéreo"),
            ("4", "Multimodal"),
        ],
        string="Modalidad de Transporte (E901)",
        required=True,
        default="1",
    )

    transport_type = fields.Selection(
        [("1", "Propio"), ("2", "Tercero")],
        string="Tipo de Transporte (E903)",
    )

    freight_responsibility = fields.Selection(
        [
            ("1", "Emisor de la Factura Electrónica"),
            ("2", "Receptor de la Factura Electrónica"),
            ("3", "Tercero"),
            ("4", "Agente intermediario del transporte"),
        ],
        string="Responsable del Flete (E905)",
    )

    incoterm = fields.Selection(
        [
            ("CFR", "CFR"),
            ("CIF", "CIF"),
            ("CIP", "CIP"),
            ("CPT", "CPT"),
            ("DAP", "DAP"),
            ("DAT", "DAT"),
            ("DDP", "DDP"),
            ("EXW", "EXW"),
            ("FAS", "FAS"),
            ("FCA", "FCA"),
            ("FOB", "FOB"),
        ],
        string="Condición de Negociación (E906)",
    )

    manifest_number = fields.Char(
        string="Número de Manifiesto / Conocimiento (E907)",
    )

    transport_start_date = fields.Date(
        string="Fecha Inicio Transporte (E909)",
    )

    transport_end_date = fields.Date(
        string="Fecha Fin Transporte (E910)",
    )

    # Departure point (gCamSal)
    departure_address = fields.Char(
        string="Dirección de Salida (E920)",
    )
    departure_house = fields.Integer(
        string="Número de Casa Salida (E921)",
    )
    departure_department = fields.Integer(
        string="Departamento Salida (E924)",
    )
    departure_district = fields.Integer(
        string="Distrito Salida (E926)",
    )
    departure_city = fields.Integer(
        string="Ciudad Salida (E928)",
    )

    # Transporter data (gCamTrans)
    transporter_nature = fields.Selection(
        [("1", "Contribuyente"), ("2", "No contribuyente")],
        string="Naturaleza del Transportista (E940)",
    )
    transporter_name = fields.Char(
        string="Nombre del Transportista (E941)",
    )
    transporter_ruc = fields.Char(
        string="RUC del Transportista (E942)",
    )
    transporter_dv = fields.Char(
        string="DV del Transportista (E943)",
        size=1,
    )
    driver_doc_number = fields.Char(
        string="Doc. del Chofer (E950)",
    )
    driver_name = fields.Char(
        string="Nombre del Chofer (E951)",
    )

    # Related vehicles and deliveries
    vehicle_ids = fields.One2many(
        "l10n_py.transport.vehicle",
        "transport_id",
        string="Vehículos",
    )
    delivery_ids = fields.One2many(
        "l10n_py.transport.delivery",
        "transport_id",
        string="Entregas",
    )

    company_id = fields.Many2one(
        related="move_id.company_id",
        store=True,
    )


class TransportVehicle(models.Model):
    """Vehículo de transporte (gVehTras)."""

    _name = "l10n_py.transport.vehicle"
    _description = "Vehículo de Transporte"

    transport_id = fields.Many2one(
        "l10n_py.transport",
        string="Transporte",
        required=True,
        ondelete="cascade",
    )

    vehicle_type = fields.Char(
        string="Tipo de Vehículo (E960)",
        required=True,
    )
    brand = fields.Char(
        string="Marca (E961)",
        required=True,
    )
    plate_number = fields.Char(
        string="Número de Identificación (E962)",
        required=True,
    )


class TransportDelivery(models.Model):
    """Punto de entrega de mercaderías (gCamEnt)."""

    _name = "l10n_py.transport.delivery"
    _description = "Punto de Entrega"

    transport_id = fields.Many2one(
        "l10n_py.transport",
        string="Transporte",
        required=True,
        ondelete="cascade",
    )

    address = fields.Char(
        string="Dirección de Entrega (E930)",
        required=True,
    )
    house_number = fields.Integer(
        string="Número de Casa (E931)",
    )
    department = fields.Integer(
        string="Departamento (E934)",
        required=True,
    )
    district = fields.Integer(
        string="Distrito (E936)",
    )
    city = fields.Integer(
        string="Ciudad (E938)",
        required=True,
    )
