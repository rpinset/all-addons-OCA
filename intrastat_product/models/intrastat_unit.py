# Copyright 2011-2020 Akretion (http://www.akretion.com)
# Copyright 2009-2020 Noviat (http://www.noviat.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Luc de Meyer <info@noviat.com>

from odoo import fields, models


class IntrastatUnit(models.Model):
    _name = "intrastat.unit"
    _description = "Intrastat Supplementary Units"
    _order = "name"

    name = fields.Char(required=True)
    description = fields.Char(required=True)
    uom_id = fields.Many2one(
        comodel_name="uom.uom",
        string="Regular UoM",
        help="Select the regular Unit of Measure of Odoo that corresponds "
        "to this Intrastat Supplementary Unit.",
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name)",
            "An intrastat supplementary unit with the same name already exists!",
        )
    ]
