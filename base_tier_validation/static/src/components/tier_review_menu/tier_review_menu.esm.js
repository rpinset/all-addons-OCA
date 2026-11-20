import {Component, onWillDestroy, useState} from "@odoo/owl";
import {Dropdown} from "@web/core/dropdown/dropdown";
import {browser} from "@web/core/browser/browser";
import {registry} from "@web/core/registry";
import {useDiscussSystray} from "@mail/utils/common/hooks";
import {useDropdownState} from "@web/core/dropdown/dropdown_hooks";
import {useService} from "@web/core/utils/hooks";

// Minimum time between two recounts triggered by bus notifications (ms).
export const RECOUNT_INTERVAL = 2000;

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
        this.lastFetch = 0;
        this.recountTimer = null;
        onWillDestroy(() => browser.clearTimeout(this.recountTimer));
        // Keep the badge live and correct: re-fetch the authoritative count
        // whenever a tier review changes server-side, instead of nudging a
        // running +/- delta. The absolute value is a len() and so can never go
        // negative, which a delta could when an update reaches a user for whom
        // the review was never part of their pending count.
        //
        // That re-fetch is not free: ``review_user_count`` runs a few queries
        // per reviewed model, and the notification reaches every reviewer of
        // the document. The server sends one notification per reviewer per
        // transaction, and ``scheduleRecount`` throttles what is left.
        this.fetchSystrayReviewer();
        // The footer link's action does not change while the page is open:
        // read it once, not on every recount.
        this.loadDashboardAction();
        this.busService.subscribe("base.tier.validation/updated", () =>
            this.scheduleRecount()
        );
        this.busService.start();
    }

    scheduleRecount() {
        // Throttle, not debounce: a burst of changes is coalesced into at most
        // one recount per RECOUNT_INTERVAL, but the badge never lags further
        // behind, however long the burst lasts.
        if (this.recountTimer) {
            return;
        }
        const wait = this.lastFetch + RECOUNT_INTERVAL - Date.now();
        if (wait <= 0) {
            this.fetchSystrayReviewer();
            return;
        }
        this.recountTimer = browser.setTimeout(() => {
            this.recountTimer = null;
            this.fetchSystrayReviewer();
        }, wait);
    }

    async fetchSystrayReviewer() {
        // A recount can outlast the throttle window on a busy database. Never
        // let them overlap: remember that something changed and re-run once,
        // instead of stacking concurrent calls on top of a slow one.
        if (this.fetchRunning) {
            this.fetchPending = true;
            return;
        }
        this.fetchRunning = true;
        this.lastFetch = Date.now();
        try {
            const groups = await this.orm.call("res.users", "review_user_count");
            let total = 0;
            for (const group of groups) {
                // Headline counter mirrors what the reviewer must act on
                // *right now*: late + pending. Future is a heads-up only
                // and shouldn't inflate the urgency badge.
                total += (group.late_count || 0) + (group.pending_count || 0);
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

    async loadDashboardAction() {
        // False when no downstream module exposes a global review dashboard
        // (default); a serialised action dict when one does (e.g.
        // ``base_tier_validation_board``).
        const action = await this.orm.call("res.users", "tier_review_dashboard_action");
        this.store.tierReviewDashboardAction = action || null;
    }

    openDashboard() {
        const action = this.store.tierReviewDashboardAction;
        if (!action) {
            return;
        }
        this.dropdown.close();
        this.action.doAction(action, {clearBreadcrumbs: true});
    }

    availableViews() {
        return [
            [false, "kanban"],
            [false, "list"],
            [false, "form"],
            [false, "activity"],
        ];
    }

    openReviewGroup(group, bucket = null) {
        this.dropdown.close();
        // Per-bucket ids are pre-computed server-side so we just hand
        // them to the action's domain. Empty buckets are no-ops.
        const idsByBucket = {
            late: group.late_ids || [],
            pending: group.pending_ids || [],
            future: group.future_ids || [],
        };
        let ids = [];
        if (bucket) {
            ids = idsByBucket[bucket] || [];
        } else {
            // Clicking the row opens what the reviewer can act on (late +
            // pending), or the future reviews when there is nothing else.
            ids = [...idsByBucket.late, ...idsByBucket.pending];
            if (!ids.length) {
                ids = idsByBucket.future;
            }
        }
        if (!ids.length) {
            return;
        }
        const labelByBucket = {
            late: "Late",
            pending: "Pending",
            future: "Future",
        };
        const domain = [["id", "in", ids]];
        if (group.active_field) {
            domain.push(["active", "in", [true, false]]);
        }
        const views = this.availableViews();

        this.action.doAction(
            {
                context: {},
                domain,
                name: bucket
                    ? `${group.name} - ${labelByBucket[bucket] || bucket}`
                    : group.name,
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

// Systray items render right-to-left by descending sequence (higher =
// further left; the user menu at sequence 0 is the right-most). A low
// sequence keeps the reviewer menu grouped with the standard
// notification menus (messaging 25, activities 20) on the right, rather
// than off on the far left -- notably to the right of the Enterprise AI
// button (which sits left of the messaging menu, i.e. sequence > 25).
registry
    .category("systray")
    .add("base_tier_validation.ReviewerMenu", systrayItem, {sequence: 24});
