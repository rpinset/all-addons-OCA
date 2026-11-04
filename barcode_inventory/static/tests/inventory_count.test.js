import {
    COUNTABLE_PRODUCTS,
    InventoryCountScreen,
} from "@barcode_inventory/js/screens/inventory_count_screen.esm";
import {beforeEach, describe, expect, test} from "@odoo/hoot";
import {
    makeMockEnv,
    patchTranslations,
    patchWithCleanup,
} from "@web/../tests/web_test_helpers";
import {InventoryLocationScreen} from "@barcode_inventory/js/screens/inventory_location_screen.esm";
import {InventoryProductSelectorScreen} from "@barcode_inventory/js/screens/inventory_product_selector_screen.esm";
import {getTemplate} from "@web/core/templates";
import {parseBarcode} from "@barcode_scanner/js/barcode_parser.esm";
import {user} from "@web/core/user";

const UNTRACKED = {
    id: 7,
    display_name: "Bolts",
    tracking: "none",
    uom_id: [1, "Units"],
    is_storable: true,
};
const BY_LOT = {
    id: 8,
    display_name: "Cheese",
    tracking: "lot",
    uom_id: [12, "kg"],
    is_storable: true,
};
const BY_SERIAL = {
    id: 9,
    display_name: "Drill",
    tracking: "serial",
    uom_id: [1, "Units"],
    is_storable: true,
};
// A product with no stock to count.
const SERVICE = {
    id: 20,
    display_name: "Gift wrapping",
    tracking: "none",
    uom_id: [1, "Units"],
    is_storable: false,
};

/**
 * The fake services a screen talks to. What it tells the operator lands in
 * `notes`, where it navigates in `moves`, what it searches for in `searches`
 * (answered in turn with `found`, the last answer repeated), what it asks
 * the server in `calls` (answered with `answer`, or in turn with `answers`;
 * failing when the answer is an Error) and the dialogs it opens in `dialogs`.
 *
 * @param {Object} [options] the answers to give
 * @returns {Object} the fakes and what they recorded
 */
function fakes({found = [[]], answer = {}, answers = null} = {}) {
    const notes = [];
    const moves = [];
    const searches = [];
    const calls = [];
    const dialogs = [];
    const inventory = {
        notify: (message, options) =>
            notes.push({message: String(message), ...options}),
        searchRead: async (model, domain) => {
            searches.push({model, domain});
            return found[Math.min(searches.length, found.length) - 1];
        },
        call: async (model, method, args, kwargs) => {
            calls.push(kwargs ? {model, method, args, kwargs} : {model, method, args});
            const reply = answers ? answers[calls.length - 1] : answer;
            if (reply instanceof Error) {
                throw reply;
            }
            return reply;
        },
        openDialog: (component, props) => dialogs.push(props),
    };
    const store = {
        navigate: (route, params, options) => moves.push({route, params, options}),
        goBack: (params) => moves.push({route: "back", params}),
    };
    return {inventory, store, notes, moves, searches, calls, dialogs};
}

/**
 * A count screen holding `lines`, without mounting it.
 *
 * @param {Object} [options] the lines and the fakes' answers
 * @returns {Object} the screen and what its fakes recorded
 */
function countScreen({lines = [], ...answers} = {}) {
    const screen = Object.create(InventoryCountScreen.prototype);
    const recorded = fakes(answers);
    screen._seq = lines.length;
    screen.state = {
        locationId: 3,
        locationName: "WH/Stock/Shelf",
        lines,
        loading: false,
        applying: false,
    };
    screen.inventory = recorded.inventory;
    screen.store = recorded.store;
    screen.flashLine = () => undefined;
    return {screen, ...recorded};
}

function stockLine(values) {
    return {
        _id: 1,
        lot_id: false,
        lot_name: "",
        theoretical_qty: 0,
        uom: "Units",
        lot_fixed: false,
        lot_options: [],
        counted: null,
        isNew: false,
        ...values,
    };
}

describe("BarcodeInventory", () => {
    beforeEach(() => patchTranslations());

    test("the same product and lot add up on one line, the newest on top", async () => {
        const {screen} = countScreen();
        await screen.addOrIncrement(UNTRACKED, null, 1);
        await screen.addOrIncrement(UNTRACKED, null, 2);
        expect(screen.state.lines.length).toBe(1);
        expect(screen.state.lines[0].counted).toBe("3");
        await screen.addOrIncrement(BY_LOT, "LOT-9", 1);
        expect(screen.state.lines.map((l) => l.product_id)).toEqual([8, 7]);
        expect(screen.state.lines[0]).toMatchObject({
            lot_name: "LOT-9",
            lot_fixed: true,
            counted: "1",
            uom: "kg",
            isNew: true,
        });
    });

    test("a product added from the selector is listed, not counted", async () => {
        const {screen, calls} = countScreen({answer: ["LOT-1"]});
        await screen.addOrIncrement(BY_LOT, null, null);
        expect(screen.state.lines[0]).toMatchObject({counted: null, lot_fixed: false});
        // Its lot is still to be set: the lots a count here can use are
        // suggested, as the server finds them.
        expect(calls).toEqual([
            {
                model: "stock.inventory",
                method: "action_barcode_lot_names",
                args: [3, 8, ""],
            },
        ]);
        expect(screen.state.lines[0].lot_options).toEqual(["LOT-1"]);
        // Picking it again leaves its line as it is.
        await screen.addOrIncrement(BY_LOT, null, null);
        expect(screen.state.lines.length).toBe(1);
        expect(screen.state.lines[0].counted).toBe(null);
    });

    test("a serial number counts one unit, once", async () => {
        const {screen, notes} = countScreen();
        await screen.addOrIncrement(BY_SERIAL, "SN-1", 3);
        await screen.addOrIncrement(BY_SERIAL, "SN-1", 1);
        expect(screen.state.lines.length).toBe(1);
        expect(screen.state.lines[0].counted).toBe("1");
        // Without its serial number yet, the line stands for one unit too.
        await screen.addOrIncrement(BY_SERIAL, null, 1);
        await screen.addOrIncrement(BY_SERIAL, null, 1);
        expect(screen.state.lines[0].counted).toBe("1");
        expect(notes).toEqual([
            {message: "Serial number SN-1 is already counted.", type: "warning"},
            {
                message:
                    "Drill is already counted: set its serial number before counting another one.",
                type: "warning",
            },
        ]);
    });

    test("scanning a serial number in stock counts it", async () => {
        const {screen, notes} = countScreen({
            lines: [
                stockLine({
                    product_id: 9,
                    tracking: "serial",
                    lot_name: "SN-1",
                    lot_fixed: true,
                    theoretical_qty: 1,
                }),
            ],
        });
        await screen.addOrIncrement(BY_SERIAL, "SN-1", 1);
        expect(screen.state.lines.length).toBe(1);
        expect(screen.state.lines[0].counted).toBe("1");
        expect(notes).toEqual([]);
    });

    test("a scan looks for the product by every code it carries", async () => {
        const {screen, searches} = countScreen({found: [[SERVICE, BY_LOT]]});
        await screen.onBarcodeScanned("(01)0123(10)L1(30)4", {
            gtin: "0123",
            value: "0123",
            lot: "L1",
            qty: 4,
        });
        const [{domain}] = searches;
        expect(JSON.stringify(domain)).toInclude("0123");
        expect(JSON.stringify(domain)).toInclude("(01)0123(10)L1(30)4");
        // The storable one among those it matches is counted.
        expect(screen.state.lines.length).toBe(1);
        expect(screen.state.lines[0]).toMatchObject({
            product_id: 8,
            lot_name: "L1",
            counted: "4",
        });
    });

    test("a scanned product with no stock to count is refused, saying why", async () => {
        const {screen, notes} = countScreen({found: [[SERVICE]]});
        await screen.onBarcodeScanned("777", {value: "777"});
        expect(screen.state.lines).toEqual([]);
        expect(notes).toEqual([
            {
                message:
                    "Gift wrapping is not a storable product: it has no stock to count.",
                type: "warning",
            },
        ]);
    });

    test("a scan matching no product says so", async () => {
        const {screen, notes} = countScreen();
        await screen.onBarcodeScanned("999", {value: "999"});
        expect(screen.state.lines).toEqual([]);
        expect(notes).toEqual([
            {message: "No product matches “999”.", type: "warning"},
        ]);
    });

    test("a plain EAN-13, as the core parser reads it, counts one unit", async () => {
        const {screen, searches} = countScreen({found: [[UNTRACKED]]});
        const parsed = parseBarcode("4006381333931");
        await screen.onBarcodeScanned("4006381333931", parsed);
        expect(JSON.stringify(searches[0].domain)).toInclude("4006381333931");
        expect(screen.state.lines[0]).toMatchObject({
            product_id: 7,
            lot_name: "",
            counted: "1",
        });
    });

    test("a scan that resolves while the count is applied changes nothing", async () => {
        const {screen, notes} = countScreen();
        let resolve = null;
        screen.inventory.searchRead = () =>
            new Promise((done) => {
                resolve = done;
            });
        const scan = screen.onBarcodeScanned("0123", {value: "0123"});
        // Apply is pressed while the product is looked up.
        screen.state.applying = true;
        resolve([UNTRACKED]);
        await scan;
        expect(screen.state.lines).toEqual([]);
        expect(notes).toEqual([
            {
                message: "Wait until the count is applied to scan again.",
                type: "warning",
            },
        ]);
    });

    test("the count is sent once, and stays as sent meanwhile", async () => {
        const line = stockLine({product_id: 7, tracking: "none", counted: "2"});
        const lot = stockLine({_id: 2, product_id: 8, tracking: "lot", lot_name: "L"});
        const {screen, calls, moves} = countScreen({lines: [line, lot]});
        let resolve = null;
        screen.inventory.call = (model, method, args) => {
            calls.push({model, method, args});
            return new Promise((done) => {
                resolve = done;
            });
        };
        const sending = screen.apply();
        await screen.apply();
        expect(calls.length).toBe(1);
        // While it is on its way, nothing changes the lines it sent.
        screen.setCounted(line, "5");
        screen.setLotName(lot, "OTHER");
        screen.removeLine(line);
        screen.addProduct();
        expect(screen.state.lines.map((l) => [l.counted, l.lot_name])).toEqual([
            ["2", ""],
            [null, "L"],
        ]);
        resolve({done: true, adjusted: 1});
        await sending;
        expect(moves.map((m) => m.route)).toEqual(["main"]);
    });

    test("a scan stands for its piece count, or one unit", () => {
        const {screen} = countScreen();
        expect(screen.scannedQuantity({qty: 6})).toBe(6);
        expect(screen.scannedQuantity({quantity: "2.5"})).toBe(2.5);
        expect(screen.scannedQuantity({qty: null, quantity: null})).toBe(1);
        expect(screen.scannedQuantity(undefined)).toBe(1);
        // A label stating zero counts zero; one stating no quantity, nothing.
        expect(screen.scannedQuantity({qty: 0})).toBe(0);
        expect(screen.scannedQuantity({qty: "abc"})).toBe(null);
        expect(screen.scannedQuantity({qty: Infinity})).toBe(null);
        expect(screen.scannedQuantity({qty: -2})).toBe(null);
    });

    test("scans wait while the count is being applied", async () => {
        const {screen, notes, searches} = countScreen();
        screen.state.applying = true;
        await screen.onBarcodeScanned("0123", {value: "0123"});
        expect(searches).toEqual([]);
        expect(notes).toEqual([
            {
                message: "Wait until the count is applied to scan again.",
                type: "warning",
            },
        ]);
    });

    test("each line shows how far the count is from the stock", async () => {
        await makeMockEnv();
        const {screen} = countScreen();
        const line = stockLine({product_id: 7, tracking: "none", theoretical_qty: 0.1});
        expect(screen.diff(line)).toBe(null);
        screen.setCounted(line, "0.3");
        expect(screen.formatDiff(screen.diff(line))).toBe("+0.2");
        expect(screen.diffClass(line)).toBe("ilx-inv-diff-up");
        screen.setCounted(line, "0");
        expect(screen.formatDiff(screen.diff(line))).toBe("-0.1");
        expect(screen.diffClass(line)).toBe("ilx-inv-diff-down");
        screen.setCounted(line, "0.1");
        expect(screen.formatDiff(screen.diff(line))).toBe("0");
        expect(screen.diffClass(line)).toBe("ilx-inv-diff-none");
        screen.setCounted(line, "");
        expect(screen.isCounted(line)).toBe(false);
        expect(screen.formatQty(10)).toBe("10");
    });

    test("applying sends the counted lines only", async () => {
        const counted = stockLine({
            _id: 1,
            product_id: 8,
            tracking: "lot",
            lot_name: "LOT-1",
            counted: "4",
        });
        const untouched = stockLine({_id: 2, product_id: 7, tracking: "none"});
        const {screen, calls, notes, moves} = countScreen({
            lines: [counted, untouched],
            answer: {done: true, adjusted: 1},
        });
        expect(screen.countedLines).toEqual([counted]);
        await screen.apply();
        expect(calls).toEqual([
            {
                model: "stock.inventory",
                method: "action_barcode_apply_count",
                args: [
                    3,
                    [
                        {
                            product_id: 8,
                            lot_name: "LOT-1",
                            counted_qty: 4,
                            theoretical_qty: 0,
                        },
                    ],
                ],
                kwargs: {force: false},
            },
        ]);
        expect(notes).toEqual([
            {message: "Inventory adjusted: 1 product(s).", type: "success"},
        ]);
        expect(moves).toEqual([
            {route: "main", params: {}, options: {clearHistory: true}},
        ]);
    });

    test("nothing is applied without a count, or a lot where one is needed", async () => {
        const {screen, calls, notes} = countScreen({
            lines: [
                stockLine({
                    product_id: 8,
                    product_name: "Cheese",
                    tracking: "lot",
                    lot_name: " ",
                }),
            ],
        });
        await screen.apply();
        screen.state.lines[0].counted = "2";
        await screen.apply();
        expect(calls).toEqual([]);
        expect(notes.map((n) => n.message)).toEqual([
            "Count at least one product before applying.",
            "Set the lot/serial for Cheese before applying.",
        ]);
    });

    test("a quantity that is not a number is not sent", async () => {
        const {screen, calls, notes} = countScreen({
            lines: [
                stockLine({
                    product_id: 7,
                    product_name: "Bolts",
                    tracking: "none",
                    counted: "1e309",
                }),
            ],
        });
        await screen.apply();
        expect(calls).toEqual([]);
        expect(notes.map((n) => n.message)).toEqual([
            "The counted quantity for Bolts is not a number.",
        ]);
    });

    test("stock changed while counting: shown, asked, forced only as confirmed", async () => {
        await makeMockEnv();
        const line = stockLine({
            product_id: 7,
            product_name: "Bolts",
            tracking: "none",
            theoretical_qty: 10,
            counted: "8",
        });
        const changed = {
            done: false,
            changed: [
                {
                    product_id: 7,
                    product_name: "Bolts",
                    lot_name: "",
                    shown: 10,
                    now: 15,
                    uom: "Units",
                },
            ],
        };
        const {screen, calls, dialogs, moves} = countScreen({
            lines: [line],
            answers: [changed, {done: true, adjusted: 1}, changed],
        });
        await screen.apply();
        // Nothing applied: the line shows the stock as it is now, and the
        // operator is asked.
        expect(calls[0].kwargs).toEqual({force: false});
        expect(calls[0].args[1][0].theoretical_qty).toBe(10);
        expect(line.theoretical_qty).toBe(15);
        expect(screen.state.applying).toBe(false);
        expect(dialogs.length).toBe(1);
        expect(dialogs[0].body).toInclude("Bolts: 10 Units when counting, 15 now");
        // Confirmed as it stands, the count is forced.
        await dialogs[0].confirm();
        expect(calls[1].kwargs).toEqual({force: true});
        expect(moves.map((m) => m.route)).toEqual(["main"]);
        // Had the count changed since the question, it is checked again.
        screen.state.applying = false;
        await screen.apply(true, "another count");
        expect(calls[2].kwargs).toEqual({force: false});
    });

    test("cancelling the stock warning and applying again asks again", async () => {
        await makeMockEnv();
        const line = stockLine({
            product_id: 7,
            product_name: "Bolts",
            tracking: "none",
            theoretical_qty: 10,
            checked_qty: 10,
            counted: "8",
        });
        const changed = {
            done: false,
            changed: [
                {
                    product_id: 7,
                    product_name: "Bolts",
                    lot_name: "",
                    shown: 10,
                    now: 15,
                    uom: "Units",
                },
            ],
        };
        const {screen, calls, dialogs} = countScreen({
            lines: [line],
            answers: [changed, changed],
        });
        await screen.apply();
        // The operator cancels: the line shows the stock as it is now...
        expect(line.theoretical_qty).toBe(15);
        // ...but applying again is still checked against the stock shown as
        // counting began, so the server warns again.
        await screen.apply();
        expect(calls.map((c) => c.args[1][0].theoretical_qty)).toEqual([10, 10]);
        expect(calls.map((c) => c.kwargs)).toEqual([{force: false}, {force: false}]);
        expect(dialogs.length).toBe(2);
    });

    test("a scan stating zero counts zero, an unreadable one nothing", async () => {
        const {screen, notes} = countScreen({found: [[UNTRACKED], [BY_LOT]]});
        await screen.onBarcodeScanned("0123", {value: "0123", qty: 0});
        expect(screen.state.lines[0]).toMatchObject({product_id: 7, counted: "0"});
        await screen.onBarcodeScanned("0456", {value: "0456", qty: "x"});
        expect(screen.state.lines.length).toBe(1);
        expect(notes.map((n) => n.message)).toEqual([
            "The quantity on the label of Cheese cannot be read.",
        ]);
    });

    test("the lot field looks lots up as the operator types", async () => {
        const line = stockLine({product_id: 8, tracking: "lot"});
        const {screen, calls} = countScreen({lines: [line]});
        const pending = [];
        screen.inventory.call = (model, method, args) => {
            calls.push(args);
            return new Promise((done) => pending.push(done));
        };
        screen.setLotName(line, "L");
        screen.setLotName(line, "LO");
        expect(line.lot_name).toBe("LO");
        expect(calls).toEqual([
            [3, 8, "L"],
            [3, 8, "LO"],
        ]);
        // Only the latest answer fills the list.
        pending[1](["LOT-1", "LOT-2"]);
        pending[0](["L-OLD"]);
        await Promise.resolve();
        await Promise.resolve();
        expect(line.lot_options).toEqual(["LOT-1", "LOT-2"]);
    });

    test("a refused count can be applied again", async () => {
        const {screen, moves} = countScreen({
            lines: [stockLine({product_id: 7, tracking: "none", counted: "1"})],
            answer: new Error("refused"),
        });
        await screen.apply();
        expect(screen.state.applying).toBe(false);
        expect(moves).toEqual([]);
    });

    test("the lines and the location are loaded from the server", async () => {
        const {screen, calls} = countScreen({
            answer: {
                lines: [
                    {
                        product_id: 8,
                        tracking: "lot",
                        lot_name: "LOT-1",
                        theoretical_qty: 5,
                    },
                    {
                        product_id: 8,
                        tracking: "lot",
                        lot_name: false,
                        theoretical_qty: 1,
                    },
                ],
            },
        });
        await screen.loadLines();
        expect(calls[0].method).toBe("action_barcode_location_lines");
        expect(screen.state.lines.map((l) => [l._id, l.lot_fixed, l.counted])).toEqual([
            [1, true, null],
            [2, false, null],
        ]);
        expect(screen.state.lines.map((l) => l.checked_qty)).toEqual([5, 1]);
        expect(screen.needsLotInput(screen.state.lines[1])).toBe(true);
        screen.setLotName(screen.state.lines[1], "LOT-2");
        expect(screen.state.lines[1].lot_name).toBe("LOT-2");
        screen.removeLine(screen.state.lines[0]);
        expect(screen.state.lines.map((l) => l._id)).toEqual([2]);
    });

    test("the + picker keeps the count and leaves out the untracked listed", () => {
        const {screen, moves} = countScreen({
            lines: [
                stockLine({_id: 1, product_id: 7, tracking: "none", counted: "2"}),
                stockLine({_id: 2, product_id: 8, tracking: "lot", lot_name: "L"}),
            ],
        });
        screen.addProduct();
        expect(moves[0].route).toBe("inventory_product_selector");
        expect(moves[0].params).toMatchObject({
            locationId: 3,
            locationName: "WH/Stock/Shelf",
            excludeProductIds: [7],
        });
        expect(moves[0].params.lines.map((l) => l.counted)).toEqual(["2", null]);
    });

    test("the selector shows only the latest search, of countable products", async () => {
        const screen = Object.create(InventoryProductSelectorScreen.prototype);
        const {inventory, store, searches, moves} = fakes();
        let answer = null;
        const pending = [];
        inventory.searchRead = (model, domain) => {
            searches.push(domain);
            return new Promise((resolve) => pending.push(() => resolve(answer)));
        };
        Object.assign(screen, {
            inventory,
            store,
            props: {params: {locationId: 3, lines: [], excludeProductIds: [7]}},
            state: {search: "bo", results: [], loading: true},
        });
        const first = screen.search();
        screen.state.search = "bol";
        const second = screen.search();
        expect(searches[1]).toEqual([
            ...COUNTABLE_PRODUCTS,
            "|",
            ["name", "ilike", "bol"],
            ["barcode", "ilike", "bol"],
            ["id", "not in", [7]],
        ]);
        answer = [UNTRACKED];
        pending[1]();
        await second;
        answer = [BY_LOT];
        pending[0]();
        await first;
        expect(screen.state.results).toEqual([UNTRACKED]);
        screen.pickProduct(UNTRACKED);
        screen.goBack();
        expect(moves.map((m) => m.params.addProduct?.id)).toEqual([7, undefined]);
        expect(moves[1].params).toMatchObject({locationId: 3, lines: []});
    });

    test("the selector refuses a scanned product with no stock to count", async () => {
        const screen = Object.create(InventoryProductSelectorScreen.prototype);
        const {inventory, store, notes, moves} = fakes({
            found: [[SERVICE], [UNTRACKED]],
        });
        Object.assign(screen, {inventory, store, props: {params: {lines: []}}});
        await screen.onBarcodeScanned("777", {value: "777"});
        expect(moves).toEqual([]);
        expect(notes.map((n) => n.message)).toEqual([
            "Gift wrapping is not a storable product: it has no stock to count.",
        ]);
        await screen.onBarcodeScanned("123", {value: "123"});
        expect(moves.map((m) => m.params.addProduct?.id)).toEqual([7]);
    });

    test("operators who cannot apply a count are told so first", async () => {
        patchWithCleanup(user, {hasGroup: async () => false});
        const screen = Object.create(InventoryLocationScreen.prototype);
        const {inventory, store, searches} = fakes({
            found: [[{id: 4, display_name: "Shelf"}]],
        });
        Object.assign(screen, {
            inventory,
            store,
            state: {locations: [], search: "", loading: true, canApply: true},
        });
        await screen.loadScreen();
        expect(screen.state).toMatchObject({canApply: false, loading: false});
        await screen.onBarcodeScanned("SHELF", {value: "SHELF"});
        expect(searches).toEqual([]);
    });

    test("the count screen locks while applying and takes decimal counts", () => {
        const html = getTemplate("barcode_inventory.InventoryCountScreen").outerHTML;
        expect(html).toInclude('step="any"');
        expect(html.split('t-att-disabled="state.applying"').length - 1).toBe(4);
    });

    test("an inventory administrator picks or scans the location", async () => {
        patchWithCleanup(user, {hasGroup: async () => true});
        const screen = Object.create(InventoryLocationScreen.prototype);
        const shelf = {id: 4, display_name: "WH/Stock/Shelf"};
        const {inventory, store, notes, moves} = fakes({
            found: [[shelf, {id: 5, display_name: "WH/Stock/Bin"}], [shelf], []],
        });
        Object.assign(screen, {
            inventory,
            store,
            state: {locations: [], search: "", loading: true, canApply: true},
        });
        await screen.loadScreen();
        expect(screen.state.locations.length).toBe(2);
        screen.state.search = "bin";
        expect(screen.filteredLocations.map((l) => l.id)).toEqual([5]);
        await screen.onBarcodeScanned("SHELF", {value: "SHELF"});
        expect(moves[0]).toMatchObject({
            route: "inventory_count",
            params: {locationId: 4, locationName: "WH/Stock/Shelf"},
        });
        await screen.onBarcodeScanned("NOPE", {value: "NOPE"});
        expect(screen.state.search).toBe("NOPE");
        expect(notes).toEqual([
            {message: "No internal location matches “NOPE”.", type: "warning"},
        ]);
    });
});
