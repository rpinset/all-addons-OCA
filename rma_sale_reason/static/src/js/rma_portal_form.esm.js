/*  Copyright 2024 Raumschmiede GmbH
    Copyright 2024 BCIM
    Copyright 2024 ACSONE SA/NV
    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).*/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.PortalRmaSale.include({
    events: {
        ...publicWidget.registry.PortalRmaSale.prototype.events,
        "change .rma-reason": "_onChangeReasonId",
    },

    _onChangeReasonId() {
        this._checkCanSubmit();
    },

    _canSubmit() {
        const is_required = this.$el.find('input[name="is_rma_reason_required"]').val();
        if (is_required === "0") {
            return this._super(...arguments);
        }
        let has_reason = false;
        for (const id of this.rows_ids) {
            const reason = this.$(`[name='${id}-reason_id']`);
            if (reason && reason.val()) {
                has_reason = true;
                break;
            }
        }
        return has_reason && this._super(...arguments);
    },
});
