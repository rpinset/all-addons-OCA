import {
    PRODUCT_FIELDS,
    PURCHASABLE_PRODUCTS,
    PurchaseScreen,
} from "@barcode_purchase/js/screens/purchase_screen.esm";
import {beforeEach, describe, expect, test} from "@odoo/hoot";
import {PurchaseProductSelectorScreen} from "@barcode_purchase/js/screens/product_selector_screen.esm";
import {patchTranslations} from "@web/../tests/web_test_helpers";

// Units of measure as a database holds them; a dozen is a twelfth of a unit.
const UOMS = [
    {id: 1, factor: 1, rounding: 0.01},
    {id: 2, factor: 1 / 12, rounding: 0.01},
];
const BOLTS = {
    id: 7,
    display_name: "Bolts",
    default_code: "B-7",
    tracking: "none",
    uom_id: [1, "Units"],
    uom_po_id: [1, "Units"],
};
const CHEESE = {...BOLTS, id: 8, display_name: "Cheese", tracking: "lot"};
// Stocked by the unit, bought by the dozen.
const EGGS = {...BOLTS, id: 9, display_name: "Eggs", uom_po_id: [2, "Dozens"]};

/**
 * A purchase screen, without mounting it, with the units of measure loaded.
 * What it tells the operator lands in `notes`, where it navigates in `moves`,
 * what it searches for in `searches` (answered by model with `found`) and the
 * calls it makes in `calls`, answered by method with `answers`.
 */
async function purchaseScreen({found = {}, answers = {}, state = {}} = {}) {
    const screen = Object.create(PurchaseScreen.prototype);
    const notes = [];
    const moves = [];
    const searches = [];
    const calls = [];
    screen.state = {
        supplier: {id: 3, name: "Vendor"},
        destinationLocation: null,
        buyer: null,
        vendorRef: "",
        lines: [],
        autoValidate: true,
        saving: false,
        ...state,
    };
    screen.inventory = {
        notify: (message, options) =>
            notes.push({message: String(message), ...options}),
        searchRead: async (model, domain) => {
            searches.push({model, domain});
            return model === "uom.uom" ? UOMS : found[model] || [];
        },
        call: async (model, method, args, kwargs) => {
            calls.push({model, method, args, kwargs});
            const answer = answers[method];
            return typeof answer === "function" ? answer(args) : answer;
        },
    };
    screen.store = {navigate: (route, params) => moves.push({route, params})};
    await screen.loadUoms();
    return {screen, notes, moves, searches, calls};
}

describe("BarcodePurchase", () => {
    beforeEach(() => patchTranslations());

    test("the same product and lot add up on one line, priced by the order", async () => {
        const {screen} = await purchaseScreen();
        screen.addLine(BOLTS, null, 1);
        screen.addLine(BOLTS, null, 2);
        screen.addLine(CHEESE, "LOT-A", 1);
        screen.addLine(CHEESE, "LOT-B", 1);
        expect(
            screen.state.lines.map((l) => [l.product_id, l.lot_name, l.qty])
        ).toEqual([
            [7, null, 3],
            [8, "LOT-A", 1],
            [8, "LOT-B", 1],
        ]);
        // No price of its own: the order will price it from the vendor.
        expect(screen.state.lines[0]).toMatchObject({
            price_unit: null,
            uom_name: "Units",
            tracking: "none",
        });
        screen.removeLine(screen.state.lines[1]);
        expect(screen.state.lines.map((l) => l.lot_name)).toEqual([null, "LOT-B"]);
    });

    test("a line is in the purchase unit, and a label's pieces are converted", async () => {
        const {screen} = await purchaseScreen();
        // 24 eggs on the label are 2 dozens; a plain scan is one dozen.
        screen.addPicked({product: EGGS, parsed: {lot: "LOT-E", qty: 24}});
        screen.addPicked({product: EGGS, parsed: null});
        screen.addPicked({product: EGGS, parsed: {qty: 6}});
        expect(screen.state.lines.map((l) => [l.lot_name, l.qty, l.uom_name])).toEqual([
            ["LOT-E", 2, "Dozens"],
            [null, 1.5, "Dozens"],
        ]);
        // Bought by the unit: the pieces as they come, the lot kept.
        screen.addPicked({product: CHEESE, parsed: {lot: "LOT-C", qty: 3}});
        expect(screen.state.lines[2]).toMatchObject({lot_name: "LOT-C", qty: 3});
        // A weight is no count: converting it is left to a bridge module.
        expect(screen.scannedQuantity({qty: null, weight: 1.25}, BOLTS)).toBe(1);
    });

    test("the vendor's prices are shown until the operator types one", async () => {
        const {screen, calls} = await purchaseScreen({
            answers: {barcode_purchase_prices: ([, lines]) => lines.map(() => 7)},
        });
        screen.addLine(BOLTS, null, 2);
        screen.addLine(CHEESE, "LOT-A", 1);
        screen.state.lines[1].price_unit = 0;
        await screen.refreshPrices();
        // Only the line without a typed price is asked about.
        expect(calls[0].args).toEqual([3, [{product_id: 7, qty: 2}]]);
        expect(screen.state.lines.map((l) => screen.linePrice(l))).toEqual([7, 0]);
        expect(screen.state.lines.map((l) => screen.lineSubtotal(l))).toEqual([
            "14.00",
            "0.00",
        ]);
        // No vendor yet: nothing to ask.
        screen.state.supplier = null;
        await screen.refreshPrices();
        expect(calls.length).toBe(1);
    });

    test("an older price answer never overwrites a later one", async () => {
        const pending = [];
        const {screen} = await purchaseScreen({
            answers: {
                barcode_purchase_prices: () => new Promise((r) => pending.push(r)),
            },
        });
        screen.addLine(BOLTS, null, 1);
        const first = screen.refreshPrices();
        const second = screen.refreshPrices();
        pending[1]([5]);
        await second;
        pending[0]([9]);
        await first;
        expect(screen.state.lines[0].price_estimate).toBe(5);
    });

    test("a scanned location sets the destination, anything else a product", async () => {
        const shelf = {id: 5, display_name: "WH/Stock/Shelf"};
        const withShelf = await purchaseScreen({found: {"stock.location": [shelf]}});
        await withShelf.screen.onBarcodeScanned("LOC-SHELF", null);
        expect(withShelf.screen.state.destinationLocation).toEqual(shelf);
        const located = withShelf.searches.find(
            (search) => search.model === "stock.location"
        );
        expect(located.domain[0]).toEqual(["usage", "=", "internal"]);
        expect(withShelf.screen.state.lines).toEqual([]);

        const {screen, searches, calls} = await purchaseScreen({
            found: {"product.product": [BOLTS]},
            answers: {barcode_purchase_prices: [4]},
        });
        await screen.onBarcodeScanned("9501101020917", {value: "9501101020917"});
        const products = searches.find((search) => search.model === "product.product");
        expect(products.domain.slice(0, 2)).toEqual(PURCHASABLE_PRODUCTS);
        expect(screen.state.lines[0]).toMatchObject({product_id: 7, price_estimate: 4});
        expect(calls[0].method).toBe("barcode_purchase_prices");
    });

    test("a serial number is listed once, one unit", async () => {
        const {screen, notes} = await purchaseScreen();
        const drill = {...BOLTS, id: 10, display_name: "Drill", tracking: "serial"};
        screen.addPicked({product: drill, parsed: {serial: "SN-1", qty: 3}});
        screen.addPicked({product: drill, parsed: {serial: "SN-1"}});
        expect(screen.state.lines.map((l) => [l.lot_name, l.qty])).toEqual([
            ["SN-1", 1],
        ]);
        expect(notes).toEqual([
            {message: "Serial number SN-1 is already on the list.", type: "warning"},
        ]);
    });

    test("a scan the save overtakes adds nothing", async () => {
        let answer = null;
        const {screen, notes} = await purchaseScreen();
        screen.inventory.searchRead = (model) =>
            model === "product.product"
                ? new Promise((resolve) => {
                      answer = resolve;
                  })
                : Promise.resolve([]);
        const scanning = screen.onBarcodeScanned("9501101020917", null);
        await Promise.resolve();
        await Promise.resolve();
        // The order goes off while the product is being looked up.
        screen.state.saving = true;
        answer([BOLTS]);
        await scanning;
        expect(screen.state.lines).toEqual([]);
        expect(notes.map((n) => n.message)).toEqual([
            "Wait until the order is saved to scan again.",
        ]);
    });

    test("an unknown product and a scan while saving add nothing", async () => {
        const {screen, notes} = await purchaseScreen();
        await screen.onBarcodeScanned("NOPE", null);
        screen.state.saving = true;
        await screen.onBarcodeScanned("NOPE", null);
        expect(screen.state.lines).toEqual([]);
        expect(notes.map((n) => n.message)).toEqual([
            "Product not found.",
            "Wait until the order is saved to scan again.",
        ]);
    });

    test("the order is sent in one call, priced only where the operator typed", async () => {
        const {screen, calls, moves, notes} = await purchaseScreen({
            answers: {
                action_barcode_purchase: {
                    name: "P00042",
                    state: "purchase",
                    missing_lots: [],
                    unplaced_lots: [],
                },
            },
            state: {
                destinationLocation: {id: 5, display_name: "Shelf"},
                buyer: {id: 9, name: "Buyer"},
                vendorRef: "REF-1",
            },
        });
        screen.addLine(CHEESE, "LOT-A", 2);
        screen.addLine(BOLTS, null, 1);
        screen.state.lines[1].price_unit = 0;
        await screen.createPurchase();
        expect(calls).toEqual([
            {
                model: "purchase.order",
                method: "action_barcode_purchase",
                args: [
                    3,
                    [
                        {product_id: 8, qty: 2, price_unit: null, lot_name: "LOT-A"},
                        {product_id: 7, qty: 1, price_unit: 0, lot_name: false},
                    ],
                ],
                kwargs: {
                    confirm: true,
                    location_dest_id: 5,
                    user_id: 9,
                    partner_ref: "REF-1",
                },
            },
        ]);
        expect(moves).toEqual([{route: "main", params: undefined}]);
        expect(notes).toEqual([
            {message: "Purchase order P00042 confirmed.", type: "success"},
        ]);
        expect(screen.state.saving).toBe(false);
    });

    test("a draft is saved without touching the validate box", async () => {
        const {screen, calls, notes} = await purchaseScreen({
            answers: {
                action_barcode_purchase: {
                    name: "P00043",
                    state: "draft",
                    missing_lots: [],
                    unplaced_lots: [],
                },
            },
        });
        screen.addLine(BOLTS, null, 1);
        await screen.saveDraft();
        expect(calls[0].kwargs.confirm).toBe(false);
        expect(screen.state.autoValidate).toBe(true);
        expect(notes).toEqual([
            {message: "Purchase order P00043 saved as a draft.", type: "success"},
        ]);
    });

    test("nothing is sent without a vendor or a product", async () => {
        const noVendor = await purchaseScreen({state: {supplier: null}});
        await noVendor.screen.createPurchase();
        const noLines = await purchaseScreen();
        await noLines.screen.createPurchase();
        expect([...noVendor.calls, ...noLines.calls]).toEqual([]);
        expect([noVendor.notes[0].message, noLines.notes[0].message]).toEqual([
            "Please select a supplier.",
            "Please add at least one product.",
        ]);
    });

    test("the operator is told what the order ended up as", async () => {
        const told = async (result, confirm = true) => {
            const {screen, notes} = await purchaseScreen();
            screen.notifyOutcome(
                {missing_lots: [], unplaced_lots: [], ...result},
                confirm
            );
            return notes.map((n) => [n.message, n.type]);
        };
        expect(
            await told({name: "P1", state: "purchase", missing_lots: ["Cheese"]})
        ).toEqual([
            ["P1 confirmed -- set the lot/serial of Cheese on the receipt.", "warning"],
        ]);
        expect(await told({name: "P1", state: "to approve"})).toEqual([
            ["Purchase order P1 created -- it is waiting for approval.", "warning"],
        ]);
        expect(await told({name: "P1", state: "draft"})).toEqual([
            ["Purchase order P1 was created but is still a draft.", "warning"],
        ]);
        expect(await told({name: "P1", state: "draft"}, false)).toEqual([
            ["Purchase order P1 saved as a draft.", "success"],
        ]);
        expect(
            await told({
                name: "P1",
                state: "purchase",
                unplaced_lots: ["Cheese (LOT-X)"],
            })
        ).toEqual([
            ["Set these lots on the receipt by hand: Cheese (LOT-X)", "warning"],
            ["Purchase order P1 confirmed.", "success"],
        ]);
    });

    test("the product selector hands the picked product back", () => {
        const selector = Object.create(PurchaseProductSelectorScreen.prototype);
        const moves = [];
        const lines = [{product_id: 7, lot_name: null, qty: 1}];
        selector.props = {params: {supplier: {id: 3}, lines}};
        selector.store = {navigate: (route, params) => moves.push({route, params})};
        selector.confirmSelection({...EGGS, image_url: "/x.png"}, {lot: "LOT-A"});
        expect(moves[0].route).toBe("purchase");
        expect(moves[0].params).toMatchObject({
            supplier: {id: 3},
            lines,
            addProduct: {
                product: {id: 9, uom_po_id: [2, "Dozens"]},
                parsed: {lot: "LOT-A"},
            },
        });
        // Only the fields a line needs ride along.
        expect(Object.keys(moves[0].params.addProduct.product).sort()).toEqual(
            ["id", ...PRODUCT_FIELDS].sort()
        );
    });
});
