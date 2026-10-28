import "@barcode_gs1_stock/js/gs1_stock_quantity.esm";
import {afterEach, describe, expect, test} from "@odoo/hoot";
import {
    compileGs1Nomenclature,
    setGs1Nomenclature,
} from "@barcode_gs1/js/gs1_nomenclature.esm";
import {BarcodeScannerState} from "@barcode_stock/js/services/barcode_scanner_state.esm";
import {parseGs1} from "@barcode_gs1/js/gs1_parser.esm";

// Units of measure as a stock database ships them: `factor` is how many of the
// unit make one unit of its category's reference (a kilogram is 1000 grams),
// and `rounding` is what a quantity in that unit is rounded to.
const UOMS = [
    {id: 1, name: "Units", category_id: [1, "Unit"], factor: 1.0, rounding: 0.01},
    {id: 13, name: "kg", category_id: [3, "Weight"], factor: 1.0, rounding: 0.01},
    {id: 14, name: "g", category_id: [3, "Weight"], factor: 1000.0, rounding: 0.01},
    {id: 16, name: "lb", category_id: [3, "Weight"], factor: 2.20462, rounding: 0.01},
    {id: 11, name: "L", category_id: [5, "Volume"], factor: 1.0, rounding: 0.01},
    {
        id: 6,
        name: "m",
        category_id: [4, "Length / Distance"],
        factor: 1.0,
        rounding: 0.01,
    },
];

/**
 * A scanner state with the units loaded. By default, the way Odoo ships: units
 * rounded to 0.01 and quantities stored with two decimals. `rounding` overrides
 * a unit's rounding by id, `digits` the decimals of "Product Unit of Measure".
 */
function stateWithUoms({rounding = {}, digits = 2} = {}) {
    const state = new BarcodeScannerState({});
    state.uomsById = Object.fromEntries(
        UOMS.map((uom) => [
            uom.id,
            {...uom, rounding: rounding[uom.id] ?? uom.rounding},
        ])
    );
    state.quantityDigits = digits;
    return state;
}

// The configuration that reads grams: kilograms rounded to 0.001 and quantities
// stored with three decimals.
function stateReadingGrams() {
    return stateWithUoms({rounding: {13: 0.001}, digits: 3});
}

// What barcode_gs1 hands over for a box of cured meat: two pieces, 2.497 kg.
const TWO_PIECES_OF_2497_G = {
    qty: 2,
    quantity: 2,
    count: 2,
    weight: 2.497,
    weightUom: {id: 13, name: "kg"},
};

describe("Gs1StockQuantity", () => {
    test("a product stocked by weight takes the weight, in its own unit", () => {
        const state = stateReadingGrams();
        expect(state.scannedQuantity(TWO_PIECES_OF_2497_G, 13)).toBe(2.497);
        // The label weighs in kilograms, the product is stocked in grams.
        expect(state.scannedQuantity(TWO_PIECES_OF_2497_G, 14)).toBe(2497);
    });

    test("the weight is rounded the way it will be stored", () => {
        // Odoo's defaults keep two decimals of a kilogram: 2.497 kg is stored as
        // 2.50, so that is the quantity shown.
        expect(stateWithUoms().scannedQuantity(TWO_PIECES_OF_2497_G, 13)).toBe(2.5);
        // Both settings count: a finer unit with two decimals still stores 2.50,
        // and so do three decimals with a unit rounded to 0.01.
        const finerUnit = stateWithUoms({rounding: {13: 0.001}});
        expect(finerUnit.scannedQuantity(TWO_PIECES_OF_2497_G, 13)).toBe(2.5);
        const moreDecimals = stateWithUoms({digits: 3});
        expect(moreDecimals.scannedQuantity(TWO_PIECES_OF_2497_G, 13)).toBe(2.5);
        // When the decimals could not be read, the unit's rounding still applies.
        const noDigits = stateWithUoms({rounding: {13: 0.001}, digits: null});
        expect(noDigits.scannedQuantity(TWO_PIECES_OF_2497_G, 13)).toBe(2.497);
    });

    test("a product counted in units takes the piece count", () => {
        expect(stateWithUoms().scannedQuantity(TWO_PIECES_OF_2497_G, 1)).toBe(2);
    });

    test("a weight with no count is a single unit for a product in units", () => {
        // A cheese wheel label: 4.324 kg net and no count at all. Adding "4.324
        // units" would be wrong; one box was scanned.
        const wheel = {qty: null, weight: 4.324, weightUom: {id: 13, name: "kg"}};
        expect(stateReadingGrams().scannedQuantity(wheel, 13)).toBe(4.324);
        expect(stateWithUoms().scannedQuantity(wheel, 13)).toBe(4.32);
        expect(stateWithUoms().scannedQuantity(wheel, 1)).toBe(1);
    });

    test("a measure in another unit of the same category is converted", () => {
        const pounds = {qty: null, weight: 5, weightUom: {id: 16, name: "lb"}};
        expect(stateReadingGrams().scannedQuantity(pounds, 13)).toBe(2.268);
        expect(stateWithUoms().scannedQuantity(pounds, 13)).toBe(2.27);
    });

    test("a measure of the wrong kind never becomes the quantity", () => {
        // A length says nothing about how much of a product to pick.
        const length = {qty: 3, count: 3, weight: 2.5, weightUom: {id: 6, name: "m"}};
        const state = stateWithUoms();
        expect(state.scannedQuantity(length, 6)).toBe(2.5);
        expect(state.scannedQuantity(length, 13)).toBe(3);
    });

    test("of several measures, the one in the product's kind of unit is taken", () => {
        // A net weight and a net volume, as barcode_gs1 lists them.
        const kilograms = {ai: "3103", value: 2.497, uom: {id: 13, name: "kg"}};
        const litres = {ai: "3152", value: 2.5, uom: {id: 11, name: "L"}};
        const both = {
            qty: null,
            weight: 2.497,
            weightUom: {id: 13, name: "kg"},
            measures: [kilograms, litres],
        };
        const state = stateReadingGrams();
        expect(state.scannedQuantity(both, 11)).toBe(2.5);
        expect(state.scannedQuantity(both, 13)).toBe(2.497);
        expect(state.scannedQuantity(both, 1)).toBe(1);
    });

    test("the gross weight of the pack is never the quantity", () => {
        // Even with a unit configured on its rule, AI 330n weighs the pack.
        const gross = {ai: "3303", value: 2.7, uom: {id: 13, name: "kg"}};
        const net = {ai: "3103", value: 2.497, uom: {id: 13, name: "kg"}};
        const state = stateReadingGrams();
        expect(state.scannedQuantity({qty: null, measures: [gross, net]}, 13)).toBe(
            2.497
        );
        expect(state.scannedQuantity({qty: null, measures: [gross]}, 13)).toBe(1);
    });

    test("a measure that rounds to nothing reads as a scan without one", () => {
        // 4 g of a product stocked in kilograms rounded to 0.01: a quantity of
        // zero would pick nothing, so the base reading stands.
        const pinch = {weight: 0.004, weightUom: {id: 13, name: "kg"}};
        const state = stateWithUoms();
        expect(state.scannedQuantity({...pinch, qty: null}, 13)).toBe(1);
        expect(state.scannedQuantity({...pinch, qty: 3, count: 3}, 13)).toBe(3);
        expect(state.scannedQuantity({...pinch, weight: 0, qty: null}, 13)).toBe(1);
        // The same 4 g is read when kilograms keep three decimals.
        expect(stateReadingGrams().scannedQuantity(pinch, 13)).toBe(0.004);
    });

    test("without a measure, the base reading stands", () => {
        const state = stateWithUoms();
        expect(state.scannedQuantity({qty: 7, count: 7}, 13)).toBe(7);
        expect(state.scannedQuantity({}, 13)).toBe(1);
        expect(state.scannedQuantity(null, 13)).toBe(1);
        // A unit we could not read leaves the stated quantity alone.
        expect(state.scannedQuantity(TWO_PIECES_OF_2497_G, 999)).toBe(2);
    });
});

describe("Gs1StockQuantity loading", () => {
    function fakeOrm({digits = 3, fail = false} = {}) {
        const calls = [];
        return {
            calls,
            async searchRead(model, domain, fields) {
                calls.push([model, fields]);
                return UOMS;
            },
            async call(model, method, args, kwargs) {
                calls.push([model, method, args, kwargs]);
                if (fail) {
                    throw new Error("No access");
                }
                return {quantity: {digits: [16, digits]}};
            },
        };
    }

    test("the units and the stored decimals are read once", async () => {
        const orm = fakeOrm();
        const state = new BarcodeScannerState(orm);
        await state.loadUoms();
        expect(state.uomsById[13].rounding).toBe(0.01);
        expect(state.quantityDigits).toBe(3);
        expect(orm.calls).toEqual([
            ["uom.uom", ["name", "category_id", "factor", "rounding"]],
            ["stock.move.line", "fields_get", [["quantity"]], {attributes: ["digits"]}],
        ]);
        await state.loadUoms();
        expect(orm.calls.length).toBe(2);
    });

    test("the units still load when the decimals cannot be read", async () => {
        const state = new BarcodeScannerState(fakeOrm({fail: true}));
        await state.loadUoms();
        expect(state.uomsById[13].name).toBe("kg");
        expect(state.quantityDigits).toBe(null);
    });

    test("units that failed to load are loaded again by the next measure", async () => {
        // The connection drops when the app opens, then comes back twice later.
        const outcomes = ["offline", "offline", "online"];
        const attempts = [];
        const orm = {
            async searchRead() {
                const outcome = outcomes[attempts.length];
                attempts.push(outcome);
                if (outcome === "offline") {
                    throw new Error("offline");
                }
                return UOMS;
            },
            async call() {
                return 2;
            },
        };
        const state = new BarcodeScannerState(orm);
        await state.loadUoms().catch(() => null);
        const weighed = {qty: null, weight: 2.497, weightUom: {id: 13, name: "kg"}};
        // A scan without a measure does not need the units.
        expect(state.scannedQuantity({qty: 2, count: 2}, 13)).toBe(2);
        expect(attempts.length).toBe(1);
        // One with a measure keeps the base reading and loads them again, once
        // however often it is read meanwhile.
        expect(state.scannedQuantity(weighed, 13)).toBe(1);
        expect(state.scannedQuantity(weighed, 13)).toBe(1);
        await state.uomsRetry;
        expect(attempts.length).toBe(2);
        // Still offline: the next measure tries again, and that one succeeds.
        expect(state.scannedQuantity(weighed, 13)).toBe(1);
        await state.uomsRetry;
        expect(attempts).toEqual(["offline", "offline", "online"]);
        expect(state.scannedQuantity(weighed, 13)).toBe(2.5);
    });
});

describe("Gs1StockQuantity packaging", () => {
    // The carton's own GTIN-14 (packaging indicator 1) holds twelve cheeses.
    const CARTON = "19501101020914";

    afterEach(() => setGs1Nomenclature(null));

    // The rules of Odoo's GS1 nomenclature these labels need, with the unit each
    // measure is expressed in.
    function loadNomenclature() {
        setGs1Nomenclature(
            compileGs1Nomenclature({id: 1, name: "Default GS1 Nomenclature"}, [
                {
                    name: "GTIN",
                    sequence: 2,
                    pattern: "(01)(\\d{14})",
                    type: "product",
                    gs1_content_type: "identifier",
                },
                {
                    name: "Variable count of items",
                    sequence: 20,
                    pattern: "(30)(\\d{0,8})",
                    type: "quantity",
                    gs1_content_type: "measure",
                    gs1_decimal_usage: false,
                },
                {
                    name: "Net weight, kilograms",
                    sequence: 21,
                    pattern: "(310[0-5])(\\d{6})",
                    type: "quantity",
                    gs1_content_type: "measure",
                    gs1_decimal_usage: true,
                    associated_uom_id: [13, "kg"],
                },
                {
                    name: "Net volume, litres",
                    sequence: 25,
                    pattern: "(315[0-5])(\\d{6})",
                    type: "quantity",
                    gs1_content_type: "measure",
                    gs1_decimal_usage: true,
                    associated_uom_id: [11, "L"],
                },
            ])
        );
    }

    // A picking with one move of cheese, whose carton is a packaging of 12.
    function pickingState(productUomId) {
        const state = stateWithUoms();
        state.productsById = {
            7: {
                id: 7,
                display_name: "Cheese",
                barcode: "9501101020917",
                uom_id: [productUomId, "unit"],
                tracking: "none",
            },
        };
        state.moves = [{id: 70, product_id: [7, "Cheese"]}];
        state.packagings = [
            {id: 3, product_id: [7, "Cheese"], barcode: CARTON, qty: 12},
        ];
        state.buildIndexes();
        return state;
    }

    function scan(state, label) {
        return state.applyScanResult({barcode: label, ...parseGs1(label)});
    }

    test("a carton label with no count is the pack's quantity", () => {
        loadNomenclature();
        // The weight is decoded, but a product counted in units ignores it.
        const result = scan(pickingState(1), `(01)${CARTON}(3103)004324`);
        expect(result.candidates.length).toBe(1);
        expect(result.quantity).toBe(12);
        expect(scan(pickingState(1), `(01)${CARTON}`).quantity).toBe(12);
    });

    test("a count on the carton label wins over the pack's quantity", () => {
        loadNomenclature();
        expect(scan(pickingState(1), `(01)${CARTON}(30)10`).quantity).toBe(10);
    });

    test("a carton weighed for a product stocked by weight is the weight", () => {
        loadNomenclature();
        // 4.324 kg, stored with Odoo's two decimals: not the pack's 12.
        const result = scan(pickingState(13), `(01)${CARTON}(3103)004324`);
        expect(result.quantity).toBe(4.32);
    });

    test("a carton labelled by weight and volume fits a product in litres", () => {
        loadNomenclature();
        const label = `(01)${CARTON}(3103)004324(3152)000450`;
        expect(scan(pickingState(11), label).quantity).toBe(4.5);
        expect(scan(pickingState(13), label).quantity).toBe(4.32);
    });

    test("a carton weight that rounds to nothing leaves the pack's quantity", () => {
        loadNomenclature();
        expect(scan(pickingState(13), `(01)${CARTON}(3103)000004`).quantity).toBe(12);
    });
});
