import {beforeEach, describe, expect, test} from "@odoo/hoot";
import {PickingListScreen} from "@barcode_stock/js/screens/picking_list_screen.esm";
import {patchTranslations} from "@web/../tests/web_test_helpers";

/**
 * A list screen without its OWL setup, grouping by `levels`.
 *
 * @param {String[]} [levels] the grouping levels, outermost first
 * @returns {PickingListScreen} the screen to test
 */
function listScreen(levels = []) {
    const list = Object.create(PickingListScreen.prototype);
    list.state = {
        search: "",
        groupByLevels: levels,
        stateLabels: {assigned: "Ready", confirmed: "Waiting", draft: "Draft"},
    };
    return list;
}

/**
 * An operation scheduled `days` days from today, at noon, as the ORM sends it.
 *
 * @param {Number|null} days days from today; null for no date
 * @param {String} [state] its status
 * @returns {Object} the operation
 */
function picking(days, state = "assigned") {
    if (days === null) {
        return {id: 100, state, scheduled_date: false};
    }
    const date = new Date();
    date.setDate(date.getDate() + days);
    date.setHours(12, 0, 0, 0);
    return {
        id: 100 + days,
        state,
        scheduled_date: date.toISOString().slice(0, 19).replace("T", " "),
    };
}

describe("BarcodeStock", () => {
    beforeEach(() => patchTranslations());

    test("the first group shown starts open, the others collapsed", () => {
        const list = listScreen();
        // The operations came in by scheduled date: the zone of the earliest
        // one is not the first group the list draws.
        const groups = {Zeta: [1], Alpha: [2], "No zone": [3]};
        expect(list.sortedGroupKeys(groups, 0)).toEqual(["Alpha", "No zone", "Zeta"]);
        expect(list.initialCollapsedGroups(groups)).toEqual({
            "root-Alpha": false,
            "root-No zone": true,
            "root-Zeta": true,
        });
        // While searching, every group is open.
        list.state.search = "WH/OUT";
        expect(list.initialCollapsedGroups(groups)).toEqual({
            "root-Alpha": false,
            "root-No zone": false,
            "root-Zeta": false,
        });
    });

    test("with no group or a single one", () => {
        const list = listScreen(["state"]);
        expect(list.initialCollapsedGroups({})).toEqual({});
        expect(list.initialCollapsedGroups({Ready: [picking(0)]})).toEqual({
            "root-Ready": false,
        });
    });

    test("status groups go by name, the first one open", () => {
        const list = listScreen(["state"]);
        const groups = list.groupRecursively(
            [picking(0, "confirmed"), picking(1, "assigned"), picking(2, "draft")],
            ["state"]
        );
        expect(list.sortedGroupKeys(groups, 0)).toEqual(["Draft", "Ready", "Waiting"]);
        expect(list.initialCollapsedGroups(groups)).toEqual({
            "root-Draft": false,
            "root-Ready": true,
            "root-Waiting": true,
        });
    });

    test("date groups follow the calendar, those without a date last", () => {
        const list = listScreen(["date"]);
        const pickings = [5, null, 1, 0, -2, 40].map((days) => picking(days));
        const groups = list.groupRecursively(pickings, ["date"]);
        const label = (days) =>
            list.getRelativeDayLabel(
                list.parseScheduledDate(picking(days).scheduled_date)
            );
        const expected = [label(-2), "Today", "Tomorrow", label(5), label(40)];
        expect(list.sortedGroupKeys(groups, 0)).toEqual([...expected, "No date"]);
        // The group open is the first one shown: the earliest day.
        const collapsed = list.initialCollapsedGroups(groups);
        expect(Object.keys(collapsed).filter((key) => !collapsed[key])).toEqual([
            "root-" + label(-2),
        ]);
    });

    test("the same day of another year is a group of its own", () => {
        const list = listScreen(["date"]);
        const date = new Date();
        date.setHours(12, 0, 0, 0);
        date.setFullYear(date.getFullYear() + 1);
        const nextYear = {
            ...picking(0),
            id: 200,
            scheduled_date: date.toISOString().slice(0, 19).replace("T", " "),
        };
        const groups = list.groupRecursively([nextYear, picking(0)], ["date"]);
        const keys = list.sortedGroupKeys(groups, 0);
        expect(keys.length).toBe(2);
        expect(keys[0]).toBe("Today");
        expect(keys[1]).toInclude(String(date.getFullYear()));
    });

    test("each level of nested groups keeps its own order", () => {
        const pickings = [
            picking(1, "confirmed"),
            picking(0, "draft"),
            picking(0, "confirmed"),
        ];
        // Date, then status.
        const byDate = listScreen(["date", "state"]);
        let groups = byDate.groupRecursively(pickings, ["date", "state"]);
        expect(byDate.sortedGroupKeys(groups, 0)).toEqual(["Today", "Tomorrow"]);
        expect(byDate.sortedGroupKeys(groups.Today, 1)).toEqual(["Draft", "Waiting"]);
        // Status, then date.
        const byState = listScreen(["state", "date"]);
        groups = byState.groupRecursively(pickings, ["state", "date"]);
        expect(byState.sortedGroupKeys(groups, 0)).toEqual(["Draft", "Waiting"]);
        expect(byState.sortedGroupKeys(groups.Waiting, 1)).toEqual([
            "Today",
            "Tomorrow",
        ]);
    });
});
