/** @odoo-module **/

import {registerPatch} from "@mail/model/model_core";
import {decrement} from "@mail/model/model_field_command";

registerPatch({
    name: "MessagingNotificationHandler",
    recordMethods: {
        async _handleNotifications({detail: notifications}) {
            const proms = notifications.map((message) => {
                if (
                    typeof message === "object" &&
                    message.type === "toggle_tracking_status"
                ) {
                    return this._handleChangeTrackingNeedsActionNotification(
                        message.payload
                    );
                }
            });
            await Promise.all(proms);
            return this._super(...arguments);
        },
        async _handleChangeTrackingNeedsActionNotification({
            message_ids = [],
            still_failed = false,
        }) {
            const failed = this.messaging.failedmsg;
            for (const message_id of message_ids) {
                const message = this.messaging.models.Message.findFromIdentifyingData({
                    id: message_id,
                });
                if (!message) {
                    continue;
                }
                if (!still_failed) {
                    message.update({
                        isFailed: false,
                        isFailedChatterMessage: false,
                        isNeedaction: false,
                    });
                }
                failed.update({counter: decrement(message_ids.length)});
            }
            if (failed.counter > failed.thread.cache.fetchedMessages.length) {
                failed.thread.cache.update({hasToLoadMessages: true});
            }
        },
    },
});
