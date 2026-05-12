// Copyright (C) 2023 - Today: GRAP (http://www.grap.coop)
// @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import {Orderline} from "@point_of_sale/app/generic_components/orderline/orderline";
import {PosOrder} from "@point_of_sale/app/models/pos_order";
import {PosOrderline} from "@point_of_sale/app/models/pos_order_line";
import {patch} from "@web/core/utils/patch";
import {roundCurrency} from "@point_of_sale/app/models/utils/currency";

// /////////////////////////////
// Overload models.PosOrder
// /////////////////////////////
patch(PosOrder.prototype, {
    get_margin() {
        return this.get_orderlines().reduce(
            (margin, line) => margin + line.get_margin(),
            0
        );
    },
    get_margin_rate() {
        const priceWithoutTax = this.get_total_without_tax();
        return priceWithoutTax ? (this.get_margin() / priceWithoutTax) * 100 : 0;
    },

    get_margin_rate_str() {
        return roundCurrency(this.get_margin_rate(), this.currency) + "%";
    },

    export_for_printing(baseUrl, headerData) {
        const result = super.export_for_printing(baseUrl, headerData);
        result.orderlines = result.orderlines.map((line) => ({
            ...line,
            ifaceDisplayMargin: false,
        }));
        return result;
    },
});

// /////////////////////////////
// Overload models.PosOrderline
// /////////////////////////////
patch(PosOrderline.prototype, {
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            ifaceDisplayMargin: this.get_iface_display_margin(),
            margin_rate: this.get_margin_rate(),
            margin_rate_str: this.get_margin_rate_str(),
        };
    },
    get_iface_display_margin() {
        return this.config.iface_display_margin;
    },
    get_purchase_price() {
        // Overload the function to use another field that the default standard_price
        return this.product_id.standard_price;
    },
    get_margin() {
        return (
            this.get_all_prices().priceWithoutTax - this.qty * this.get_purchase_price()
        );
    },
    get_margin_rate() {
        const priceWithoutTax = this.get_all_prices().priceWithoutTax;
        return priceWithoutTax ? (this.get_margin() / priceWithoutTax) * 100 : 0;
    },
    get_margin_rate_str() {
        return roundCurrency(this.get_margin_rate(), this.currency) + "%";
    },
});

patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                ifaceDisplayMargin: {type: Boolean, optional: true},
                margin_rate: {type: Number, optional: true},
                margin_rate_str: {type: String, optional: true},
            },
        },
    },
});
