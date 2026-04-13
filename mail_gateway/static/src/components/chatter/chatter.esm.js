/** @odoo-module */

import {ChatterTopbar} from "@mail/components/chatter_topbar/chatter_topbar";
const {onWillStart} = owl;
import {patch} from "web.utils";
import {useService} from "@web/core/utils/hooks";

patch(
    ChatterTopbar.prototype,
    "mail_gateway/static/src/components/chatter/chatter.esm.js",
    {
        setup() {
            this._super();
            this.user = useService("user");
            onWillStart(async () => {
                this.hasGatewayGroup = await this.user.hasGroup(
                    "mail_gateway.gateway_user"
                );
            });
        },
    }
);
