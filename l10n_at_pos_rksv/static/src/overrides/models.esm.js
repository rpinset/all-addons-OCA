// Copyright 2024 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import {PosOrder} from "@point_of_sale/app/models/pos_order";
import {patch} from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    /**
     * @override - initial setup of the RKSV signature fields
     */
    setup(vals) {
        super.setup(vals);
        if (
            this.config_id &&
            this.config_id.asign_enabled &&
            this.config_id.asign_state !== "draft"
        ) {
            this.asign_state = vals.asign_state || "u";
            this.asign_serial = vals.asign_serial || "";
            this.asign_qrcode = vals.asign_qrcode || "";
            this.asign_type = vals.asign_type || "";
        } else {
            this.asign_state = false;
        }
    },
});
