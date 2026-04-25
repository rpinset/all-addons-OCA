/**
 *  Copyright 2026 Bernat Obrador APSL-Nagarro
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
import {PosStore} from "@point_of_sale/app/store/pos_store";
import {patch} from "@web/core/utils/patch";
import {user} from "@web/core/user";

patch(PosStore.prototype, {
    async setup() {
        await super.setup(...arguments);
        this.user.canSeeSupplierInfo = await user.hasGroup(
            "point_of_sale.group_pos_manager"
        );
    },
});
