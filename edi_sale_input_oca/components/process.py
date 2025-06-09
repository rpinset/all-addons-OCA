# Copyright 2021 Camptocamp SA
# @author: Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


import logging

from odoo import _
from odoo.exceptions import UserError

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class EDIExchangeSOInput(Component):
    """Process sale orders."""

    _name = "edi.input.sale.order.process"
    _inherit = "edi.component.input.mixin"
    _usage = "input.process.sale.order"

    def __init__(self, work_context):
        super().__init__(work_context)
        self.settings = {}
        # Suppor legacy key `self.type_settings`
        for key in ("sale_order", "sale_order_import"):
            if key in self.type_settings:
                _logger.warning(
                    "Deprecated key %s for %s. "
                    "Please use default field values in env_ctx",
                    key,
                    self._usage,
                )
                self.settings = self.type_settings.get(key, {})
                break

    def process(self):
        wiz = self._setup_wizard()
        res = wiz.import_order_button()
        # TODO: log debug
        if wiz.state == "update" and wiz.sale_id:
            order = wiz.sale_id
            msg = self.msg_order_existing_error
            self._handle_existing_order(order, msg)
            raise UserError(msg)
        else:
            order = self._handle_create_order(res["res_id"])
            return self.msg_order_created % order.name

    @property
    def msg_order_existing_error(self):
        return _("Sales order has already been imported before")

    @property
    def msg_order_created(self):
        return _("Sales order %s created")

    def _setup_wizard(self):
        """Init a `sale.order.import` instance for current record."""
        # Set the right EDI origin on both order and lines
        edi_defaults = {"origin_exchange_record_id": self.exchange_record.id}
        addtional_ctx = dict(
            sale_order_import__default_vals=dict(order=edi_defaults, lines=edi_defaults)
        )
        wiz = (
            self.env["sale.order.import"]
            .with_context(**addtional_ctx)
            .sudo()
            .create({})
        )
        wiz.order_file = self.exchange_record._get_file_content(binary=False)
        wiz.order_filename = self.exchange_record.exchange_filename
        wiz.order_file_change()
        wiz.price_source = self._get_default_price_source()
        wiz.confirm_order = self._order_should_be_confirmed()
        return wiz

    # Deprecated: use default field values in env_ctx
    # as these settings are supported by sale_order_import model.
    def _get_default_price_source(self):
        return self.settings.get("price_source", "pricelist")

    # Deprecated: use default field values in env_ctx
    def _order_should_be_confirmed(self):
        return self.settings.get("confirm_order", False)

    def _handle_create_order(self, order_id):
        order = self.env["sale.order"].browse(order_id)
        self.exchange_record._set_related_record(order)
        return order

    def _handle_existing_order(self, order, message):
        # Hook
        pass
