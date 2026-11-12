import {afterEach, describe, expect, test} from "@odoo/hoot";
import {roundQty, setQuantityDecimals} from "@barcode_stock/js/utils/quantity.esm";
import {BarcodeScannerState} from "@barcode_stock/js/services/barcode_scanner_state.esm";
import {InternalTransferScreen} from "@barcode_stock/js/screens/internal_transfer_screen.esm";
import {MoveWizardScreen} from "@barcode_stock/js/screens/move_wizard_screen.esm";
import {PickingScreen} from "@barcode_stock/js/screens/picking_screen.esm";
import {barcodeStartupTasks} from "@barcode_scanner/js/registries.esm";

/**
 * A reception's move wizard on a move of `demand`, with `remaining` left of it
 * and `qtyPicked` to pick, without mounting it.
 *
 * @param {Object} quantities the move's demand, what is left, what is picked
 * @returns {MoveWizardScreen} the wizard
 */
function moveWizard({demand, remaining, qtyPicked = 1}) {
    const wizard = Object.create(MoveWizardScreen.prototype);
    wizard.props = {params: {moveId: 5, pickingTypeCode: "incoming"}};
    wizard.state = {
        move: {id: 5, quantity: demand},
        moveLines: [],
        qtyPicked,
        tracking: "none",
    };
    wizard.barcodeScannerState = {getRemainingQty: () => remaining};
    return wizard;
}

describe("BarcodeStock", () => {
    afterEach(() => setQuantityDecimals(null));

    test("a quantity worked out from others drops the float noise", () => {
        // 100 - 87.08, as a move of 100 with 12.92 picked shows it.
        expect(roundQty(100 - (100 - 12.92))).toBe(12.92);
        expect(roundQty(0.1 + 0.7)).toBe(0.8);
        expect(roundQty(0.8 - (0.1 + 0.7))).toBe(0);
        // Unknown decimals change no real quantity.
        expect(roundQty(0.125)).toBe(0.125);
        expect(roundQty("3.5")).toBe(3.5);
        // Known, they round as the server stores the quantity.
        setQuantityDecimals(2);
        expect(roundQty(2.497)).toBe(2.5);
        setQuantityDecimals(3);
        expect(roundQty(2.497)).toBe(2.497);
    });

    test("the move wizard shows what is picked and left without noise", () => {
        const wizard = moveWizard({demand: 100, remaining: 100 - 12.92});
        expect(wizard.doneQty).toBe(12.92);
        expect(wizard.fulfillIncrement).toBe(86.08);
        wizard.state.qtyPicked = 2.53;
        expect(wizard.fulfillIncrement).toBe(84.55);
        // Labels of 0.1 and 0.2 add up to 0.3.
        wizard.state.qtyPicked = 0.1;
        wizard.adjustQty(0.2);
        expect(wizard.state.qtyPicked).toBe(0.3);
        // Nothing left to fulfil once the move is picked.
        const done = moveWizard({demand: 0.8, remaining: 0, qtyPicked: 0});
        expect(done.canFulfill).toBe(false);
    });

    test("the decimals quantities are stored with are read at start-up", async () => {
        const calls = [];
        const state = new BarcodeScannerState({
            call: async (...args) => {
                calls.push(args);
                return {quantity: {digits: [16, 2]}};
            },
        });
        const task = barcodeStartupTasks.get("stock_quantity_decimals");
        await task({services: {barcodeScannerState: state}});
        expect(calls).toEqual([
            ["stock.move.line", "fields_get", [["quantity"]], {attributes: ["digits"]}],
        ]);
        expect(roundQty(2.497)).toBe(2.5);
    });

    test("a reply without decimals keeps dropping only the noise", async () => {
        const replies = [
            {quantity: {digits: [16, 2]}},
            {quantity: {digits: false}},
            {quantity: {digits: [16, "2"]}},
            {},
            null,
        ];
        const state = new BarcodeScannerState({call: async () => replies.shift()});
        await state.loadQuantityDecimals();
        expect(roundQty(2.497)).toBe(2.5);
        while (replies.length) {
            await state.loadQuantityDecimals();
            expect(roundQty(2.497)).toBe(2.497);
            expect(roundQty(0.1 + 0.7)).toBe(0.8);
        }
        // A failed call leaves the rounding as it was.
        const failing = new BarcodeScannerState({
            call: async () => {
                throw new Error("offline");
            },
        });
        await expect(failing.loadQuantityDecimals()).rejects.toThrow("offline");
        expect(roundQty(2.497)).toBe(2.497);
    });

    test("a move picked in decimals is left with nothing to pick", () => {
        const state = new BarcodeScannerState({});
        state.getMove = () => ({id: 5, quantity: 0.8});
        state.getMoveLinesForMove = () => [{qty_picked: 0.1}, {qty_picked: 0.7}];
        expect(state.getRemainingQty(5)).toBe(0);
        // Picks added on a line add up without noise.
        const line = {
            id: 1,
            move_id: [5, "Ham"],
            product_id: [7, "Ham"],
            lot_id: false,
            quantity: 1,
            qty_picked: 0,
        };
        state.moveLines = [line];
        const pick = {moveId: 5, pickingId: 3, productId: 7, moveLineId: 1};
        state.stageMoveLine({...pick, qtyPicked: 0.1});
        state.stageMoveLine({...pick, qtyPicked: 0.2});
        expect(line.qty_picked).toBe(0.3);
    });

    test("the picking screen counts a move picked in decimals as done", () => {
        const screen = Object.create(PickingScreen.prototype);
        screen.state = {
            moves: [{id: 5, product_uom_qty: 0.8, quantity: 0.8}],
            moveLines: [
                {move_id: [5, "Ham"], qty_picked: 0.1},
                {move_id: [5, "Ham"], qty_picked: 0.7},
            ],
        };
        expect(screen.moveStatsById[5]).toMatchObject({
            doneQty: 0.8,
            remainingQty: 0,
        });
        expect(screen.pendingMovesCount).toBe(0);
        expect(screen.progressSummary.doneQty).toBe(0.8);
    });

    test("an internal transfer line adds up scans and an edited quantity", async () => {
        const screen = Object.create(InternalTransferScreen.prototype);
        const line = {product_id: 7, lot_id: false, qty: 0.1, tracking: "none"};
        screen.state = {lines: [line]};
        await screen.addLine({id: 7}, false, false, 0.2);
        expect(line.qty).toBe(0.3);
        // The input hands an edited quantity back as text.
        line.qty = "2";
        await screen.addLine({id: 7}, false, false, 1);
        expect(line.qty).toBe(3);
    });
});
