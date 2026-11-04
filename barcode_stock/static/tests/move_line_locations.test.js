import {beforeEach, describe, expect, test} from "@odoo/hoot";
import {BarcodeScannerState} from "@barcode_stock/js/services/barcode_scanner_state.esm";
import {BarcodeScannerSync} from "@barcode_stock/js/services/barcode_scanner_sync.esm";
import {MoveWizardScreen} from "@barcode_stock/js/screens/move_wizard_screen.esm";
import {PickingScreen} from "@barcode_stock/js/screens/picking_screen.esm";
import {patchTranslations} from "@web/../tests/web_test_helpers";

const STOCK = [8, "WH/Stock"];
const SHELF_1 = [11, "WH/Stock/Shelf 1"];
const SHELF_2 = [12, "WH/Stock/Shelf 2"];
const OUTPUT = [13, "WH/Output"];
const LOT_A = {id: 21, name: "6077102", product_id: [7, "Duck confit"]};
const LOT_B = {id: 22, name: "6077103", product_id: [7, "Duck confit"]};

let lineId = 0;

/**
 * A line of move 5, reserved where Odoo found its stock.
 *
 * @param {Object} values the line's quantity, what was picked, its lot and
 *   locations
 * @returns {Object} the line
 */
function line({quantity, picked = 0, lot = false, from = SHELF_1, to = OUTPUT}) {
    lineId += 1;
    return {
        id: lineId,
        move_id: [5, "Duck confit"],
        product_id: [7, "Duck confit"],
        lot_id: lot ? [lot.id, lot.name] : false,
        quantity,
        qty_picked: picked,
        location_id: from,
        location_dest_id: to,
    };
}

/**
 * A move wizard on move 5 of picking 3, without mounting it. What it confirms
 * on the lines lands in `confirmed`, what it asks the server in `called`, what
 * it tells the operator in `notes`, and the lots it looks up in `lookedUp`,
 * found at `lotAt`.
 *
 * @param {Object} [options] the operation, the product's tracking, the move's
 *   lines, what the move still lacks, the lot scanned, where lots lie and
 *   whether the server refuses
 * @returns {MoveWizardScreen} the wizard
 */
function moveWizard({
    type = "internal",
    tracking = "none",
    lines = [],
    remaining = 5,
    defaultLot = null,
    lotAt = false,
    refused = false,
} = {}) {
    const wizard = Object.create(MoveWizardScreen.prototype);
    const move = {
        id: 5,
        product_id: [7, "Duck confit"],
        product_uom_qty: remaining,
        location_id: type === "incoming" ? [4, "Partners/Vendors"] : STOCK,
        location_dest_id: type === "incoming" ? STOCK : OUTPUT,
    };
    Object.assign(wizard, {
        props: {
            params: {moveId: 5, pickingId: 3, pickingTypeCode: type, defaultLot},
        },
        lookedUp: [],
        notes: [],
        called: [],
        flushed: 0,
        navigated: false,
        state: {
            selectedLotId: defaultLot ? String(defaultLot) : null,
            qtyPicked: 1,
            tracking: "none",
            mode: "pick",
            lots: [],
            useExistingLots: true,
            useCreateLots: type === "incoming",
            sourceLocation: null,
            destLocation: null,
        },
        barcodeScannerState: {
            ready: true,
            activePickingId: 3,
            useExistingLots: true,
            useCreateLots: type === "incoming",
            lotsById: {21: LOT_A, 22: LOT_B},
            getMove: () => move,
            getProduct: () => ({id: 7, tracking}),
            getMoveLinesForMove: () => lines,
            getLotsForProduct: () => [LOT_A, LOT_B],
            getRemainingQty: () => remaining,
            lotSourceLocation: async (productId, lotId, locationId) => {
                wizard.lookedUp.push([productId, lotId, locationId]);
                return lotAt;
            },
        },
        barcodeScannerSync: {
            validateConfirmMovePayload: () => null,
            confirmMove: async (payload) => {
                wizard.confirmed = payload;
            },
            flush: async () => {
                wizard.flushed += 1;
            },
        },
        feedback: {success: () => undefined},
        store: {
            navigate: () => {
                wizard.navigated = true;
            },
        },
        inventory: {
            notify: (message) => wizard.notes.push(String(message)),
            call: async (model, method, args) => {
                wizard.called.push([model, method, args]);
                if (refused) {
                    throw new Error("refused");
                }
                return true;
            },
        },
    });
    return wizard;
}

describe("BarcodeStock", () => {
    beforeEach(() => patchTranslations());

    test("a pick writes no location the operator did not choose", () => {
        const state = new BarcodeScannerState({});
        const reserved = line({quantity: 2});
        state.pickingTypeCode = "internal";
        state.moveLines = [reserved];
        const pick = {moveId: 5, pickingId: 3, productId: 7, qtyPicked: 2};
        state.stageMoveLine(pick);
        expect(reserved.location_id).toEqual(SHELF_1);
        expect(reserved.location_dest_id).toEqual(OUTPUT);
        const [sent] = state.sync.queue;
        expect("location_id" in sent.values).toBe(false);
        expect("location_dest_id" in sent.values).toBe(false);
        // One the operator chose is written.
        state.stageMoveLine({...pick, locationId: 12, locationDestId: 8});
        expect(state.sync.queue[0].values).toMatchObject({
            location_id: 12,
            location_dest_id: 8,
        });
    });

    test("outside receptions, a pick fills the reserved lines in turn", () => {
        const state = new BarcodeScannerState({});
        const first = line({quantity: 2, picked: 1});
        const second = line({quantity: 3, from: SHELF_2});
        state.pickingTypeCode = "internal";
        state.moveLines = [first, second];
        const pick = {moveId: 5, pickingId: 3, productId: 7, qtyPicked: 1};
        state.stageMoveLine(pick);
        expect(first.qty_picked).toBe(2);
        state.stageMoveLine(pick);
        expect(second.qty_picked).toBe(1);
        // A reception goes on the line with nothing picked yet, as before.
        const receipt = new BarcodeScannerState({});
        const started = line({quantity: 2, picked: 1});
        const untouched = line({quantity: 3});
        receipt.pickingTypeCode = "incoming";
        receipt.moveLines = [started, untouched];
        receipt.stageMoveLine(pick);
        expect(untouched.qty_picked).toBe(1);
    });

    test("a product without lots is picked line by line, from where it lies", async () => {
        const first = line({quantity: 2});
        const second = line({quantity: 3, from: SHELF_2});
        const wizard = moveWizard({lines: [first, second]});
        await wizard.loadData();
        expect(wizard.targetLine).toBe(first);
        expect(wizard.pickableQty).toBe(2);
        expect(wizard.shownSourceLocation).toEqual({
            id: 11,
            display_name: "WH/Stock/Shelf 1",
        });
        wizard.fulfillRemaining();
        await wizard.confirmPick();
        expect(wizard.confirmed).toMatchObject({
            moveLineId: first.id,
            qtyPicked: 2,
            locationId: false,
            locationDestId: false,
        });
        // The first line picked, the second one is next, from its own shelf.
        first.qty_picked = 2;
        const next = moveWizard({lines: [first, second], remaining: 3});
        await next.loadData();
        expect(next.targetLine).toBe(second);
        expect(next.shownSourceLocation.display_name).toBe("WH/Stock/Shelf 2");
    });

    test("only a location the operator chose is sent", async () => {
        const wizard = moveWizard({lines: [line({quantity: 2})]});
        await wizard.loadData();
        wizard.state.sourceLocation = {id: 12, display_name: "WH/Stock/Shelf 2"};
        expect(wizard.shownSourceLocation.display_name).toBe("WH/Stock/Shelf 2");
        await wizard.confirmPick();
        expect(wizard.confirmed).toMatchObject({locationId: 12, locationDestId: false});
    });

    test("the location shown follows the lot chosen", async () => {
        const wizard = moveWizard({
            tracking: "lot",
            lines: [
                line({quantity: 2, lot: LOT_A}),
                line({quantity: 3, lot: LOT_B, from: SHELF_2}),
            ],
        });
        await wizard.loadData();
        expect(wizard.state.selectedLotId).toBe("21");
        expect(wizard.shownSourceLocation.display_name).toBe("WH/Stock/Shelf 1");
        wizard.onLotChange({target: {value: "22"}});
        expect(wizard.shownSourceLocation.display_name).toBe("WH/Stock/Shelf 2");
    });

    test("a lot the reservation does not carry is picked by Odoo", async () => {
        // A delivery reserved lot A on Shelf 1; lot B lies on Shelf 2.
        const wizard = moveWizard({
            type: "outgoing",
            tracking: "lot",
            lines: [line({quantity: 2, lot: LOT_A})],
            lotAt: SHELF_2,
        });
        await wizard.loadData();
        expect(wizard.lookedUp).toEqual([]);
        await wizard.onLotChange({target: {value: "22"}});
        expect(wizard.lookedUp).toEqual([[7, 22, 8]]);
        expect(wizard.shownSourceLocation.display_name).toBe("WH/Stock/Shelf 2");
        await wizard.confirmPick();
        // Staged work first, then Odoo reserves and picks the lot where it lies.
        expect(wizard.flushed).toBe(1);
        expect(wizard.called).toEqual([
            ["stock.move", "barcode_pick_lot", [[5], 22, 1, false, false]],
        ]);
        expect(wizard.confirmed).toBe(undefined);
        expect(wizard.navigated).toBe(true);
        // Back on the reserved lot, its line's shelf again, and none written.
        await wizard.onLotChange({target: {value: "21"}});
        expect(wizard.shownSourceLocation.display_name).toBe("WH/Stock/Shelf 1");
        await wizard.confirmPick();
        expect(wizard.confirmed).toMatchObject({lotId: 21, locationId: false});
        expect(wizard.called.length).toBe(1);
    });

    test("confirming while the lot is still being looked up", async () => {
        // The lookup has not answered yet: the server picks the lot anyway.
        const wizard = moveWizard({
            tracking: "lot",
            lines: [line({quantity: 2, lot: LOT_A})],
            lotAt: new Promise(() => undefined),
        });
        await wizard.loadData();
        wizard.onLotChange({target: {value: "22"}});
        expect(wizard.state.lotLocation).toBe(null);
        await wizard.confirmPick();
        expect(wizard.called).toEqual([
            ["stock.move", "barcode_pick_lot", [[5], 22, 1, false, false]],
        ]);
        expect(wizard.confirmed).toBe(undefined);
    });

    test("a pick Odoo refuses keeps the wizard open", async () => {
        const wizard = moveWizard({
            tracking: "lot",
            lines: [line({quantity: 2, lot: LOT_A})],
            defaultLot: 22,
            lotAt: SHELF_2,
            refused: true,
        });
        await wizard.loadData();
        await wizard.confirmPick();
        expect(wizard.called.length).toBe(1);
        expect(wizard.navigated).toBe(false);
    });

    test("a scanned lot the reservation does not carry is looked up too", async () => {
        const wizard = moveWizard({
            tracking: "lot",
            lines: [line({quantity: 2, lot: LOT_A})],
            defaultLot: 22,
            lotAt: SHELF_2,
        });
        await wizard.loadData();
        expect(wizard.shownSourceLocation.display_name).toBe("WH/Stock/Shelf 2");
        // A source and a destination the operator chose are Odoo's to use.
        wizard.state.sourceLocation = {id: 8, display_name: "WH/Stock"};
        wizard.state.destLocation = {id: 12, display_name: "WH/Stock/Shelf 2"};
        await wizard.confirmPick();
        expect(wizard.called).toEqual([
            ["stock.move", "barcode_pick_lot", [[5], 22, 1, 8, 12]],
        ]);
    });

    test("a lot with no stock under the move's source is not picked", async () => {
        const nowhere = moveWizard({
            tracking: "lot",
            lines: [line({quantity: 2, lot: LOT_A})],
            defaultLot: 22,
        });
        await nowhere.loadData();
        const message = "Lot 6077103 has no stock in WH/Stock.";
        expect(nowhere.missingLotMessage).toBe(message);
        await nowhere.confirmPick();
        expect(nowhere.called).toEqual([]);
        expect(nowhere.notes).toEqual([message]);
        // Choosing where it comes from is the operator's way past it.
        nowhere.state.sourceLocation = {id: 12, display_name: "WH/Stock/Shelf 2"};
        expect(nowhere.missingLotMessage).toBe("");
        await nowhere.confirmPick();
        expect(nowhere.called).toEqual([
            ["stock.move", "barcode_pick_lot", [[5], 22, 1, 12, false]],
        ]);
        // A reserved lot is never looked up, nor held back.
        await nowhere.onLotChange({target: {value: "21"}});
        expect(nowhere.state.lotMissing).toBe(false);
        expect(nowhere.lookedUp).toEqual([[7, 22, 8]]);
    });

    test("where a lot lies is asked to the server, which knows the removal strategy", async () => {
        const asked = [];
        const state = new BarcodeScannerState({
            call: async (...args) => {
                asked.push(args);
                return SHELF_2;
            },
        });
        expect(await state.lotSourceLocation(7, 22, 8)).toEqual(SHELF_2);
        expect(asked).toEqual([["stock.quant", "barcode_lot_location", [7, 22, 8]]]);
    });

    test("the picking's lines are read with their locations", async () => {
        const read = {};
        const state = new BarcodeScannerState({
            searchRead: async (model, domain, fields) => {
                read[model] = fields;
                return model === "stock.picking"
                    ? [{id: 3, name: "WH/INT/003", picking_type_id: [2, "Internal"]}]
                    : [];
            },
            read: async () => [{code: "internal"}],
            call: async () => ({}),
        });
        await state.preloadPicking(3);
        expect(read["stock.move.line"]).toInclude("location_id");
        expect(read["stock.move.line"]).toInclude("location_dest_id");
    });

    test("a pick is spread over the reserved lines, each up to what it holds", () => {
        const state = new BarcodeScannerState({});
        const first = line({quantity: 2});
        const second = line({quantity: 3, from: SHELF_2});
        state.pickingTypeCode = "outgoing";
        state.moveLines = [first, second];
        const pick = {moveId: 5, pickingId: 3, productId: 7};
        // A scan of 5 (a GS1 count, say) takes 2 from Shelf 1 and 3 from Shelf 2.
        state.stagePick({...pick, qtyPicked: 5});
        expect([first.qty_picked, second.qty_picked]).toEqual([2, 3]);
        // What is over goes on the last of them.
        state.stagePick({...pick, qtyPicked: 1});
        expect([first.qty_picked, second.qty_picked]).toEqual([2, 4]);
        // A reception is not spread.
        const receipt = new BarcodeScannerState({});
        const only = line({quantity: 3});
        receipt.pickingTypeCode = "incoming";
        receipt.moveLines = [only, line({quantity: 2})];
        receipt.stagePick({...pick, qtyPicked: 5});
        expect(only.qty_picked).toBe(5);
    });

    test("a confirmation is spread the same way", async () => {
        const state = new BarcodeScannerState({});
        const first = line({quantity: 2});
        const second = line({quantity: 3, from: SHELF_2});
        state.pickingTypeCode = "internal";
        state.moveLines = [first, second];
        const sync = new BarcodeScannerSync({}, state);
        sync.schedule = () => undefined;
        await sync.confirmMove(
            {moveId: 5, pickingId: 3, productId: 7, qtyPicked: 5, moveLineId: first.id},
            {immediate: false}
        );
        expect([first.qty_picked, second.qty_picked]).toEqual([2, 3]);
    });

    test("outside receptions, a lot the reservation lacks takes no other lot's line", () => {
        const state = new BarcodeScannerState({});
        const reserved = line({quantity: 2, lot: LOT_A});
        state.pickingTypeCode = "outgoing";
        state.moveLines = [reserved];
        state.stageMoveLine({
            moveId: 5,
            pickingId: 3,
            productId: 7,
            qtyPicked: 2,
            lotId: 22,
            lotName: "6077103",
        });
        expect(reserved.lot_id).toEqual([21, "6077102"]);
        expect(reserved.qty_picked).toBe(0);
        expect(state.moveLines.length).toBe(2);
        // A reception's lotless reserved line is still taken over.
        const receipt = new BarcodeScannerState({});
        const lotless = line({quantity: 3});
        receipt.pickingTypeCode = "incoming";
        receipt.moveLines = [lotless];
        receipt.stageMoveLine({
            moveId: 5,
            pickingId: 3,
            productId: 7,
            qtyPicked: 3,
            lotId: 22,
            lotName: "6077103",
        });
        expect(lotless.lot_id).toBe(22);
        expect(receipt.moveLines.length).toBe(1);
    });

    test("a reception shows its line's putaway shelf and keeps it", async () => {
        const wizard = moveWizard({
            type: "incoming",
            lines: [line({quantity: 3, from: [4, "Partners/Vendors"], to: SHELF_2})],
            remaining: 3,
        });
        await wizard.loadData();
        expect(wizard.targetLine).toBe(null);
        expect(wizard.shownDestLocation.display_name).toBe("WH/Stock/Shelf 2");
        await wizard.confirmPick();
        expect(wizard.confirmed).toMatchObject({locationDestId: false});
    });

    test("a re-scan in the picking sends no location", async () => {
        const screen = Object.create(PickingScreen.prototype);
        const sent = [];
        const move = {id: 5, product_id: [7, "Duck confit"], location_id: STOCK};
        Object.assign(screen, {
            props: {},
            state: {
                picking: {id: 3},
                moveLines: [line({quantity: 2, picked: 1})],
            },
            barcodeScannerState: {
                applyScanResult: () => ({candidates: [move], quantity: 1}),
                indexes: {trackingByProductId: {7: "none"}},
            },
            barcodeScannerSync: {confirmMove: async (payload) => sent.push(payload)},
            feedback: {success: () => undefined},
            setLastScanContext: () => undefined,
            _reloadMoves: async () => undefined,
        });
        await screen.handleBarcode("DUCK");
        expect(sent.length).toBe(1);
        expect("locationId" in sent[0]).toBe(false);
        expect("locationDestId" in sent[0]).toBe(false);
    });
});
