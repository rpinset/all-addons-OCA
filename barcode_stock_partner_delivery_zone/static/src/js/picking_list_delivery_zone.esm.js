import {PickingListScreen} from "@barcode_stock/js/screens/picking_list_screen.esm";
import {_t} from "@web/core/l10n/translation";
import {onWillStart} from "@odoo/owl";
import {patch} from "@web/core/utils/patch";

/** Grouping level and filter key of the delivery zone. */
export const ZONE = "delivery_zone";
/** Filter value that keeps the operations without a delivery zone. */
export const NO_ZONE = "none";
/** Group key of the operations without a delivery zone. */
export const NO_ZONE_GROUP = "zone:none";
/** Group key of the operations whose delivery zone could not be read. */
export const UNKNOWN_ZONE_GROUP = "zone:unknown";

/**
 * Bring `partner_delivery_zone` into the warehouse app's operation lists: the
 * delivery zone becomes a grouping level (the outermost one) and a filter --
 * which the ★ can save as the default, like the status and date ones -- and is
 * shown on each operation and matched by the search.
 *
 * Delivery orders open grouped by zone, the way a dispatcher works through
 * them; the other operation types do not, since the zone belongs to the
 * customer goods are delivered to. Any grouping the operator picks during the
 * session is kept.
 */
patch(PickingListScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.initDeliveryZone();
        this.state.deliveryZones = [];
        onWillStart(async () => {
            this.state.deliveryZones = await this.loadZoneCatalog();
        });
    },

    /**
     * The zones the filter offers. Archived ones too: a filter saved on a zone
     * archived since then must still read as that zone (see zoneFilterOptions).
     * Should they not load, the list opens all the same, without zones to
     * filter on; the API wrapper has already told the operator.
     *
     * @returns {Promise<Object[]>} the zones, archived ones included
     */
    async loadZoneCatalog() {
        try {
            return await this.inventory.searchRead(
                "partner.delivery.zone",
                [["active", "in", [true, false]]],
                ["id", "name", "active"]
            );
        } catch {
            return [];
        }
    },

    /** Register the zone as a grouping level and as a filter. */
    initDeliveryZone() {
        this.groupOrder = [ZONE, ...this.groupOrder.filter((g) => g !== ZONE)];
        this.groupLabels = {...this.groupLabels, [ZONE]: _t("Delivery Zone")};
        this.filterLabels = {...this.filterLabels, [ZONE]: _t("Delivery Zone")};
        this.sessionViewRestored = false;
    },

    // --- data -----------------------------------------------------------------

    /**
     * `loadPickings` hands its freshly read operations here before showing
     * them: read their delivery zone alongside the move statistics, so the list
     * is grouped and filtered by zone from its very first render.
     *
     * @param {Object[]} pickings the operations just read, not shown yet
     * @returns {Promise<Object>} the move statistics, per operation
     */
    async loadMoveStats(pickings) {
        const [stats] = await Promise.all([
            super.loadMoveStats(...arguments),
            this.loadDeliveryZones(pickings),
        ]);
        return stats;
    },

    async loadDeliveryZones(pickings) {
        const ids = pickings.map((picking) => picking.id).filter(Boolean);
        if (!ids.length) {
            return;
        }
        let records = null;
        try {
            records = await this.inventory.read("stock.picking", ids, [
                "delivery_zone_id",
            ]);
        } catch {
            // The operations are listed all the same. Their zone is left
            // unknown, not set to "no zone": they are neither grouped nor
            // filtered out as if they had none (see isZoneUnknown).
            this.inventory.notify(
                _t(
                    "The delivery zones could not be read: the operations are listed without them."
                ),
                {type: "warning"}
            );
            return;
        }
        const zoneById = Object.fromEntries(
            records.map((record) => [record.id, record.delivery_zone_id])
        );
        for (const picking of pickings) {
            picking.delivery_zone_id = zoneById[picking.id] || false;
        }
    },

    getDeliveryZoneName(picking) {
        return picking.delivery_zone_id?.[1] || "";
    },

    /**
     * Whether the operation's zone could not be read: it has none set, not
     * even `false`, the value of an operation without a zone.
     *
     * @param {Object} picking the operation
     * @returns {Boolean} whether its zone is unknown
     */
    isZoneUnknown(picking) {
        return picking.delivery_zone_id === undefined;
    },

    // --- grouping -------------------------------------------------------------

    getGroupKey(picking, groupBy) {
        if (groupBy === ZONE) {
            if (this.isZoneUnknown(picking)) {
                return UNKNOWN_ZONE_GROUP;
            }
            // By id, not by name: two zones may share a name, and a zone may
            // be named like the group of the operations without one.
            const zoneId = picking.delivery_zone_id?.[0];
            return zoneId ? `zone:${zoneId}` : NO_ZONE_GROUP;
        }
        return super.getGroupKey(...arguments);
    },

    isZoneGroup(groupKey) {
        return groupKey.startsWith("zone:");
    },

    /**
     * What a group's header shows. A zone group is keyed by the zone's id, so
     * its name is taken from its operations; other groups show their key.
     *
     * @param {String} groupKey the group's key
     * @returns {String} the group's title
     */
    getGroupTitle(groupKey) {
        if (groupKey === NO_ZONE_GROUP) {
            return _t("No zone");
        }
        if (groupKey === UNKNOWN_ZONE_GROUP) {
            return _t("Unknown zone");
        }
        if (!this.isZoneGroup(groupKey)) {
            return groupKey;
        }
        const zoneId = Number(groupKey.slice("zone:".length));
        const picking = this.state.pickings.find(
            (p) => p.delivery_zone_id?.[0] === zoneId
        );
        return picking ? picking.delivery_zone_id[1] : groupKey;
    },

    /**
     * Zone groups are drawn in the order of the names they show, not of their
     * ids; zones sharing a name keep the order of their ids.
     *
     * @returns {String[]} the group keys, in the order they are drawn
     */
    sortedGroupKeys() {
        const keys = super.sortedGroupKeys(...arguments);
        if (!keys.some((key) => this.isZoneGroup(key))) {
            return keys;
        }
        const titles = Object.fromEntries(
            keys.map((key) => [key, this.getGroupTitle(key)])
        );
        return keys.sort((left, right) =>
            titles[left].localeCompare(titles[right], undefined, {
                numeric: true,
                sensitivity: "base",
            })
        );
    },

    /**
     * Restoring this session's working view keeps the operator's grouping.
     *
     * @returns {*} what the restore itself returns
     */
    applyViewState() {
        this.sessionViewRestored = true;
        return super.applyViewState(...arguments);
    },

    async loadDefaultFilter() {
        await super.loadDefaultFilter(...arguments);
        if (
            !this.sessionViewRestored &&
            this.operationType === "outgoing" &&
            !this.state.groupByLevels.length
        ) {
            this.state.groupByLevels = [ZONE];
        }
    },

    // --- filtering ------------------------------------------------------------

    getMatchingPickings() {
        const pickings = super.getMatchingPickings(...arguments);
        if (!this.state.activeFilters.includes(ZONE)) {
            return pickings;
        }
        const zone = this.state.filterValues[ZONE];
        return pickings.filter((picking) => this.matchesZoneFilter(picking, zone));
    },

    matchesZoneFilter(picking, zone) {
        if (this.isZoneUnknown(picking)) {
            // Its zone could not be read: keep it in sight rather than hide
            // an operation the filter may well keep.
            return true;
        }
        const zoneId = picking.delivery_zone_id?.[0] || false;
        return zone === NO_ZONE ? !zoneId : zoneId === zone;
    },

    /**
     * Radio options for the Delivery Zone section of the Filters menu: the
     * active zones, and an archived one only while it is the zone filtered on,
     * so that a saved filter still shows what it keeps and can be changed.
     */
    get zoneFilterOptions() {
        const selected = this.state.activeFilters.includes(ZONE)
            ? this.state.filterValues[ZONE]
            : null;
        const zones = this.state.deliveryZones.filter(
            (zone) => zone.active !== false || zone.id === selected
        );
        return [
            {value: null, label: _t("All")},
            {value: NO_ZONE, label: _t("No zone")},
            ...zones.map((zone) => ({value: zone.id, label: this.zoneLabel(zone)})),
        ];
    },

    zoneLabel(zone) {
        if (zone.active === false) {
            return _t("%(zone)s (archived)", {zone: zone.name});
        }
        return zone.name;
    },

    isZoneOptionSelected(value) {
        const active = this.state.activeFilters.includes(ZONE);
        return value === null
            ? !active
            : active && this.state.filterValues[ZONE] === value;
    },

    /**
     * Pick a zone from the menu; the empty value turns the filter off.
     *
     * @param {Number|String|null} value a zone id, NO_ZONE, or null for all
     */
    setZoneFilter(value) {
        if (value === null || value === undefined) {
            this.removeFilter(ZONE);
            return;
        }
        if (!this.state.activeFilters.includes(ZONE)) {
            this.state.activeFilters = [...this.state.activeFilters, ZONE];
        }
        this.state.filterValues[ZONE] = value;
        this.computeGroups();
        // Changing the zone of an already active filter is not one of the
        // changes the list watches: remember the view explicitly.
        this.persistSessionView();
    },

    getFilterDisplayValue(filter) {
        if (filter !== ZONE) {
            return super.getFilterDisplayValue(...arguments);
        }
        const value = this.state.filterValues[ZONE];
        if (value === NO_ZONE) {
            return _t("No zone");
        }
        const zone = this.state.deliveryZones.find((z) => z.id === value);
        return zone ? this.zoneLabel(zone) : _t("Unknown zone");
    },

    // --- search ---------------------------------------------------------------

    getPickingSearchText(picking) {
        return [
            super.getPickingSearchText(...arguments),
            this.normalizeSearchValue(this.getDeliveryZoneName(picking)),
        ].join(" ");
    },
});
