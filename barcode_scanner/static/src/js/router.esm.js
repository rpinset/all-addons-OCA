import {Reactive} from "@web/core/utils/reactive";
import {browser} from "@web/core/browser/browser";
import {registry} from "@web/core/registry";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";

const HISTORY_LIMIT = 50;

export class BarcodeRouter extends Reactive {
    static serviceDependencies = [];

    constructor(...args) {
        super(...args);
        this.setup(...args);
    }

    setup() {
        this.currentRoute = null;
        this.routeParams = {};
        this.history = [];
        this._onPopState = this._onPopState.bind(this);
        browser.addEventListener("popstate", this._onPopState);
    }

    destroy() {
        browser.removeEventListener("popstate", this._onPopState);
    }

    _onPopState(ev) {
        const state = ev.state;
        if (!state || !state.routeName) {
            return;
        }
        if (!barcodeScreens.contains(state.routeName)) {
            return;
        }
        this.history = [];
        this.currentRoute = {name: state.routeName};
        this.routeParams = state.params || {};
    }

    _sanitizeHistoryState(state) {
        try {
            return JSON.parse(JSON.stringify(state));
        } catch {
            return {};
        }
    }

    navigate(routeName, params = {}, options = {}) {
        if (!barcodeScreens.contains(routeName)) {
            throw new Error(`Unknown route: ${routeName}`);
        }

        if (params.pickingId !== undefined) {
            const pickingId = parseInt(params.pickingId, 10);
            if (isNaN(pickingId) || pickingId <= 0) {
                throw new Error(`Invalid pickingId: ${params.pickingId}`);
            }
            params = {...params, pickingId};
        }
        if (params.picking_id !== undefined) {
            const pickingId = parseInt(params.picking_id, 10);
            if (isNaN(pickingId) || pickingId <= 0) {
                throw new Error(`Invalid picking_id: ${params.picking_id}`);
            }
            params = {...params, picking_id: pickingId};
        }

        if (options.clearHistory) {
            this.history = [];
        } else if (this.currentRoute && !options.replace) {
            this.history.push({
                route: this.currentRoute,
                params: this.routeParams,
            });
            if (this.history.length > HISTORY_LIMIT) {
                this.history.shift();
            }
        }

        const historyState = this._sanitizeHistoryState({routeName, params});
        if (options.replace || options.clearHistory) {
            history.replaceState(historyState, "", browser.location.href);
        } else {
            history.pushState(historyState, "", browser.location.href);
        }

        this.currentRoute = {name: routeName};
        this.routeParams = params;
    }

    goBack(overrides) {
        const previous = this.history.pop();
        if (previous) {
            this.currentRoute = previous.route;
            this.routeParams = overrides || previous.params;
            const historyState = this._sanitizeHistoryState({
                routeName: previous.route.name,
                params: this.routeParams,
            });
            history.replaceState(historyState, "", browser.location.href);
        } else {
            this.currentRoute = barcodeScreens.contains("main") ? {name: "main"} : null;
            this.routeParams = overrides || {};
            const historyState = this._sanitizeHistoryState({
                routeName: "main",
                params: this.routeParams,
            });
            history.replaceState(historyState, "", browser.location.href);
        }
    }

    getState() {
        return {
            currentRoute: this.currentRoute,
            routeParams: this.routeParams,
            history: this.history,
        };
    }
}

export const barcodeRouterService = {
    dependencies: BarcodeRouter.serviceDependencies,
    start(env) {
        return new BarcodeRouter(env);
    },
};

registry.category("services").add("barcodeRouter", barcodeRouterService);
