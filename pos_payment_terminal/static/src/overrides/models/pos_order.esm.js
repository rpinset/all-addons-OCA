import {PosOrder} from "@point_of_sale/app/models/pos_order";
import {patch} from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    shouldHideReturnToBasketButton() {
        if (this.payment_ids.length > 0) {
            for (const line of this.payment_ids) {
                if (
                    line.payment_method_id.use_payment_terminal ===
                        "oca_payment_terminal" &&
                    this.config.payment_terminal_hide_back_btn
                ) {
                    return true;
                }
            }
        }
        return false;
    },
});
