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

// Systray items render right-to-left by descending sequence (higher =
// further left; the user menu at sequence 0 is the right-most). A low
// sequence keeps the reviewer menu grouped with the standard
// notification menus (messaging 25, activities 20) on the right, rather
// than off on the far left -- notably to the right of the Enterprise AI
// button (which sits left of the messaging menu, i.e. sequence > 25).
registry
    .category("systray")
    .add("base_tier_validation.ReviewerMenu", systrayItem, {sequence: 24});
