import {Component, useState} from "@odoo/owl";
import {Dropdown} from "@web/core/dropdown/dropdown";
import {registry} from "@web/core/registry";
import {useDebounced} from "@web/core/utils/timing";
import {useDiscussSystray} from "@mail/utils/common/hooks";
import {useDropdownState} from "@web/core/dropdown/dropdown_hooks";
import {useService} from "@web/core/utils/hooks";

export class TierReviewMenu extends Component {
    static components = {Dropdown};
    static props = [];
    static template = "base_tier_validation.TierReviewMenu";

    setup() {
        super.setup();
        this.discussSystray = useDiscussSystray();
        this.orm = useService("orm");
        this.store = useState(useService("mail.store"));
        this.action = useService("action");
        this.busService = useService("bus_service");
        this.dropdown = useDropdownState();
        this.fetchPending = false;
        this.fetchRunning = false;
        // Keep the badge live and correct: re-fetch the authoritative count
        // whenever a tier review changes server-side, instead of nudging a
        // running +/- delta. The absolute value is a len() and so can never go
        // negative, which a delta could when an update reaches a user for whom
        // the review was never part of their pending count.
        //
        // That re-fetch is not free: ``review_user_count`` costs a handful of
        // queries per pending review, and the notification is broadcast to
        // every reviewer. Approving a batch of documents therefore fans out to
        // (reviewers x open tabs x documents) recounts, which is enough to
        // occupy every HTTP worker. Coalesce the bursts: the leading edge keeps
        // an isolated change instant, the trailing edge settles the final value.
        this.debouncedFetch = useDebounced(() => this.fetchSystrayReviewer(), 15000, {
            immediate: true,
            trailing: true,
        });
        this.fetchSystrayReviewer();
        this.busService.subscribe("base.tier.validation/updated", () =>
            this.debouncedFetch()
        );
        this.busService.start();
    }

    async fetchSystrayReviewer() {
        // A recount can outlast the debounce window on a busy database. Never
        // let them overlap: remember that something changed and re-run once,
        // instead of stacking concurrent calls on top of a slow one.
        if (this.fetchRunning) {
            this.fetchPending = true;
            return;
        }
        this.fetchRunning = true;
        try {
            const groups = await this.orm.call("res.users", "review_user_count");
            let total = 0;
            for (const group of groups) {
                total += group.pending_count || 0;
            }
            this.store.tierReviewCounter = total;
            this.store.tierReviewGroups = groups;
        } finally {
            this.fetchRunning = false;
        }
        if (this.fetchPending) {
            this.fetchPending = false;
            await this.fetchSystrayReviewer();
        }
    }

    availableViews() {
        return [
            [false, "kanban"],
            [false, "list"],
            [false, "form"],
            [false, "activity"],
        ];
    }

    openReviewGroup(group) {
        this.dropdown.close();
        const context = {};
        const domain = [["can_review", "=", true]];
        if (group.active_field) {
            domain.push(["active", "in", [true, false]]);
        }
        const views = this.availableViews();

        this.action.doAction(
            {
                context,
                domain,
                name: group.name,
                res_model: group.model,
                search_view_id: [false],
                type: "ir.actions.act_window",
                views,
            },
            {
                clearBreadcrumbs: true,
            }
        );
    }
}

export const systrayItem = {
    Component: TierReviewMenu,
};

registry
    .category("systray")
    .add("base_tier_validation.ReviewerMenu", systrayItem, {sequence: 99});
