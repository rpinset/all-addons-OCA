odoo.define("pos_hr_access_right.NumpadWidget", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const NumpadWidget = require("pos_access_right.NumpadWidget");

    const PosHRNumpadWidget = (OriginalNumpadWidget) =>
        class extends OriginalNumpadWidget {
            get hasManualDiscount() {
                if (this.env.pos.config.module_pos_hr)
                    return this.env.pos.cashier.hasGroupDiscount;
                return super.hasManualDiscount;
            }
            get hasMinusControlRights() {
                if (this.env.pos.config.module_pos_hr)
                    return this.env.pos.cashier.hasGroupNegativeQty;
                return super.hasMinusControlRights;
            }
            get hasPriceControlRights() {
                if (this.env.pos.config.module_pos_hr)
                    return this.env.pos.cashier.hasGroupPriceControl;
                return super.hasPriceControlRights;
            }
        };

    Registries.Component.extend(NumpadWidget, PosHRNumpadWidget);

    return NumpadWidget;
});
