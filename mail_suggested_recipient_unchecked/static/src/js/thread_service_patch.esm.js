/** @odoo-module */

import {ThreadService} from "@mail/core/common/thread_service";
import {patch} from "@web/core/utils/patch";

patch(ThreadService.prototype, {
    async insertSuggestedRecipients(thread) {
        await super.insertSuggestedRecipients(...arguments);
        for (var recipient of thread.suggestedRecipients) {
            recipient.checked = false;
        }
    },
});
