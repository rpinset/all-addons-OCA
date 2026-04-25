/** @odoo-module **/

/*
    Copyright (C) 2024 - Today: GRAP (http://www.grap.coop)
    @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/

import NumberBuffer from "point_of_sale.NumberBuffer";
import ProductScreen from "point_of_sale.ProductScreen";
import Registries from "point_of_sale.Registries";
import {useBarcodeReader} from "point_of_sale.custom_hooks";

const PosPriceToWeightProductScreen = (OriginalProductScreen) =>
    class extends OriginalProductScreen {
        setup() {
            super.setup();
            useBarcodeReader({
                price_to_weight: this._barcodeProductAction,
            });
        }
        async getQuantityFromPrice(product, price) {
            const product_price = product.lst_price;
            if (product_price === 0) {
                return 0;
            }
            const taxes = this.env.pos.get_taxes_after_fp(product.taxes_id);
            const allPrices = this.env.pos.compute_all(
                taxes,
                product_price,
                1,
                this.env.pos.currency.rounding
            );
            const isTaxIncluded = this.env.pos.config.is_price_to_weight_tax_included;
            if (isTaxIncluded) {
                return price / allPrices.total_included;
            }
            return price / allPrices.total_excluded;
        }
        async _barcodeProductAction(code) {
            if (code.type !== "price_to_weight") {
                return await super._barcodeProductAction(...arguments);
            }

            // <BEGIN> copy of the original function '_barcodeProductAction'
            const product = await this._getProductByBarcode(code);
            if (!product) {
                return;
            }
            const options = await this._getAddProductOptions(product, code);
            // Do not proceed on adding the product when no options is returned.
            // This is consistent with _clickProduct.
            if (!options) return;
            // </END> copy of the original function '_barcodeProductAction'

            // update the options depending on the type of the scanned code

            const barcode_price = parseFloat(code.value, 10) || 0;
            const quantity = await this.getQuantityFromPrice(product, barcode_price);
            Object.assign(options, {
                quantity: quantity,
                merge: false,
            });
            this.currentOrder.add_product(product, options);
            NumberBuffer.reset();
        }
    };

Registries.Component.extend(ProductScreen, PosPriceToWeightProductScreen);
