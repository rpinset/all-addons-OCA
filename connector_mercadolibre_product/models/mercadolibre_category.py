# Copyright 2026 Odoo Community Association (OCA)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MercadoLibreCategory(models.Model):
    _name = "mercadolibre.category"
    _description = "Mercado Libre Category"
    _parent_name = "parent_id"
    _parent_store = True
    _order = "name, id"

    backend_id = fields.Many2one(
        comodel_name="mercadolibre.backend",
        required=True,
        ondelete="cascade",
        index=True,
    )
    external_id = fields.Char(required=True, index=True)
    name = fields.Char()
    parent_external_id = fields.Char()
    parent_id = fields.Many2one(
        comodel_name="mercadolibre.category",
        index=True,
        ondelete="cascade",
    )
    parent_path = fields.Char(index=True)
    listing_allowed = fields.Boolean()
    attribute_schema = fields.Json(readonly=True)
    sync_date = fields.Datetime(readonly=True)

    _category_external_unique = models.Constraint(
        "UNIQUE(backend_id, external_id)",
        "This Mercado Libre category is already cached.",
    )

    @api.model
    def _upsert(self, backend, payload, parent=False):
        external_id = payload.get("id")
        category = self.search(
            [
                ("backend_id", "=", backend.id),
                ("external_id", "=", external_id),
            ],
            limit=1,
        )
        values = {
            "name": payload.get("name") or external_id,
            "listing_allowed": bool(payload.get("listing_allowed")),
            "parent_external_id": parent.external_id if parent else False,
            "parent_id": parent.id if parent else False,
            "sync_date": fields.Datetime.now(),
        }
        if category:
            category.write(values)
        else:
            values.update(
                {
                    "backend_id": backend.id,
                    "external_id": external_id,
                }
            )
            category = self.create(values)
        return category

    @api.model
    def _sync_nodes(self, backend, nodes, adapter, parent=False, seen=None):
        seen = seen if seen is not None else set()
        for node in nodes or []:
            external_id = node.get("id")
            if not external_id or external_id in seen:
                continue
            seen.add(external_id)
            detail = node
            if "children_categories" not in node or "listing_allowed" not in node:
                detail = adapter.read(f"/categories/{external_id}")
            category = self._upsert(backend, detail, parent=parent)
            if detail.get("listing_allowed"):
                category.attribute_schema = adapter.read(
                    f"/categories/{external_id}/attributes"
                )
            children = detail.get("children_categories") or []
            self._sync_nodes(
                backend,
                children,
                adapter,
                parent=category,
                seen=seen,
            )
