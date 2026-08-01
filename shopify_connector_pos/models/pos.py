from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Command

from odoo.addons.shopify_connector.models.order_sync import ShopifyOrderImportError

from ..lib.pos import (
    adjusted_pos_total,
    exchange_origin_gid,
    selected_cash_rounding,
)


class ShopifyInstancePosConfiguration(models.Model):
    _inherit = "shopify.instance"

    pos_enabled = fields.Boolean(
        string="Import Shopify POS Orders",
        default=False,
    )
    pos_auto_confirm = fields.Boolean(
        string="Confirm POS Orders",
        default=True,
    )
    pos_auto_fulfill = fields.Boolean(
        string="Validate POS Deliveries",
        default=True,
    )
    pos_rounding_product_id = fields.Many2one(
        "product.product",
        string="Cash Rounding Product",
        check_company=True,
        ondelete="restrict",
    )
    pos_rounding_account_id = fields.Many2one(
        "account.account",
        string="Cash Rounding Account",
        check_company=True,
        ondelete="restrict",
    )

    @api.constrains(
        "company_id",
        "pos_rounding_product_id",
        "pos_rounding_account_id",
    )
    def _check_pos_rounding_configuration(self):
        for instance in self:
            product = instance.pos_rounding_product_id
            account = instance.pos_rounding_account_id
            if (
                product
                and product.company_id
                and product.company_id != instance.company_id
            ):
                raise ValidationError(
                    self.env._(
                        "The POS rounding product must belong to the instance company."
                    )
                )
            if product and product.type != "service":
                raise ValidationError(
                    self.env._("The POS rounding product must be a service product.")
                )
            if (
                account
                and account.company_ids
                and instance.company_id not in account.company_ids
            ):
                raise ValidationError(
                    self.env._(
                        "The POS rounding account must be available to the company."
                    )
                )
            if product and account:
                effective = (
                    product.with_company(instance.company_id).property_account_income_id
                    or product.categ_id.with_company(
                        instance.company_id
                    ).property_account_income_categ_id
                )
                if effective != account:
                    raise ValidationError(
                        self.env._(
                            "The POS rounding product's effective income account "
                            "must match the configured rounding account."
                        )
                    )


class ShopifyLocationPosConfiguration(models.Model):
    _inherit = "shopify.location"

    pos_warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="POS Warehouse Override",
        check_company=True,
        ondelete="restrict",
        help=(
            "Optional warehouse used for POS orders. The inventory warehouse "
            "mapping is used when this is empty."
        ),
    )

    @api.constrains("instance_id", "pos_warehouse_id")
    def _check_pos_warehouse_company(self):
        for location in self.filtered("pos_warehouse_id"):
            if location.pos_warehouse_id.company_id != location.instance_id.company_id:
                raise ValidationError(
                    self.env._("The POS warehouse must belong to the instance company.")
                )


class ShopifyOrderPosBinding(models.Model):
    _inherit = "shopify.order"

    pos_location_id = fields.Many2one(
        "shopify.location",
        string="Shopify POS Location",
        readonly=True,
        ondelete="set null",
    )
    cash_rounding_amount = fields.Char(readonly=True)
    exchange_origin_shopify_id = fields.Char(
        string="Original Exchange Order GID",
        readonly=True,
        index=True,
    )
    exchange_origin_id = fields.Many2one(
        "shopify.order",
        string="Original Exchange Order",
        readonly=True,
        ondelete="set null",
    )
    exchange_order_ids = fields.One2many(
        "shopify.order",
        "exchange_origin_id",
        string="Exchange Orders",
        readonly=True,
    )

    @api.constrains(
        "instance_id",
        "pos_location_id",
        "exchange_origin_id",
    )
    def _check_pos_binding_scope(self):
        for binding in self:
            if (
                binding.pos_location_id
                and binding.pos_location_id.instance_id != binding.instance_id
            ):
                raise ValidationError(
                    self.env._(
                        "The POS location must use the order's Shopify instance."
                    )
                )
            if (
                binding.exchange_origin_id
                and binding.exchange_origin_id.instance_id != binding.instance_id
            ):
                raise ValidationError(
                    self.env._("Exchange orders must use one Shopify instance.")
                )

    def _route_shopify_pos_order(self, binding, instance, order_data, digest):
        if not instance.pos_enabled:
            return super()._route_shopify_pos_order(
                binding, instance, order_data, digest
            )
        return self._process_shopify_order(binding, instance, order_data, digest)

    def _pos_location(self, instance, order_data):
        location_id = order_data.get("retail_location_id")
        if not location_id:
            raise ShopifyOrderImportError(
                self.env._("The Shopify POS order has no retail location.")
            )
        location = self.env["shopify.location"].search(
            [
                ("instance_id", "=", instance.id),
                ("shopify_id", "=", location_id),
                ("active", "=", True),
            ],
            limit=1,
        )
        if not location:
            raise ShopifyOrderImportError(
                self.env._(
                    "No Shopify location mapping matches POS location %s.", location_id
                )
            )
        warehouse = location.pos_warehouse_id or location.warehouse_id
        if not warehouse:
            raise ShopifyOrderImportError(
                self.env._("Map POS location %s to an Odoo warehouse.", location.name)
            )
        return location, warehouse

    def _shopify_order_extra_values(self, instance, order_data):
        values = super()._shopify_order_extra_values(instance, order_data)
        if order_data["source"] != "pos":
            return values
        _location, warehouse = self._pos_location(instance, order_data)
        return {
            **values,
            "warehouse_id": warehouse.id,
            "shopify_pos_order": True,
        }

    def _apply_lines(self, binding, sale_order, instance, order_data):
        result = super()._apply_lines(binding, sale_order, instance, order_data)
        if order_data["source"] == "pos":
            self._sync_cash_rounding_line(sale_order, instance, order_data)
        return result

    def _sync_cash_rounding_line(self, sale_order, instance, order_data):
        amount = selected_cash_rounding(
            order_data,
            use_presentment=(instance.order_currency_policy == "presentment"),
        )
        line = sale_order.order_line.filtered("shopify_pos_rounding")[:1]
        if not amount:
            line.unlink()
            return
        product = instance.pos_rounding_product_id
        account = instance.pos_rounding_account_id
        if not product or not account:
            raise ShopifyOrderImportError(
                self.env._(
                    "Configure the POS cash-rounding product and account "
                    "before importing rounded cash orders."
                )
            )
        if product.type != "service":
            raise ShopifyOrderImportError(
                self.env._("The POS cash-rounding product must be a service product.")
            )
        effective = (
            product.with_company(instance.company_id).property_account_income_id
            or product.categ_id.with_company(
                instance.company_id
            ).property_account_income_categ_id
        )
        if effective != account:
            raise ShopifyOrderImportError(
                self.env._(
                    "The POS cash-rounding product does not use the configured "
                    "rounding account."
                )
            )
        values = {
            "order_id": sale_order.id,
            "product_id": product.id,
            "name": self.env._("Shopify POS cash rounding"),
            "product_uom_qty": 1,
            "product_uom_id": product.uom_id.id,
            "price_unit": format(amount, "f"),
            "tax_ids": [Command.clear()],
            "shopify_pos_rounding": True,
        }
        if line:
            line.with_context(shopify_order_import=True).write(values)
        else:
            self.env["sale.order.line"].with_context(shopify_order_import=True).create(
                values
            )

    def _shopify_expected_order_total(self, instance, order_data):
        if order_data["source"] != "pos":
            return super()._shopify_expected_order_total(instance, order_data)
        return format(
            adjusted_pos_total(
                order_data,
                use_presentment=(instance.order_currency_policy == "presentment"),
            ),
            "f",
        )

    def _should_confirm_shopify_order(self, instance, order_data, sale_order):
        if order_data["source"] == "pos":
            return (
                instance.pos_auto_confirm
                and not order_data["cancelled_at"]
                and sale_order.state in ("draft", "sent")
            )
        return super()._should_confirm_shopify_order(instance, order_data, sale_order)

    def _apply_state(self, binding, sale_order, order_data):
        result = super()._apply_state(binding, sale_order, order_data)
        instance = binding.instance_id
        if (
            order_data["source"] == "pos"
            and instance.pos_auto_fulfill
            and sale_order.state in ("sale", "done")
            and not order_data["cancelled_at"]
        ):
            self._validate_pos_deliveries(sale_order)
        return result

    def _validate_pos_deliveries(self, sale_order):
        pickings = sale_order.picking_ids.filtered(
            lambda picking: (
                picking.state not in ("done", "cancel")
                and picking.picking_type_id.code == "outgoing"
            )
        )
        for picking in pickings:
            picking.action_assign()
            for move in picking.move_ids.filtered(
                lambda item: item.state not in ("done", "cancel")
            ):
                move.quantity = move.product_uom_qty
            picking.with_context(skip_shopify_fulfillment_push=True).button_validate()
            if picking.state != "done":
                raise ShopifyOrderImportError(
                    self.env._(
                        "POS delivery %s still requires manual validation.",
                        picking.name,
                    )
                )

    def _write_success(self, binding, sale_order, order_data, digest):
        result = super()._write_success(binding, sale_order, order_data, digest)
        if order_data["source"] != "pos":
            return result
        location, _warehouse = self._pos_location(binding.instance_id, order_data)
        origin_gid = exchange_origin_gid(order_data.get("raw") or {})
        origin = (
            self.search(
                [
                    ("instance_id", "=", binding.instance_id.id),
                    ("shopify_id", "=", origin_gid),
                ],
                limit=1,
            )
            if origin_gid
            else self.env["shopify.order"]
        )
        binding.write(
            {
                "pos_location_id": location.id,
                "cash_rounding_amount": format(
                    selected_cash_rounding(
                        order_data,
                        use_presentment=(
                            binding.instance_id.order_currency_policy == "presentment"
                        ),
                    ),
                    "f",
                ),
                "exchange_origin_shopify_id": origin_gid or False,
                "exchange_origin_id": origin.id,
            }
        )
        self.search(
            [
                ("instance_id", "=", binding.instance_id.id),
                ("exchange_origin_shopify_id", "=", binding.shopify_id),
                ("exchange_origin_id", "=", False),
            ]
        ).write({"exchange_origin_id": binding.id})
        return result


class SaleOrderPosSource(models.Model):
    _inherit = "sale.order"

    shopify_pos_order = fields.Boolean(
        string="Shopify POS Order",
        readonly=True,
        copy=False,
        index=True,
    )


class SaleOrderLinePosRounding(models.Model):
    _inherit = "sale.order.line"

    shopify_pos_rounding = fields.Boolean(
        string="Shopify POS Cash Rounding",
        readonly=True,
        copy=False,
        index=True,
    )
