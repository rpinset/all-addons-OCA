import {
    Component,
    onWillStart,
    useEffect,
    useExternalListener,
    useState,
} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {barcodeScreens} from "@barcode_scanner/js/registries.esm";
import {deserializeDateTime} from "@web/core/l10n/dates";
import {scanBarcode} from "@web/core/barcode/barcode_dialog";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";
import {useBarcodeScanner} from "@barcode_scanner/js/hooks/use_inventory.esm";
import {useService} from "@web/core/utils/hooks";
import {user} from "@web/core/user";

const GROUP_ORDER = ["date", "state"];
const FILTER_ORDER = ["state", "date"];
const FILTER_DEFAULTS = {state: "all", date: null};
const FILTER_LABELS = {state: _t("Status"), date: _t("Date")};

const EMPTY_MOVE_STATS = {
    skuCount: 0,
    demandQty: 0,
    doneQty: 0,
    remainingQty: 0,
};

const OPERATION_LABELS = {
    incoming: _t("Receipts"),
    internal: _t("Internal Transfers"),
    outgoing: _t("Delivery Orders"),
};

// In-session working view (filters + grouping) per operation-type code. Module
// scope so it outlives the screen being re-created on navigation: entering a
// picking and coming back keeps the filter the user was working with, without
// persisting it to the server (that is what the ★ default is for). Cleared only
// on a full app reload.
const SESSION_VIEWS = {};

export class PickingListScreen extends Component {
    setup() {
        this.inventory = useBarcodeScanner();
        this.store = useService("barcodeStore");
        this.feedback = useService("barcodeScannerFeedback");
        this.state = useState({
            pickings: [],
            moveStatsByPickingId: {},
            groupedPickings: {},
            loading: true,
            groupByLevels: [],
            collapsedGroups: {},
            search: "",
            stateLabels: {},
            activeFilters: [],
            filterValues: {state: "all", date: null},
            savedDefault: null,
            openMenu: null,
        });
        // Whole `res.users.barcode_default_filters` map, kept out of reactive
        // state: only this operation type's entry (state.savedDefault) drives the
        // ★, but the full map must survive a write so other operations' defaults
        // are not wiped.
        this.allDefaults = {};
        this.groupLabels = {
            state: _t("Status"),
            date: _t("Date"),
        };
        this.filterLabels = FILTER_LABELS;
        this.groupOrder = GROUP_ORDER;

        // Close any open filter/group menu when tapping outside the toolbar; the
        // toolbar itself stops propagation so its own taps do not trigger this.
        useExternalListener(document, "click", () => this.closeMenu());

        useBarcodeHandler({
            onScan: (barcode) => this.onBarcodeScanned(barcode),
        });

        onWillStart(async () => {
            await this.loadStateLabels();
            await this.loadDefaultFilter();
            await this.loadPickings();
        });

        this.openPicking = (id) => {
            this.store.navigate("picking", {
                pickingId: id,
                listParams: this.props.params,
            });
        };

        useEffect(
            () => {
                this.computeGroups();
                this.persistSessionView();
                const collapsed = {};
                const groups = this.state.groupedPickings;
                const keys = Object.keys(groups);
                keys.forEach((key, index) => {
                    collapsed["root-" + key] = this.state.search ? false : index !== 0;
                });
                this.state.collapsedGroups = collapsed;
            },
            () => [
                this.state.pickings,
                this.state.groupByLevels,
                this.state.search,
                this.state.activeFilters,
                this.state.filterValues.state,
                this.state.filterValues.date,
            ]
        );
    }

    async loadPickings() {
        const type = this.props.params?.type;
        const warehouseId = this.props.params?.warehouseId;
        const domain = [
            ["picking_type_id.warehouse_id", "=", warehouseId],
            ["picking_type_id.code", "=", type],
            ["state", "not in", ["done", "cancel"]],
        ];
        const fields = ["name", "partner_id", "scheduled_date", "state"];
        const result = await this.inventory.searchRead(
            "stock.picking",
            domain,
            fields,
            {
                order: "scheduled_date asc",
            }
        );
        this.state.moveStatsByPickingId = await this.loadMoveStats(result);
        this.state.pickings = result;
        this.state.collapsedGroups = {};
        this.computeGroups();
        this.state.loading = false;
    }

    async loadMoveStats(pickings) {
        const pickingIds = pickings.map((picking) => picking.id).filter(Boolean);
        if (!pickingIds.length) {
            return {};
        }
        const moves = await this.inventory.searchRead(
            "stock.move",
            [
                ["picking_id", "in", pickingIds],
                ["product_uom_qty", ">", 0],
            ],
            ["picking_id", "product_uom_qty", "qty_done_total", "quantity"]
        );
        const stats = {};
        for (const move of moves) {
            const pickingId = move.picking_id?.[0];
            if (!pickingId) {
                continue;
            }
            stats[pickingId] = stats[pickingId] || {...EMPTY_MOVE_STATS};
            stats[pickingId].skuCount += 1;
            stats[pickingId].demandQty += move.product_uom_qty || 0;
            stats[pickingId].doneQty += move.qty_done_total || 0;
            stats[pickingId].remainingQty += Math.max(
                (move.quantity || move.product_uom_qty || 0) -
                    (move.qty_done_total || 0),
                0
            );
        }
        return stats;
    }

    getGroupKey(p, groupBy) {
        if (groupBy === "state") {
            return this.state.stateLabels[p.state] || _t("Unknown");
        }
        if (groupBy === "date") {
            return p.scheduled_date
                ? this.getRelativeDayLabel(this.parseScheduledDate(p.scheduled_date))
                : _t("No date");
        }
        return _t("Other");
    }

    groupRecursively(records, levels) {
        if (!levels.length) {
            return records;
        }
        const level = levels[0];
        const rest = levels.slice(1);
        const groups = {};
        for (const r of records) {
            const key = this.getGroupKey(r, level);
            if (!groups[key]) {
                groups[key] = [];
            }
            groups[key].push(r);
        }
        for (const key in groups) {
            groups[key] = this.groupRecursively(groups[key], rest);
        }
        return groups;
    }

    goBack() {
        this.store.goBack();
    }

    get filteredPickings() {
        return this.getMatchingPickings(this.state.search);
    }

    computeGroups() {
        if (!this.state.groupByLevels.length) {
            this.state.groupedPickings = {all: this.filteredPickings};
            return;
        }
        this.state.groupedPickings = this.groupRecursively(
            this.filteredPickings,
            this.state.groupByLevels
        );
    }

    toggleGroupBy(group, ev) {
        if (ev.target.checked) {
            if (!this.state.groupByLevels.includes(group)) {
                this.state.groupByLevels = GROUP_ORDER.filter((g) =>
                    g === group
                        ? ev.target.checked
                        : this.state.groupByLevels.includes(g)
                );
            }
        } else {
            this.state.groupByLevels = this.state.groupByLevels.filter(
                (g) => g !== group
            );
        }
        this.computeGroups();
    }

    toggleGroup(path) {
        this.state.collapsedGroups[path] = !this.state.collapsedGroups[path];
    }

    addGroup(ev) {
        const value = ev.target.value;
        if (!value) {
            return;
        }
        if (!this.state.groupByLevels.includes(value)) {
            this.state.groupByLevels = GROUP_ORDER.filter(
                (group) => group === value || this.state.groupByLevels.includes(group)
            );
        }
        this.computeGroups();
        ev.target.value = "";
    }

    removeGroup(group) {
        this.state.groupByLevels = this.state.groupByLevels.filter((g) => g !== group);
        this.computeGroups();
    }

    async loadStateLabels() {
        const fields = await this.inventory.call(
            "stock.picking",
            "fields_get",
            [["state"]],
            {
                attributes: ["selection"],
            }
        );
        const selection = fields.state.selection;
        const labelsMap = {};
        for (const [key, label] of selection) {
            labelsMap[key] = label;
        }
        this.state.stateLabels = labelsMap;
    }

    get operationLabel() {
        return OPERATION_LABELS[this.props.params?.type] || _t("Pickings");
    }

    get headerSubtitle() {
        if (this.state.loading) {
            return _t("Preparing scanner-first work queue...");
        }
        return `${this.filteredPickings.length}/${this.state.pickings.length} ${_t(
            "visible"
        )} · ${this.operationLabel}`;
    }

    get summaryCards() {
        return [
            {
                key: "open",
                label: _t("Open"),
                value: this.state.pickings.length,
                tone: "default",
            },
            {
                key: "ready",
                label: _t("Ready"),
                value: this.state.pickings.filter((picking) =>
                    this.isReadyPicking(picking)
                ).length,
                tone: "success",
            },
            {
                key: "visible",
                label: _t("Visible"),
                value: this.filteredPickings.length,
                tone: "info",
            },
        ];
    }

    get availableGroupingOptions() {
        return GROUP_ORDER.filter((group) => !this.state.groupByLevels.includes(group));
    }

    normalizeSearchValue(value) {
        return (value || "").toString().trim().toLowerCase();
    }

    parseScheduledDate(value) {
        if (!value) {
            return null;
        }
        // Scheduled_date arrives from the ORM in UTC; deserializeDateTime
        // converts it to the user's timezone so that day-based grouping, the
        // date filter and the Today/Tomorrow and Urgent labels line up with the
        // date shown on the picking instead of slipping to the previous day.
        const date = deserializeDateTime(value);
        return date && date.isValid ? date.toJSDate() : null;
    }

    isSameDay(first, second) {
        return (
            first.getFullYear() === second.getFullYear() &&
            first.getMonth() === second.getMonth() &&
            first.getDate() === second.getDate()
        );
    }

    isReadyPicking(picking) {
        return picking.state === "assigned";
    }

    isUrgentPicking(picking) {
        const date = this.parseScheduledDate(picking.scheduled_date);
        if (!date) {
            return false;
        }
        const endOfToday = new Date();
        endOfToday.setHours(23, 59, 59, 999);
        return date <= endOfToday;
    }

    getRelativeDayLabel(date) {
        if (!date) {
            return _t("No date");
        }
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(today.getDate() + 1);
        if (this.isSameDay(date, today)) {
            return _t("Today");
        }
        if (this.isSameDay(date, tomorrow)) {
            return _t("Tomorrow");
        }
        return date.toLocaleDateString(undefined, {
            month: "short",
            day: "numeric",
        });
    }

    getTimeLabel(picking) {
        const date = this.parseScheduledDate(picking.scheduled_date);
        if (!date) {
            return _t("No time");
        }
        return date.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
        });
    }

    getScheduleSummary(picking) {
        const date = this.parseScheduledDate(picking.scheduled_date);
        if (!date) {
            return _t("No schedule");
        }
        return `${this.getRelativeDayLabel(date)}, ${this.getTimeLabel(picking)}`;
    }

    getStateLabel(picking) {
        return this.state.stateLabels[picking.state] || picking.state || _t("Unknown");
    }

    getPartnerName(picking) {
        return picking.partner_id?.[1] || _t("No customer");
    }

    getMoveStats(picking) {
        return this.state.moveStatsByPickingId[picking.id] || EMPTY_MOVE_STATS;
    }

    getSkuSummary(picking) {
        const stats = this.getMoveStats(picking);
        if (!stats.skuCount) {
            return _t("Queue ready");
        }
        return `${stats.skuCount} ${_t("SKUs to pick")}`;
    }

    getProgressLabel(picking) {
        const stats = this.getMoveStats(picking);
        if (!stats.skuCount) {
            return "";
        }
        if (stats.remainingQty <= 0) {
            return _t("Completed");
        }
        if (stats.doneQty > 0 && stats.demandQty > 0) {
            return `${Math.round((stats.doneQty / stats.demandQty) * 100)}% ${_t(
                "done"
            )}`;
        }
        return `${Math.round(stats.remainingQty)} ${_t("remaining")}`;
    }

    getStateBadgeClass(picking) {
        return `ilx-state-pill ilx-state-pill--${picking.state || "default"}`;
    }

    getPickingSearchText(picking) {
        return [
            picking.name,
            this.getPartnerName(picking),
            this.getStateLabel(picking),
            this.getScheduleSummary(picking),
        ]
            .map((value) => this.normalizeSearchValue(value))
            .join(" ");
    }

    matchesSearch(picking, search) {
        if (!search) {
            return true;
        }
        return this.getPickingSearchText(picking).includes(search);
    }

    matchesDateFilter(picking, dateFilter) {
        if (!dateFilter) {
            return true;
        }
        const pickingDate = this.parseScheduledDate(picking.scheduled_date);
        if (!pickingDate) {
            return false;
        }
        const today = new Date();
        if (dateFilter === "today") {
            return this.isSameDay(pickingDate, today);
        }
        if (dateFilter === "tomorrow") {
            const tomorrow = new Date(today);
            tomorrow.setDate(today.getDate() + 1);
            return this.isSameDay(pickingDate, tomorrow);
        }
        if (dateFilter.startsWith("custom:")) {
            const customDateStr = dateFilter.substring(7);
            if (!customDateStr) {
                return true;
            }
            const parts = customDateStr.split("-");
            const customDate = new Date(
                parseInt(parts[0], 10),
                parseInt(parts[1], 10) - 1,
                parseInt(parts[2], 10)
            );
            return this.isSameDay(pickingDate, customDate);
        }
        return true;
    }

    getMatchingPickings(query = "") {
        const search = this.normalizeSearchValue(query);
        return this.state.pickings.filter((picking) => {
            for (const filter of this.state.activeFilters) {
                const value = this.state.filterValues[filter];
                if (filter === "state" && value !== "all" && picking.state !== value) {
                    return false;
                }
                if (
                    filter === "date" &&
                    value &&
                    !this.matchesDateFilter(picking, value)
                ) {
                    return false;
                }
            }
            return this.matchesSearch(picking, search);
        });
    }

    getExactScanMatch(barcode) {
        const normalized = this.normalizeSearchValue(barcode);
        const exactMatches = this.state.pickings.filter(
            (picking) => this.normalizeSearchValue(picking.name) === normalized
        );
        return exactMatches.length === 1 ? exactMatches[0] : null;
    }

    async openCameraScanner() {
        try {
            const barcode = await scanBarcode(this.env, "environment");
            if (barcode) {
                this.onBarcodeScanned(barcode);
            }
        } catch (error) {
            const msg = error?.message || "";
            // A user-cancelled/aborted scan is expected; only surface real errors.
            if (!msg.includes("cancel") && !msg.includes("abort")) {
                this.feedback.error({
                    notify: true,
                    message: _t("Could not start camera: ") + msg,
                });
            }
        }
    }

    async onBarcodeScanned(barcode) {
        const scanValue = (barcode || "").trim();
        if (!scanValue) {
            return;
        }
        const exactMatch = this.getExactScanMatch(scanValue);
        if (exactMatch) {
            this.feedback.success({
                notify: true,
                message: _t("Picking opened from scan."),
            });
            this.openPicking(exactMatch.id);
            return;
        }
        this.state.search = scanValue;
        const matches = this.getMatchingPickings(scanValue);
        if (matches.length === 1) {
            this.feedback.success({
                notify: true,
                message: _t("Single picking matched the scan."),
            });
            this.openPicking(matches[0].id);
            return;
        }
        if (matches.length > 1) {
            this.feedback.info({
                notify: true,
                message: _t("Scan narrowed the queue."),
            });
            return;
        }
        // Not in the list currently shown here (which is scoped to this
        // warehouse, operation type and open state). The scanned name may belong
        // to another type, warehouse or an already-done operation, so look it up
        // on the server by exact name and open it -- otherwise scanning a valid
        // operation "worked for some and not others" with no clear reason.
        const found = await this.inventory.searchRead(
            "stock.picking",
            [["name", "=", scanValue]],
            ["id"],
            {limit: 1}
        );
        if (found.length) {
            this.feedback.success({
                notify: true,
                message: _t("Operation opened from scan."),
            });
            this.openPicking(found[0].id);
            return;
        }
        this.feedback.warning({
            notify: true,
            message: _t("No operation found for “%(code)s”.", {code: scanValue}),
        });
    }

    addFilter(ev) {
        const value = ev.target.value;
        if (!value || this.state.activeFilters.includes(value)) {
            return;
        }
        this.state.activeFilters = [...this.state.activeFilters, value];
        this.state.filterValues[value] = FILTER_DEFAULTS[value];
        ev.target.value = "";
    }

    removeFilter(filter) {
        this.state.activeFilters = this.state.activeFilters.filter((f) => f !== filter);
        this.state.filterValues[filter] = FILTER_DEFAULTS[filter];
        this.computeGroups();
    }

    setFilterValue(filter, value) {
        if (filter === "date" && value === "custom") {
            this.state.filterValues.date = "custom:";
        } else {
            this.state.filterValues[filter] = value;
        }
        this.computeGroups();
    }

    setCustomDate(dateStr) {
        if (dateStr) {
            this.state.filterValues.date = "custom:" + dateStr;
        } else {
            this.state.filterValues.date = null;
        }
        this.computeGroups();
    }

    toggleMenu(name) {
        this.state.openMenu = this.state.openMenu === name ? null : name;
    }

    closeMenu() {
        if (this.state.openMenu) {
            this.state.openMenu = null;
        }
    }

    /** Radio options for the Date section of the Filters menu. */
    get dateFilterOptions() {
        return [
            {value: null, label: _t("All")},
            {value: "today", label: _t("Today")},
            {value: "tomorrow", label: _t("Tomorrow")},
            {value: "custom:", label: _t("Custom date")},
        ];
    }

    isDateOptionSelected(value) {
        const active = this.state.activeFilters.includes("date");
        const current = this.state.filterValues.date;
        if (!value) {
            return !active;
        }
        if (value === "custom:") {
            return (
                active && typeof current === "string" && current.startsWith("custom:")
            );
        }
        return active && current === value;
    }

    /** Pick a status from the menu; "all" turns the status filter off. */
    setStateFilter(value) {
        if (!value || value === "all") {
            this.removeFilter("state");
            return;
        }
        if (!this.state.activeFilters.includes("state")) {
            this.state.activeFilters = [...this.state.activeFilters, "state"];
        }
        this.state.filterValues.state = value;
        this.computeGroups();
    }

    /** Label of the "assigned" state, shown on the Ready quick filter. */
    get readyStateLabel() {
        return this.state.stateLabels.assigned || _t("Ready");
    }

    /** The Ready quick filter is just a shortcut for status = assigned. */
    get isReadyQuickActive() {
        return (
            this.state.activeFilters.includes("state") &&
            this.state.filterValues.state === "assigned"
        );
    }

    toggleReadyQuick() {
        this.setStateFilter(this.isReadyQuickActive ? "all" : "assigned");
    }

    /** Pick a date option from the menu; the empty value turns it off. */
    setDateFilter(value) {
        if (!value) {
            this.removeFilter("date");
            return;
        }
        if (!this.state.activeFilters.includes("date")) {
            this.state.activeFilters = [...this.state.activeFilters, "date"];
        }
        this.state.filterValues.date = value;
        this.computeGroups();
    }

    /** Add or remove a grouping level from the Group menu, keeping GROUP_ORDER. */
    toggleGroupLevel(group) {
        if (this.state.groupByLevels.includes(group)) {
            this.removeGroup(group);
            return;
        }
        this.state.groupByLevels = GROUP_ORDER.filter(
            (level) => level === group || this.state.groupByLevels.includes(level)
        );
        this.computeGroups();
    }

    getFilterDisplayValue(filter) {
        const value = this.state.filterValues[filter];
        if (filter === "state") {
            if (value === "all") {
                return _t("All");
            }
            return this.state.stateLabels[value] || value;
        }
        if (filter === "ready") {
            return value ? _t("Yes") : _t("No");
        }
        if (filter === "date") {
            if (!value) {
                return _t("All");
            }
            if (value === "today") {
                return _t("Today");
            }
            if (value === "tomorrow") {
                return _t("Tomorrow");
            }
            if (value.startsWith("custom:")) {
                const dateStr = value.substring(7);
                if (!dateStr) {
                    return _t("Select date");
                }
                const parts = dateStr.split("-");
                const d = new Date(
                    parseInt(parts[0], 10),
                    parseInt(parts[1], 10) - 1,
                    parseInt(parts[2], 10)
                );
                return d.toLocaleDateString(undefined, {
                    month: "short",
                    day: "numeric",
                    year: "numeric",
                });
            }
            return value;
        }
        return "";
    }

    get availableFilterOptions() {
        return FILTER_ORDER.filter((f) => !this.state.activeFilters.includes(f));
    }

    clearFilters() {
        this.state.search = "";
        this.state.activeFilters = [];
        this.state.filterValues = {state: "all", date: null};
        this.computeGroups();
    }

    /**
     * The operation type this list belongs to; also the key under which its
     * default filter is stored in `res.users.barcode_default_filters`.
     */
    get operationType() {
        return this.props.params?.type || null;
    }

    /**
     * The built-in, Odoo-like default: show the pickings that are ready to
     * process. Applied on entry when the user has not saved their own default.
     */
    get builtinDefaultConfig() {
        return {activeFilters: ["state"], filterValues: {state: "assigned"}};
    }

    /**
     * Read the user's saved defaults and apply the one for this operation type
     * before the pickings load, so the queue arrives already filtered.
     */
    async loadDefaultFilter() {
        if (!this.operationType) {
            return;
        }
        let stored = {};
        try {
            const [record] = await this.inventory.read(
                "res.users",
                [user.userId],
                ["barcode_default_filters"]
            );
            stored = record?.barcode_default_filters || {};
        } catch {
            // A malformed map or a read hiccup must never keep the list from
            // loading: fall back to no default.
            stored = {};
        }
        this.allDefaults = stored && typeof stored === "object" ? stored : {};
        const config = this.allDefaults[this.operationType];
        if (config && Array.isArray(config.activeFilters)) {
            // Keep the saved default for the ★ state regardless of what we show.
            this.state.savedDefault = this.normalizeFilterConfig(config);
        }
        // What to show, in priority order:
        const session = SESSION_VIEWS[this.operationType];
        if (session) {
            // The filter the user was working with before navigating away:
            // survive the round trip into a picking so it need not be re-set.
            this.applyViewState(session);
        } else if (config && Array.isArray(config.activeFilters)) {
            this.applyFilterConfig(config);
        } else {
            // No personal default: open on the ready-to-process view, the way
            // Odoo opens its operation lists. A ★ default overrides this.
            this.applyFilterConfig(this.builtinDefaultConfig);
        }
    }

    /** Restore a full working view (filters + grouping) from the session stash. */
    applyViewState(view) {
        this.applyFilterConfig(view);
        this.state.groupByLevels = [...(view.groupByLevels || [])];
    }

    /**
     * Remember the current working view for this operation type, so it survives
     * the screen being torn down and rebuilt on navigation (picking ↔ list).
     */
    persistSessionView() {
        if (!this.operationType) {
            return;
        }
        SESSION_VIEWS[this.operationType] = {
            activeFilters: [...this.state.activeFilters],
            filterValues: {...this.state.filterValues},
            groupByLevels: [...this.state.groupByLevels],
        };
    }

    /**
     * Canonical, comparable form of a filter config: sorted keys and only the
     * values of the active filters, so the ★ can tell "current == saved" apart
     * from cosmetic ordering differences.
     */
    normalizeFilterConfig({activeFilters, filterValues}) {
        const filters = [...(activeFilters || [])].filter(Boolean).sort();
        const values = {};
        for (const filter of filters) {
            const value = (filterValues || {})[filter];
            values[filter] = value === undefined ? FILTER_DEFAULTS[filter] : value;
        }
        return {activeFilters: filters, filterValues: values};
    }

    applyFilterConfig(config) {
        const normalized = this.normalizeFilterConfig(config);
        this.state.activeFilters = [...normalized.activeFilters];
        this.state.filterValues = {...FILTER_DEFAULTS, ...normalized.filterValues};
    }

    get currentFilterConfig() {
        return this.normalizeFilterConfig({
            activeFilters: this.state.activeFilters,
            filterValues: this.state.filterValues,
        });
    }

    get isCurrentFilterDefault() {
        if (!this.state.savedDefault) {
            return false;
        }
        return (
            JSON.stringify(this.currentFilterConfig) ===
            JSON.stringify(this.normalizeFilterConfig(this.state.savedDefault))
        );
    }

    /** Whether the ★ has anything to act on: an active filter or a saved one. */
    get canStarFilter() {
        return this.state.activeFilters.length > 0 || Boolean(this.state.savedDefault);
    }

    get starLabel() {
        return this.isCurrentFilterDefault ? _t("Default") : _t("Set default");
    }

    get starTitle() {
        return this.isCurrentFilterDefault
            ? _t("Default filter for %(operation)s — tap to remove.", {
                  operation: this.operationLabel,
              })
            : _t("Save this filter as the default for %(operation)s.", {
                  operation: this.operationLabel,
              });
    }

    async persistDefaultFilters() {
        await this.inventory.write("res.users", [user.userId], {
            barcode_default_filters: this.allDefaults,
        });
    }

    /**
     * Star: save the current filter as this operation's default. Filled star:
     * remove it. Starring an empty filter is the same as clearing the default.
     */
    async toggleDefaultFilter() {
        const type = this.operationType;
        if (!type) {
            return;
        }
        const config = this.currentFilterConfig;
        const clearing = this.isCurrentFilterDefault || !config.activeFilters.length;
        if (clearing) {
            if (!this.state.savedDefault) {
                this.inventory.notify(
                    _t("Add a filter first, then save it as the default."),
                    {type: "warning"}
                );
                return;
            }
            delete this.allDefaults[type];
            this.state.savedDefault = null;
            await this.persistDefaultFilters();
            this.inventory.notify(
                _t("Default filter cleared for %(operation)s.", {
                    operation: this.operationLabel,
                }),
                {type: "info"}
            );
            return;
        }
        this.allDefaults[type] = config;
        this.state.savedDefault = config;
        await this.persistDefaultFilters();
        this.inventory.notify(
            _t("Filter saved as the default for %(operation)s.", {
                operation: this.operationLabel,
            }),
            {type: "success"}
        );
    }

    countGroupEntries(groupNode) {
        if (Array.isArray(groupNode)) {
            return groupNode.length;
        }
        return Object.values(groupNode).reduce(
            (count, childGroup) => count + this.countGroupEntries(childGroup),
            0
        );
    }

    sortedGroupKeys(groups) {
        return Object.keys(groups).sort((left, right) =>
            left.localeCompare(right, undefined, {
                numeric: true,
                sensitivity: "base",
            })
        );
    }

    getGroupLevelLabel(level) {
        return this.groupLabels[this.state.groupByLevels[level]] || _t("Group");
    }

    getGroupSummary(groupNode) {
        const count = this.countGroupEntries(groupNode);
        return `${count} ${count === 1 ? _t("picking") : _t("pickings")}`;
    }
}
PickingListScreen.template = "barcode_scanner.PickingListScreen";

barcodeScreens.add("picking_list", {component: PickingListScreen});
