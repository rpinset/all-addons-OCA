odoo.define("pos_hr_access_right.ActionpadWidget", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const ActionpadWidget = require("pos_access_right.ActionpadWidget");

    const PosHRActionpadWidget = (OriginalActionpadWidget) =>
        class extends OriginalActionpadWidget {
            get hasPaymentControlRights() {
                if (this.env.pos.config.module_pos_hr)
                    return this.env.pos.cashier.hasGroupPayment;
                return super.hasPaymentControlRights;
            }
        };

    Registries.Component.extend(ActionpadWidget, PosHRActionpadWidget);

    return ActionpadWidget;
});
