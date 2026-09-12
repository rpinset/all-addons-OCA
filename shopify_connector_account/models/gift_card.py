from decimal import Decimal

from odoo import fields, models
from odoo.fields import Command

from odoo.addons.shopify_connector.models.order_sync import ShopifyOrderImportError


class ShopifyOrderGiftCardAccounting(models.Model):
    _inherit = "shopify.order"

    def _after_shopify_gateway_payment(self, gateway_payment, transaction, invoice):
        result = super()._after_shopify_gateway_payment(
            gateway_payment, transaction, invoice
        )
        gateway = str(gateway_payment.gateway or "").strip().lower()
        if (
            gateway not in ("gift_card", "gift card")
            or gateway_payment.gift_card_move_id
        ):
            return result
        instance = gateway_payment.instance_id
        liability_account = instance.gift_card_liability_account_id
        if not liability_account or liability_account.account_type not in (
            "liability_current",
            "liability_non_current",
        ):
            raise ShopifyOrderImportError(
                self.env._(
                    "Configure the gift-card product income account as its "
                    "liability account before importing gift-card payments."
                )
            )
        payment = gateway_payment.payment_id
        clearing_line = payment.move_id.line_ids.filtered(
            lambda line: (
                line.account_id.account_type
                not in ("asset_receivable", "liability_payable")
                and line.balance
            )
        )[:1]
        if not clearing_line:
            raise ShopifyOrderImportError(
                self.env._("The gift-card payment has no clearing line to reclassify.")
            )
        balance = abs(Decimal(str(clearing_line.balance)))
        move = self.env["account.move"].create(
            {
                "move_type": "entry",
                "journal_id": payment.journal_id.id,
                "company_id": instance.company_id.id,
                "date": payment.date or fields.Date.today(),
                "ref": self.env._(
                    "Gift card redemption %(transaction)s",
                    transaction=gateway_payment.transaction_shopify_id,
                ),
                "line_ids": [
                    Command.create(
                        {
                            "name": self.env._("Shopify gift card redemption"),
                            "account_id": liability_account.id,
                            "debit": float(balance),
                            "credit": 0.0,
                        }
                    ),
                    Command.create(
                        {
                            "name": self.env._("Shopify gift card clearing"),
                            "account_id": clearing_line.account_id.id,
                            "debit": 0.0,
                            "credit": float(balance),
                        }
                    ),
                ],
            }
        )
        gateway_payment.gift_card_move_id = move
        instance._write_log(
            entity="gift_card",
            direction="import",
            level="info",
            message=self.env._(
                "Created draft gift-card liability entry %s.", move.display_name
            ),
            record=gateway_payment,
        )
        return result
