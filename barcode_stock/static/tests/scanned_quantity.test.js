import {describe, expect, test} from "@odoo/hoot";
import {BarcodeScannerState} from "@barcode_stock/js/services/barcode_scanner_state.esm";

describe("BarcodeStock", () => {
    test("a scan counts as one unit unless the barcode states a quantity", () => {
        const state = new BarcodeScannerState({});
        // A plain product barcode says nothing about how many.
        expect(state.scannedQuantity({value: "9501101020917"}, 13)).toBe(1);
        expect(state.scannedQuantity({}, null)).toBe(1);
        expect(state.scannedQuantity(null, null)).toBe(1);
        // A barcode that states one is taken at its word.
        expect(state.scannedQuantity({qty: 12}, 13)).toBe(12);
        expect(state.scannedQuantity({quantity: 2.5}, 13)).toBe(2.5);
        // Nonsense and zero both mean a single unit.
        expect(state.scannedQuantity({qty: "abc"}, 13)).toBe(1);
        expect(state.scannedQuantity({qty: 0}, 13)).toBe(1);
    });
});
