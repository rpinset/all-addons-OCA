import {beforeEach, describe, expect, test} from "@odoo/hoot";
import {makeMockEnv, patchTranslations} from "@web/../tests/web_test_helpers";
import {
    SCRAPPABLE_PRODUCTS,
    ScrapScreen,
} from "@barcode_scrap/js/screens/scrap_screen.esm";
import {ScrapProductSelectorScreen} from "@barcode_scrap/js/screens/scrap_product_selector_screen.esm";

const UNTRACKED = {
    id: 7,
    display_name: "Bolts",
    tracking: "none",
    uom_id: [1, "Units"],
};
const BY_LOT = {id: 8, display_name: "Cheese", tracking: "lot", uom_id: [12, "kg"]};
const BY_SERIAL = {
    id: 9,
    display_name: "Drill",
    tracking: "serial",
    uom_id: [1, "Units"],
};

/**
 * A scrap screen on a location holding `stock`, without mounting it. What it
 * tells the operator lands in `notes`, where it navigates in `moves`, what it
 * searches for in `searches` (answered with `found`), the scraps it asks the
 * server for in `calls` (answered in turn with `answers`) and the dialogs it
 * opens in `dialogs`.
 */
function scrapScreen({stock = [], lines = [], found = [], answers = []} = {}) {
    const screen = Object.create(ScrapScreen.prototype);
    const notes = [];
    const moves = [];
    const searches = [];
    const calls = [];
    const dialogs = [];
    screen._seq = lines.length;
    screen.state = {
        locationId: 3,
        locationName: "WH/Stock/Shelf",
        lines,
        stock,
        reasonIds: [5],
        scrapLocationId: 4,
    };
    screen.inventory = {
        notify: (message, options) =>
            notes.push({message: String(message), ...options}),
        searchRead: async (model, domain) => {
            searches.push(domain);
            return found;
        },
        call: async (model, method, args, kwargs) => {
            calls.push({lines: args[1], ...kwargs});
            return answers[calls.length - 1];
        },
        openDialog: (component, props) => dialogs.push(props),
    };
    screen.store = {
        navigate: (route, params) => moves.push({route, params}),
        goBack: (params) => moves.push({route: "back", params}),
    };
    screen.flashLine = () => undefined;
    return {screen, notes, moves, searches, calls, dialogs};
}

const STOCK = [
    {product_id: 7, lot_id: false, lot_name: false, quantity: 4},
    {product_id: 7, lot_id: false, lot_name: false, quantity: 6},
    {product_id: 8, lot_id: 21, lot_name: "ABC", quantity: 2},
    {product_id: 8, lot_id: 22, lot_name: "abc", quantity: 3},
    {product_id: 8, lot_id: 23, lot_name: "LOT-9", quantity: 1},
];

describe("BarcodeScrap", () => {
    beforeEach(() => patchTranslations());

    test("the same product and lot add up on one line, the newest on top", async () => {
        const {screen} = scrapScreen({stock: STOCK});
        await screen.addOrIncrement(UNTRACKED, null, 1);
        await screen.addOrIncrement(UNTRACKED, null, 2);
        expect(screen.state.lines.length).toBe(1);
        expect(screen.state.lines[0].qty).toBe("3");
        await screen.addOrIncrement(BY_LOT, "LOT-9", 1);
        expect(screen.state.lines.map((l) => l.product_id)).toEqual([8, 7]);
        expect(screen.state.lines[0]).toMatchObject({lot_id: 23, lot_name: "LOT-9"});
    });

    test("a lot is matched exactly first, and in another case only alone", () => {
        const {screen} = scrapScreen({stock: STOCK});
        // Lots that differ only in case are distinct lots.
        expect(screen.findStockLot(8, "ABC").lot_id).toBe(21);
        expect(screen.findStockLot(8, "abc").lot_id).toBe(22);
        expect(screen.findStockLot(8, "Abc")).toBe(null);
        expect(screen.findStockLot(8, " lot-9 ").lot_id).toBe(23);
        expect(screen.findStockLot(8, "")).toBe(null);
    });

    test("lots that differ in case stay on lines of their own", async () => {
        const {screen} = scrapScreen({stock: STOCK});
        await screen.addOrIncrement(BY_LOT, "ABC", 1);
        await screen.addOrIncrement(BY_LOT, "abc", 1);
        expect(screen.state.lines.map((l) => l.lot_id)).toEqual([22, 21]);
    });

    test("the single lot a location holds fills itself in", async () => {
        const {screen} = scrapScreen({
            stock: [{product_id: 8, lot_id: 23, lot_name: "LOT-9", quantity: 1}],
        });
        await screen.addOrIncrement(BY_LOT, null, 1);
        expect(screen.state.lines[0]).toMatchObject({lot_id: 23, lot_name: "LOT-9"});
        // Not when the location holds several lots of it.
        const several = scrapScreen({stock: STOCK}).screen;
        await several.addOrIncrement(BY_LOT, null, 1);
        expect(several.state.lines[0]).toMatchObject({lot_id: false, lot_name: ""});
    });

    test("a serial number is listed once, one unit", async () => {
        const {screen, notes} = scrapScreen();
        await screen.addOrIncrement(BY_SERIAL, "SN-1", 3);
        await screen.addOrIncrement(BY_SERIAL, "SN-1", 1);
        expect(screen.state.lines.length).toBe(1);
        expect(screen.state.lines[0].qty).toBe("1");
        expect(notes).toEqual([
            {message: "Serial number SN-1 is already on the list.", type: "warning"},
        ]);
    });

    test("a line shows what the location holds of it", () => {
        const {screen} = scrapScreen({stock: STOCK});
        expect(screen.available({product_id: 7, tracking: "none"})).toBe(10);
        expect(screen.available({product_id: 8, tracking: "lot", lot_id: 22})).toBe(3);
        // A tracked line without its lot yet: nothing to show.
        expect(screen.available({product_id: 8, tracking: "lot", lot_id: false})).toBe(
            null
        );
    });

    test("the scrap button and the final message sum the lines up", async () => {
        await makeMockEnv();
        const {screen} = scrapScreen();
        expect(String(screen.scrapLabel())).toBe("Scrap");
        const kilos = [
            {product_id: 8, product_name: "Cheese", uom: "kg", qty: "2"},
            {product_id: 8, product_name: "Cheese", uom: "kg", qty: "0.5"},
        ];
        screen.state.lines = kilos;
        expect(screen.scrapLabel()).toBe("Scrap 2.5 kg");
        expect(screen.scrappedMessage(kilos)).toBe("Scrapped 2.5 kg of Cheese.");
        // Units that cannot be added up: a count of products instead.
        const mixed = [
            ...kilos,
            {product_id: 7, product_name: "Bolts", uom: "Units", qty: "4"},
        ];
        screen.state.lines = mixed;
        expect(screen.scrapLabel()).toBe("Scrap 2 products");
        expect(screen.scrappedMessage(mixed)).toBe("Scrapped 2 products.");
    });

    test("a scan counts the pieces it states, or one unit", () => {
        const {screen} = scrapScreen();
        expect(screen.scannedQuantity({qty: 4, quantity: 4}, 1)).toBe(4);
        expect(screen.scannedQuantity({qty: null, quantity: null}, 1)).toBe(1);
        // A weight is no count: converting it is left to a bridge module.
        expect(screen.scannedQuantity({qty: null, weight: 1.25}, 12)).toBe(1);
        expect(screen.scannedQuantity(null, 1)).toBe(1);
    });

    test("only goods are searched for, scanned or picked", async () => {
        const {screen, searches} = scrapScreen({found: [UNTRACKED]});
        await screen.onBarcodeScanned("9501101020917", {value: "9501101020917"});
        expect(searches[0].slice(0, 1)).toEqual(SCRAPPABLE_PRODUCTS);
        expect(screen.state.lines[0].product_id).toBe(7);

        const selector = Object.create(ScrapProductSelectorScreen.prototype);
        const domains = [];
        selector.props = {params: {stockProductIds: [7]}};
        selector.state = {search: "", results: [], loading: true};
        selector.inventory = {
            searchRead: async (model, domain) => {
                domains.push(domain);
                return [];
            },
        };
        await selector.search();
        selector.state.search = "bolt";
        await selector.search();
        expect(domains).toEqual([
            [...SCRAPPABLE_PRODUCTS, ["id", "in", [7]]],
            [
                ...SCRAPPABLE_PRODUCTS,
                "|",
                ["name", "ilike", "bolt"],
                ["barcode", "ilike", "bolt"],
            ],
        ]);
    });

    test("the lines in progress survive a trip to the product selector", () => {
        const line = {_id: 1, product_id: 7, lot_id: false, lot_name: "", qty: "2"};
        const {screen, moves} = scrapScreen({stock: STOCK, lines: [line]});
        screen.addProduct();
        const [{route, params}] = moves;
        expect(route).toBe("scrap_product_selector");
        expect(params).toMatchObject({
            locationId: 3,
            lines: [line],
            reasonIds: [5],
            scrapLocationId: 4,
            stockProductIds: [7, 8],
        });
        // A copy: what happens to the screen's lines meanwhile is not carried.
        expect(params.lines[0]).not.toBe(line);

        const selector = Object.create(ScrapProductSelectorScreen.prototype);
        const back = [];
        selector.props = {params};
        selector.store = {goBack: (backParams) => back.push(backParams)};
        selector.pickProduct(BY_LOT);
        expect(back[0]).toMatchObject({
            locationId: 3,
            lines: [line],
            reasonIds: [5],
            scrapLocationId: 4,
            addProduct: {id: 8, tracking: "lot", uom_id: [12, "kg"]},
        });
    });

    test("a scan waits while the scrap is on its way", async () => {
        const {screen, notes, searches} = scrapScreen({found: [UNTRACKED]});
        screen.state.scrapping = true;
        await screen.onBarcodeScanned("9501101020917", {value: "9501101020917"});
        expect(searches).toEqual([]);
        expect(screen.state.lines).toEqual([]);
        expect(notes).toEqual([
            {message: "Wait until the scrap is done to scan again.", type: "warning"},
        ]);
    });

    test("scrapping anyway only covers the lines the warning was about", async () => {
        await makeMockEnv();
        const short = {
            product_name: "Bolts",
            lot_name: false,
            requested: 12,
            available: 10,
            uom: "Units",
        };
        const line = {
            _id: 1,
            product_id: 7,
            product_name: "Bolts",
            tracking: "none",
            uom: "Units",
            lot_id: false,
            lot_name: "",
            qty: "12",
        };
        const {screen, calls, dialogs, moves} = scrapScreen({
            lines: [line],
            answers: [
                {done: false, insufficient: [short]},
                {done: true, count: 1, names: ["SP/1"]},
            ],
        });
        await screen.scrap();
        expect(calls[0]).toMatchObject({force: false, scrap_location_id: 4});
        // Confirmed as warned: forced.
        await dialogs[0].confirm();
        expect(calls[1]).toMatchObject({force: true});
        expect(moves[0].route).toBe("main");

        // Lines changed between the warning and the confirmation: checked again.
        const again = scrapScreen({
            lines: [{...line}],
            answers: [
                {done: false, insufficient: [short]},
                {done: false, insufficient: [short]},
            ],
        });
        await again.screen.scrap();
        again.screen.state.lines[0].qty = "20";
        await again.dialogs[0].confirm();
        expect(again.calls[1]).toMatchObject({force: false});
        expect(again.calls[1].lines[0].qty).toBe(20);
    });

    test("without a destination there is nothing to scrap into", async () => {
        const line = {
            _id: 1,
            product_id: 7,
            tracking: "none",
            lot_id: false,
            lot_name: "",
            qty: "1",
        };
        const {screen, calls, notes} = scrapScreen({lines: [line]});
        expect(screen.canScrap).toBe(true);
        screen.state.scrapLocationId = null;
        expect(screen.canScrap).toBe(false);
        await screen.scrap();
        expect(calls).toEqual([]);
        expect(notes).toEqual([
            {message: "Choose where the scrapped goods go.", type: "warning"},
        ]);
    });

    test("a search answered late never overwrites a later one", async () => {
        const selector = Object.create(ScrapProductSelectorScreen.prototype);
        const pending = [];
        selector.props = {params: {stockProductIds: []}};
        selector.state = {search: "", results: [], loading: true};
        selector.inventory = {
            searchRead: () => new Promise((resolve) => pending.push(resolve)),
        };
        selector.state.search = "bo";
        const first = selector.search();
        selector.state.search = "bolt";
        const second = selector.search();
        // The later search answers first, the earlier one after it.
        pending[1]([BY_LOT]);
        await second;
        pending[0]([UNTRACKED, BY_LOT]);
        await first;
        expect(selector.state.results).toEqual([BY_LOT]);
    });
});
