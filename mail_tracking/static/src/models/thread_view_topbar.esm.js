/** @odoo-module **/

import {registerPatch} from "@mail/model/model_core";
import Dialog from "web.Dialog";

registerPatch({
    name: "ThreadViewTopbar",
    recordMethods: {
        async onClickMarkAllFailedAsReviewed() {
            await this._askMarkAllFailedAsReviewed();
            this.messaging.models.Message.markAllFailedAsReviewed();
        },
        _askMarkAllFailedAsReviewed() {
            return new Promise((resolve) => {
                Dialog.confirm(
                    this,
                    this.env._t(
                        "Do you really want to mark as reviewed all the failed messages?"
                    ),
                    {
                        buttons: [
                            {
                                text: this.env._t("Ok"),
                                classes: "btn-primary",
                                close: true,
                                click: resolve,
                            },
                            {
                                text: this.env._t("Cancel"),
                                close: true,
                            },
                        ],
                    }
                );
            });
        },
    },
});
