/** @odoo-module **/

import {Message} from "@mail/components/message/message";
import {patch} from "web.utils";

patch(Message.prototype, "mail_tracking/static/src/components/message/message.esm.js", {
    constructor() {
        this._super(...arguments);
    },
    setup() {
        this._super(...arguments);
    },
    _onTrackingStatusClick(event) {
        var tracking_email_id = $(event.currentTarget).data("tracking");
        event.preventDefault();
        return this.env.services.action.doAction({
            type: "ir.actions.act_window",
            view_type: "form",
            view_mode: "form",
            res_model: "mail.tracking.email",
            views: [[false, "form"]],
            target: "new",
            res_id: tracking_email_id,
        });
    },
    async _onMarkFailedMessageReviewed(event) {
        event.preventDefault();
        const messageID = $(event.currentTarget).data("message-id");
        return this.messaging.rpc({
            model: "mail.message",
            method: "set_need_action_done",
            args: [[messageID]],
        });
    },
    _onRetryFailedMessage(event) {
        event.preventDefault();
        const messageID = $(event.currentTarget).data("message-id");
        this.env.services.action.doAction("mail.mail_resend_message_action", {
            additionalContext: {
                mail_message_to_resend: messageID,
            },
        });
    },
});
