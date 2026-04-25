odoo.define("pos_hr_access_right.TicketScreen", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const TicketScreen = require("pos_access_right.TicketScreen");

    const PosHRTicketScreen = (OriginalTicketScreen) =>
        class extends OriginalTicketScreen {
            get hasNewOrdersControlRights() {
                if (this.env.pos.config.module_pos_hr)
                    return this.env.pos.cashier.hasGroupMultiOrder;
                return super.hasNewOrdersControlRights;
            }

            async _onDeleteOrder({detail: order}) {
                if (
                    this.env.pos.config.module_pos_hr &&
                    !this.env.pos.cashier.hasGroupDeleteOrder
                )
                    return;
                return super._onDeleteOrder({detail: order});
            }
        };

    Registries.Component.extend(TicketScreen, PosHRTicketScreen);

    return TicketScreen;
});
