import {PosStore} from "@point_of_sale/app/store/pos_store";
import {patch} from "@web/core/utils/patch";

patch(PosStore.prototype, {
    // @Override
    useProxy() {
        return (
            (this.config.is_posbox && this.config.iface_payment_terminal) ||
            super.useProxy()
        );
    },
});
