# Copyright 2026 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields
from odoo.fields import Command

from odoo.addons.edi_core_oca.tests.common import EDIBackendTestMixin


class PurchaseEDIBackendTestMixin(EDIBackendTestMixin):
    @classmethod
    def _get_backend_type(cls):
        backend_type = cls.env["edi.backend.type"].search(
            [("code", "=", "purchase_demo")], limit=1
        )
        if backend_type:
            return backend_type
        return cls.env["edi.backend.type"].create(
            {
                "name": "Purchase DEMO",
                "code": "purchase_demo",
            }
        )

    @classmethod
    def _get_backend(cls):
        backend_type = cls._get_backend_type()
        backend = cls.env["edi.backend"].search(
            [("backend_type_id", "=", backend_type.id)], limit=1
        )
        if backend:
            return backend
        return cls.env["edi.backend"].create(
            {
                "name": "purchase DEMO",
                "backend_type_id": backend_type.id,
            }
        )

    @classmethod
    def _create_exchange_type(cls, **kw):
        model = cls.env["edi.exchange.type"]
        code = kw.get("code")
        if code:
            exchange_type = model.search(
                [("code", "=", code), ("backend_id", "=", cls.backend.id)], limit=1
            )
            if exchange_type:
                return exchange_type
        return super()._create_exchange_type(**kw)


class OrderMixin:
    @classmethod
    def _create_purchase_order(cls, **kw):
        model = cls.env["purchase.order"]
        vals = {
            "partner_id": cls.vendor.id,
            "user_id": cls.env.ref("base.user_admin").id,
            "date_planned": fields.Datetime.now(),
        }
        vals.update(kw)
        if hasattr(model, "play_onchanges"):
            po_vals = model.play_onchanges(vals, [])
        else:
            po_vals = vals.copy()
        if "order_line" in vals:
            po_vals["order_line"] = [Command.create(x) for x in vals["order_line"]]
        return model.create(po_vals)

    @classmethod
    def _setup_order_records(cls):
        cls.vendor = cls.env["res.partner"].create(
            {"name": "ACME inc", "country_id": cls.env.company.country_id.id}
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Product 1",
                "default_code": "1234567",
                "purchase_ok": True,
            }
        )
