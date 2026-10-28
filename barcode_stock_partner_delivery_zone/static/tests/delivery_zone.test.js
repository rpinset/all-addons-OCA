import "@barcode_stock_partner_delivery_zone/js/picking_info_delivery_zone.esm";
import {
    NO_ZONE,
    NO_ZONE_GROUP,
    UNKNOWN_ZONE_GROUP,
    ZONE,
} from "@barcode_stock_partner_delivery_zone/js/picking_list_delivery_zone.esm";
import {beforeEach, describe, expect, test} from "@odoo/hoot";
import {PickingInfoTab} from "@barcode_stock/js/components/picking_info_tab.esm";
import {PickingListScreen} from "@barcode_stock/js/screens/picking_list_screen.esm";
import {getTemplate} from "@web/core/templates";
import {patchTranslations} from "@web/../tests/web_test_helpers";

const ZONES = [
    {id: 1, name: "North"},
    {id: 2, name: "South"},
];

const PICKINGS = [
    {id: 10, name: "WH/OUT/00010", state: "assigned", delivery_zone_id: [1, "North"]},
    {id: 11, name: "WH/OUT/00011", state: "assigned", delivery_zone_id: [2, "South"]},
    {id: 12, name: "WH/OUT/00012", state: "assigned", delivery_zone_id: false},
];

/**
 * A list screen without its OWL setup, wired the way the patch sets it up.
 *
 * @param {Object} [options] the operation type and the fake ORM to use
 * @returns {PickingListScreen} the screen to test
 */
function listScreen({type = "outgoing", inventory = {}} = {}) {
    const screen = Object.create(PickingListScreen.prototype);
    screen.props = {params: {type}};
    screen.inventory = inventory;
    screen.groupOrder = ["date", "state"];
    screen.groupLabels = {date: "Date", state: "Status"};
    screen.filterLabels = {state: "Status", date: "Date"};
    screen.allDefaults = {};
    screen.state = {
        pickings: PICKINGS.map((picking) => ({...picking})),
        groupByLevels: [],
        groupedPickings: {},
        activeFilters: [],
        filterValues: {state: "all", date: null},
        stateLabels: {assigned: "Ready"},
        deliveryZones: ZONES,
        savedDefault: null,
        search: "",
    };
    screen.initDeliveryZone();
    // Unit tests never mount the screen: keep the session views untouched.
    screen.persistSessionView = () => undefined;
    return screen;
}

const ids = (pickings) => pickings.map((picking) => picking.id);

describe("DeliveryZone", () => {
    // `_t()` texts become strings only once translations are loaded.
    beforeEach(() => patchTranslations());

    test("the zone is the outermost grouping level", () => {
        const screen = listScreen();
        expect(screen.groupOrder).toEqual([ZONE, "date", "state"]);
        expect(screen.groupLabels[ZONE]).toBe("Delivery Zone");
        expect(screen.filterLabels[ZONE]).toBe("Delivery Zone");
    });

    test("operations group by zone, those without one under No zone", () => {
        const screen = listScreen();
        const groups = screen.groupRecursively(screen.state.pickings, [ZONE]);
        expect(ids(groups["zone:1"])).toEqual([10]);
        expect(ids(groups["zone:2"])).toEqual([11]);
        expect(ids(groups[NO_ZONE_GROUP])).toEqual([12]);
        expect(screen.sortedGroupKeys(groups, 0)).toEqual([
            NO_ZONE_GROUP,
            "zone:1",
            "zone:2",
        ]);
        expect(screen.getGroupTitle("zone:1")).toBe("North");
        expect(screen.getGroupTitle(NO_ZONE_GROUP)).toBe("No zone");
        // Other levels keep showing their own key.
        expect(screen.getGroupTitle("Ready")).toBe("Ready");
    });

    test("zones are grouped by id, whatever their name", () => {
        const screen = listScreen();
        const zone = (id, name) => ({
            id,
            name: `WH/OUT/000${id}`,
            state: "assigned",
            delivery_zone_id: [id, name],
        });
        screen.state.pickings = [
            zone(1, "North"),
            zone(3, "North"),
            zone(4, "No zone"),
            zone(5, "__proto__"),
            zone(6, "constructor"),
            {id: 7, name: "WH/OUT/0007", state: "assigned", delivery_zone_id: false},
        ];
        const groups = screen.groupRecursively(screen.state.pickings, [ZONE]);
        const keys = screen.sortedGroupKeys(groups, 0);
        // Two zones sharing a name stay apart, as does a zone named like the
        // group of the operations without one.
        expect(keys.map((key) => screen.getGroupTitle(key))).toEqual([
            "__proto__",
            "constructor",
            "No zone",
            "No zone",
            "North",
            "North",
        ]);
        expect(keys.map((key) => ids(groups[key]))).toEqual([
            [5],
            [6],
            [4],
            [7],
            [1],
            [3],
        ]);
    });

    test("the list opens even if the zones cannot be read", async () => {
        const screen = listScreen({
            inventory: {
                searchRead: () => Promise.reject(new Error("offline")),
            },
        });
        expect(await screen.loadZoneCatalog()).toEqual([]);
        screen.state.deliveryZones = [];
        expect(screen.zoneFilterOptions.map((o) => o.value)).toEqual([null, NO_ZONE]);
    });

    test("adding a grouping level keeps the zone outermost", () => {
        const screen = listScreen();
        screen.state.groupByLevels = ["date"];
        screen.toggleGroupLevel(ZONE);
        expect(screen.state.groupByLevels).toEqual([ZONE, "date"]);
        screen.toggleGroupLevel(ZONE);
        expect(screen.state.groupByLevels).toEqual(["date"]);
    });

    test("the zone filter keeps one zone, or the operations without one", () => {
        const screen = listScreen();
        screen.setZoneFilter(1);
        expect(ids(screen.getMatchingPickings())).toEqual([10]);
        expect(screen.getFilterDisplayValue(ZONE)).toBe("North");
        screen.setZoneFilter(NO_ZONE);
        expect(ids(screen.getMatchingPickings())).toEqual([12]);
        expect(screen.getFilterDisplayValue(ZONE)).toBe("No zone");
        expect(screen.isZoneOptionSelected(NO_ZONE)).toBe(true);
        screen.setZoneFilter(null);
        expect(screen.state.activeFilters).not.toInclude(ZONE);
        expect(ids(screen.getMatchingPickings())).toEqual([10, 11, 12]);
        expect(screen.isZoneOptionSelected(null)).toBe(true);
    });

    test("the zone filter can be saved as the default", () => {
        const screen = listScreen();
        screen.setZoneFilter(2);
        const config = screen.currentFilterConfig;
        expect(config.activeFilters).toInclude(ZONE);
        expect(config.filterValues[ZONE]).toBe(2);
        const other = listScreen();
        other.applyFilterConfig(config);
        expect(ids(other.getMatchingPickings())).toEqual([11]);
    });

    test("a zone filtered on and archived since still shows as itself", () => {
        const archived = [...ZONES, {id: 3, name: "East", active: false}];
        const values = (screen) => screen.zoneFilterOptions.map((o) => o.value);
        const saved = listScreen();
        saved.state.deliveryZones = archived;
        saved.setZoneFilter(3);
        const screen = listScreen();
        screen.state.deliveryZones = archived;
        // An archived zone is not offered...
        expect(values(screen)).toEqual([null, NO_ZONE, 1, 2]);
        // ...unless it is the one a saved filter keeps.
        screen.applyFilterConfig(saved.currentFilterConfig);
        expect(screen.zoneFilterOptions.at(-1)).toEqual({
            value: 3,
            label: "East (archived)",
        });
        expect(screen.isZoneOptionSelected(3)).toBe(true);
        expect(screen.getFilterDisplayValue(ZONE)).toBe("East (archived)");
        // Back to all the zones, it is offered no more.
        screen.setZoneFilter(null);
        expect(values(screen)).toEqual([null, NO_ZONE, 1, 2]);
    });

    test("the search also matches the zone name", () => {
        const screen = listScreen();
        expect(ids(screen.getMatchingPickings("south"))).toEqual([11]);
    });

    test("zones are read alongside the move statistics", async () => {
        const pickings = [{id: 10}, {id: 12}];
        const screen = listScreen({
            inventory: {
                searchRead: () => [],
                read: (model, recordIds) =>
                    model === "stock.picking"
                        ? recordIds.map((id) => ({
                              id,
                              delivery_zone_id: id === 10 ? [1, "North"] : false,
                          }))
                        : [],
            },
        });
        await screen.loadMoveStats(pickings);
        expect(pickings[0].delivery_zone_id).toEqual([1, "North"]);
        expect(pickings[1].delivery_zone_id).toBe(false);
    });

    test("the list opens even if the operations' zones cannot be read", async () => {
        const notes = [];
        const pickings = [
            {id: 10, state: "assigned"},
            {id: 12, state: "assigned"},
        ];
        const screen = listScreen({
            inventory: {
                searchRead: () => [],
                read: (model) =>
                    model === "stock.picking"
                        ? Promise.reject(new Error("offline"))
                        : [],
                notify: (message, options) =>
                    notes.push({message: String(message), ...options}),
            },
        });
        await screen.loadMoveStats(pickings);
        expect(pickings.map((p) => p.delivery_zone_id)).toEqual([undefined, undefined]);
        expect(notes).toEqual([
            {
                message:
                    "The delivery zones could not be read: the operations are listed without them.",
                type: "warning",
            },
        ]);
        // Their zone is unknown, not "no zone": grouped apart, and kept in
        // sight whatever zone is filtered on.
        screen.state.pickings = pickings;
        const groups = screen.groupRecursively(pickings, [ZONE]);
        expect(Object.keys(groups)).toEqual([UNKNOWN_ZONE_GROUP]);
        expect(screen.getGroupTitle(UNKNOWN_ZONE_GROUP)).toBe("Unknown zone");
        screen.setZoneFilter(NO_ZONE);
        expect(ids(screen.getMatchingPickings())).toEqual([10, 12]);
        screen.setZoneFilter(1);
        expect(ids(screen.getMatchingPickings())).toEqual([10, 12]);
    });

    test("delivery orders open grouped by zone, other operations do not", async () => {
        const inventory = {read: () => [{barcode_default_filters: {}}]};
        const outgoing = listScreen({type: "outgoing", inventory});
        await outgoing.loadDefaultFilter();
        expect(outgoing.state.groupByLevels).toEqual([ZONE]);
        const incoming = listScreen({type: "incoming", inventory});
        await incoming.loadDefaultFilter();
        expect(incoming.state.groupByLevels).toEqual([]);
    });

    test("a grouping restored from the session is kept", async () => {
        const inventory = {read: () => [{barcode_default_filters: {}}]};
        const screen = listScreen({type: "outgoing", inventory});
        screen.applyViewState({activeFilters: [], filterValues: {}, groupByLevels: []});
        expect(screen.sessionViewRestored).toBe(true);
        await screen.loadDefaultFilter();
        expect(screen.state.groupByLevels).toEqual([]);
    });
});

describe("DeliveryZone info tab", () => {
    // `_t()` texts become strings only once translations are loaded.
    beforeEach(() => patchTranslations());

    function infoTab(write) {
        const tab = Object.create(PickingInfoTab.prototype);
        tab.props = {picking: {id: 10}};
        tab.zoneState = {
            zones: ZONES,
            zone: [1, "North"],
            saving: false,
            failed: false,
        };
        tab.inventory = {write, notify: () => undefined};
        return tab;
    }

    test("changing the zone writes it at once", async () => {
        const calls = [];
        const tab = infoTab((model, recordIds, vals) =>
            calls.push([model, recordIds, vals])
        );
        await tab.onDeliveryZoneChange({target: {value: "2"}});
        expect(calls).toEqual([["stock.picking", [10], {delivery_zone_id: 2}]]);
        expect(tab.zoneState.zone).toEqual([2, "South"]);
        await tab.onDeliveryZoneChange({target: {value: ""}});
        expect(calls[1][2]).toEqual({delivery_zone_id: false});
        expect(tab.zoneState.zone).toBe(false);
    });

    test("a refused change shows the zone the operation still has", async () => {
        const tab = infoTab(() => {
            throw new Error("refused");
        });
        const target = {value: "2"};
        await tab.onDeliveryZoneChange({target});
        expect(tab.zoneState.zone).toEqual([1, "North"]);
        expect(target.value).toBe("1");
        expect(tab.zoneState.saving).toBe(false);
    });

    test("the zone cannot be changed if it could not be read", async () => {
        const tab = infoTab(() => undefined);
        tab.zoneState.zone = false;
        tab.inventory.searchRead = () => Promise.reject(new Error("offline"));
        tab.inventory.read = () => Promise.resolve([]);
        await tab.loadDeliveryZone();
        expect(tab.zoneState.failed).toBe(true);
        expect(tab.zoneState.zone).toBe(false);
    });

    test("the zones and the operation's own are read together", async () => {
        const tab = infoTab(() => undefined);
        tab.zoneState.zone = false;
        tab.inventory.searchRead = () => Promise.resolve(ZONES);
        tab.inventory.read = () =>
            Promise.resolve([{id: 10, delivery_zone_id: [2, "South"]}]);
        await tab.loadDeliveryZone();
        expect(tab.zoneState).toMatchObject({failed: false, zone: [2, "South"]});
        expect(tab.zoneState.zones).toEqual(ZONES);
    });

    test("an archived zone still set stays in the list", () => {
        const tab = infoTab(() => undefined);
        tab.zoneState.zone = [9, "Old zone"];
        expect(tab.deliveryZoneOptions.map((zone) => zone.id)).toEqual([1, 2, 9]);
        expect(tab.isDeliveryZoneSelected({id: 9})).toBe(true);
    });
});

describe("DeliveryZone templates", () => {
    // Template extensions are applied in the browser: an XPath that no longer
    // finds its node would only break when the screen is drawn.
    test("the zone reaches the list, its cards and the information tab", () => {
        const html = (name) => getTemplate(name).outerHTML;
        expect(html("barcode_scanner.PickingListScreen")).toInclude(
            "zoneFilterOptions"
        );
        expect(html("barcode_scanner.GroupRenderer")).toInclude("p.delivery_zone_id");
        expect(html("barcode_scanner.GroupRenderer")).toInclude(
            "component.getGroupTitle(groupKey)"
        );
        expect(html("barcode_scanner.PickingInfoTab")).toInclude(
            "onDeliveryZoneChange"
        );
    });
});
