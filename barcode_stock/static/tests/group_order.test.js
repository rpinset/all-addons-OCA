import {describe, expect, test} from "@odoo/hoot";
import {PickingListScreen} from "@barcode_stock/js/screens/picking_list_screen.esm";

describe("BarcodeStock", () => {
    test("grouping levels nest in the order of groupOrder", () => {
        const list = Object.create(PickingListScreen.prototype);
        list.state = {groupByLevels: []};
        list.computeGroups = () => undefined;
        // A module adding a level only extends groupOrder.
        list.groupOrder = ["extra", "date", "state"];
        list.toggleGroupLevel("state");
        list.toggleGroupLevel("extra");
        expect(list.state.groupByLevels).toEqual(["extra", "state"]);
        list.toggleGroupLevel("date");
        expect(list.state.groupByLevels).toEqual(["extra", "date", "state"]);
        list.toggleGroupLevel("extra");
        expect(list.state.groupByLevels).toEqual(["date", "state"]);
    });
});
