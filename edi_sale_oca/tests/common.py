# Copyright 2022 Camptocamp SA
# @author: Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.fields import Domain

from odoo.addons.edi_core_oca.tests.common import EDIBackendTestMixin


class SaleEDIBackendTestMixin(EDIBackendTestMixin):
    @classmethod
    def _get_backend_type(cls):
        backend_type = cls.env["edi.backend.type"].search(
            Domain([("code", "=", "sale_demo")]), limit=1
        )
        if backend_type:
            return backend_type
        return cls.env["edi.backend.type"].create(
            {"name": "Sale DEMO", "code": "sale_demo"}
        )

    @classmethod
    def _get_backend(cls):
        backend_type = cls._get_backend_type()
        backend = cls.env["edi.backend"].search(
            Domain([("backend_type_id", "=", backend_type.id)]), limit=1
        )
        if backend:
            return backend
        return cls.env["edi.backend"].create(
            {"name": "Sale DEMO", "backend_type_id": backend_type.id}
        )

    @classmethod
    def _create_exchange_type(cls, **kw):
        model = cls.env["edi.exchange.type"]
        code = kw.get("code")
        if code:
            exchange_type = model.search(
                Domain([("code", "=", code), ("backend_id", "=", cls.backend.id)]),
                limit=1,
            )
            if exchange_type:
                return exchange_type
        return super()._create_exchange_type(**kw)


class OrderMixin:
    @classmethod
    def _setup_order_records(cls):
        cls.sale_partner = cls.env["res.partner"].create({"name": "Test Sale Customer"})
        cls.product_a = cls.env["product.product"].create(
            {"name": "Product A", "sale_ok": True, "barcode": "1" * 14}
        )
        cls.product_b = cls.env["product.product"].create(
            {"name": "Product B", "sale_ok": True, "barcode": "2" * 14}
        )
        cls.product_c = cls.env["product.product"].create(
            {"name": "Product C", "sale_ok": True, "barcode": "3" * 14}
        )
        cls.product_d = cls.env["product.product"].create(
            {"name": "Product D", "sale_ok": True, "barcode": "4" * 14}
        )

    @classmethod
    def _create_sale_order(cls, **kw):
        model = cls.env["sale.order"]
        vals = dict(commitment_date=fields.Date.today())
        vals.update(kw)
        # Loose dependency on onchange_helper
        if hasattr(model, "play_onchanges"):
            so_vals = model.play_onchanges(vals, [])
        else:
            so_vals = vals.copy()
        if "order_line" in so_vals:
            so_vals["order_line"] = [(0, 0, x) for x in vals["order_line"]]
        return model.create(so_vals)

    @classmethod
    def _setup_order(cls, **kw):
        line_defaults = kw.pop("line_defaults", {})
        vals = {
            "partner_id": cls.sale_partner.id,
            "commitment_date": "2022-07-29",
        }
        vals.update(kw)
        if "client_order_ref" not in vals:
            vals["client_order_ref"] = "ABC123"
        vals["order_line"] = [
            {"product_id": cls.product_a.id, "product_uom_qty": 300, "edi_id": 1000},
            {"product_id": cls.product_b.id, "product_uom_qty": 200, "edi_id": 2000},
            {"product_id": cls.product_c.id, "product_uom_qty": 100, "edi_id": 3000},
        ]
        if line_defaults:
            for line in vals["order_line"]:
                line.update(line_defaults)
        sale = cls._create_sale_order(**vals)
        sale.action_confirm()
        return sale
