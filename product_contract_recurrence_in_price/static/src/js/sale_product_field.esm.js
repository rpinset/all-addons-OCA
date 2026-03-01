/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {SaleOrderLineProductField} from "@sale/js/sale_product_field";

patch(SaleOrderLineProductField.prototype, {
    get contractContext() {
        const context = super.contractContext;
        return {
            ...context,
            default_include_recurrence_in_price:
                this.props.record.data.include_recurrence_in_price,
        };
    },
});
