import {beforeEach, describe, expect, test} from "@odoo/hoot";
import {BarcodeScannerState} from "@barcode_stock/js/services/barcode_scanner_state.esm";
import {MoveWizardScreen} from "@barcode_stock/js/screens/move_wizard_screen.esm";
import {PickingScreen} from "@barcode_stock/js/screens/picking_screen.esm";
import {patchTranslations} from "@web/../tests/web_test_helpers";

const LOT_A = {id: 21, name: "6077102", product_id: [7, "Duck confit"], product_qty: 4};
const LOT_B = {id: 22, name: "6077103", product_id: [7, "Duck confit"], product_qty: 9};

/**
 * A move wizard on move 5 of picking 3, without mounting it. What it confirms
 * lands in `confirmed`.
 *
 * @param {Object} [options] the operation, the move's lines and the lot and
 *   quantity given
 * @returns {MoveWizardScreen} the wizard
 */
function moveWizard({
    type = "outgoing",
    lines = [],
    defaultLot = null,
    defaultQty = null,
    tracking = "lot",
    remaining = 4,
} = {}) {
    const wizard = Object.create(MoveWizardScreen.prototype);
    wizard.props = {
        params: {
            moveId: 5,
            pickingId: 3,
            pickingTypeCode: type,
            defaultLot,
            defaultQty,
        },
    };
    wizard.state = {
        selectedLotId: defaultLot ? String(defaultLot) : null,
        qtyPicked: defaultQty || 1,
        tracking: "none",
        mode: "pick",
        lots: [],
        useExistingLots: true,
        useCreateLots: false,
        sourceLocation: null,
        destLocation: null,
    };
    wizard.barcodeScannerState = {
        ready: true,
        activePickingId: 3,
        useExistingLots: true,
        useCreateLots: type === "incoming",
        lotsById: {21: LOT_A, 22: LOT_B},
        getMove: () => ({
            id: 5,
            product_id: [7, "Duck confit"],
            product_uom_qty: 4,
            location_id: [8, "WH/Stock"],
            location_dest_id: [9, "Customers"],
        }),
        getProduct: () => ({id: 7, tracking}),
        getMoveLinesForMove: () => lines,
        getLotsForProduct: () => [LOT_B],
        getRemainingQty: () => remaining,
        lotSourceLocation: async () => false,
    };
    Object.assign(wizard, {
        feedback: {success: () => undefined},
        barcodeScannerSync: {
            validateConfirmMovePayload: () => null,
            confirmMove: async (payload) => {
                wizard.confirmed = payload;
            },
        },
        store: {navigate: () => undefined},
        inventory: {notify: () => undefined},
    });
    return wizard;
}

let lineId = 0;

function line(lotId, quantity, qtyPicked = 0) {
    lineId += 1;
    return {
        id: lineId,
        move_id: [5, "Duck confit"],
        product_id: [7, "Duck confit"],
        lot_id: lotId ? [lotId, lotId === 21 ? "6077102" : "6077103"] : false,
        quantity,
        qty_picked: qtyPicked,
    };
}

describe("BarcodeStock", () => {
    // `_t()` texts become strings only once translations are loaded.
    beforeEach(() => patchTranslations());

    test("a move reserved against a lot opens with that lot chosen", async () => {
        const wizard = moveWizard({lines: [line(21, 4)]});
        await wizard.loadData();
        expect(wizard.state.selectedLotId).toBe("21");
        // Listed even if the lots offered had left it out.
        expect(wizard.state.lots.map((lot) => lot.id)).toEqual([21, 22]);
    });

    test("the next reserved lot once the first one is picked", async () => {
        const wizard = moveWizard({lines: [line(21, 2, 2), line(22, 2)]});
        await wizard.loadData();
        expect(wizard.state.selectedLotId).toBe("22");
        // Everything picked: no lot is chosen for the operator.
        const done = moveWizard({lines: [line(21, 2, 2), line(22, 2, 2)]});
        await done.loadData();
        expect(done.state.selectedLotId).toBe(null);
    });

    test("a scanned lot, a reception or an untracked product keep their way", async () => {
        const scanned = moveWizard({lines: [line(21, 4)], defaultLot: 22});
        await scanned.loadData();
        expect(scanned.state.selectedLotId).toBe("22");
        const receipt = moveWizard({type: "incoming", lines: [line(21, 4)]});
        await receipt.loadData();
        expect(receipt.state.selectedLotId).toBe(null);
        const untracked = moveWizard({tracking: "none", lines: [line(21, 4)]});
        await untracked.loadData();
        expect(untracked.state.selectedLotId).toBe(null);
        const noLot = moveWizard({lines: [line(null, 4)]});
        await noLot.loadData();
        expect(noLot.state.selectedLotId).toBe(null);
    });

    test("Fulfill completes the chosen lot's reservation, not the whole move", async () => {
        // 4 reserved over two lots, 2 each.
        const wizard = moveWizard({lines: [line(21, 2), line(22, 2)]});
        await wizard.loadData();
        expect(wizard.state.selectedLotId).toBe("21");
        expect(wizard.pickableQty).toBe(2);
        expect(wizard.fulfillIncrement).toBe(1);
        expect(wizard.quantityHelper).toBe("2 remaining to process");
        wizard.fulfillRemaining();
        expect(wizard.state.qtyPicked).toBe(2);
        expect(wizard.canFulfill).toBe(false);
        // Lot A picked, the wizard opens on lot B with what is left of it.
        const next = moveWizard({lines: [line(21, 2, 2), line(22, 2)], remaining: 2});
        await next.loadData();
        expect(next.state.selectedLotId).toBe("22");
        next.fulfillRemaining();
        expect(next.state.qtyPicked).toBe(2);
    });

    test("a lot with nothing reserved left fulfils what the move lacks", async () => {
        // The operator picks lot A again, its reservation already picked.
        const wizard = moveWizard({
            lines: [line(21, 2, 2), line(22, 2)],
            defaultLot: 21,
            remaining: 2,
        });
        await wizard.loadData();
        expect(wizard.state.selectedLotId).toBe("21");
        expect(wizard.pickableQty).toBe(2);
        // No lot chosen at all: the move's remaining, as before.
        const none = moveWizard({tracking: "none", remaining: 3});
        await none.loadData();
        expect(none.pickableQty).toBe(3);
    });

    test("a lot reserved over several lines is picked line by line", async () => {
        // 9 reserved: lot A over two lines (2 + 3), lot B on one.
        const [a1, a2, b] = [line(21, 2), line(21, 3), line(22, 4)];
        const wizard = moveWizard({lines: [a1, a2, b], remaining: 9});
        await wizard.loadData();
        expect(wizard.state.selectedLotId).toBe("21");
        expect(wizard.targetLine).toBe(a1);
        wizard.fulfillRemaining();
        expect(wizard.state.qtyPicked).toBe(2);
        // Confirmed on that very line.
        await wizard.confirmPick();
        expect(wizard.confirmed).toMatchObject({
            moveLineId: a1.id,
            lotId: 21,
            qtyPicked: 2,
        });
        // Its first line picked, lot A goes on with its second one.
        a1.qty_picked = 2;
        const next = moveWizard({lines: [a1, a2, b], remaining: 7});
        await next.loadData();
        expect(next.state.selectedLotId).toBe("21");
        expect(next.targetLine).toBe(a2);
        expect(next.pickableQty).toBe(3);
        // Lot A covered, even if over-picked on its first line: on to lot B.
        a1.qty_picked = 5;
        const last = moveWizard({lines: [a1, a2, b], remaining: 4});
        await last.loadData();
        expect(last.state.selectedLotId).toBe("22");
        expect(last.targetLine).toBe(b);
        expect(last.pickableQty).toBe(4);
    });

    test("a pick goes on the reserved line named", () => {
        const state = new BarcodeScannerState({});
        const [a1, a2] = [line(21, 2), line(21, 3)];
        state.moveLines = [a1, a2];
        const pick = {moveId: 5, pickingId: 3, productId: 7, lotId: 21};
        state.stageMoveLine({...pick, qtyPicked: 3, moveLineId: a2.id});
        expect(a2.qty_picked).toBe(3);
        expect(a1.qty_picked).toBe(0);
        // None named: on the lot's line with nothing picked yet, as before.
        state.stageMoveLine({...pick, qtyPicked: 1});
        expect(a1.qty_picked).toBe(1);
        // One of another move is not taken.
        state.stageMoveLine({...pick, moveId: 6, qtyPicked: 1, moveLineId: a1.id});
        expect(a1.qty_picked).toBe(1);
    });

    test("a tapped move starts at no more than its lot's reservation holds", async () => {
        const tapped = moveWizard({lines: [line(21, 0.5)]});
        await tapped.loadData();
        expect(tapped.state.selectedLotId).toBe("21");
        expect(tapped.state.qtyPicked).toBe(0.5);
        // Still one unit when the lot holds more.
        const more = moveWizard({lines: [line(21, 3)]});
        await more.loadData();
        expect(more.state.qtyPicked).toBe(1);
        // A scan's quantity stands.
        const scanned = moveWizard({lines: [line(21, 0.5)], defaultQty: 1});
        await scanned.loadData();
        expect(scanned.state.qtyPicked).toBe(1);
    });

    test("only a scan hands the wizard a quantity", () => {
        const screen = Object.create(PickingScreen.prototype);
        const opened = [];
        screen.props = {};
        screen.state = {picking: {id: 3}, pickingTypeCode: "outgoing"};
        screen.store = {navigate: (name, params) => opened.push(params.defaultQty)};
        const move = {id: 5, quantity: 4};
        screen.openMoveWizard(move);
        screen.openMoveWizard(move, {qty: 6});
        expect(opened).toEqual([null, 6]);
    });

    test("a reception fulfils what the move lacks, whatever its lot's lines hold", async () => {
        const receipt = moveWizard({
            type: "incoming",
            lines: [line(21, 1)],
            defaultLot: 21,
            remaining: 4,
        });
        await receipt.loadData();
        expect(receipt.pickableQty).toBe(4);
        receipt.fulfillRemaining();
        expect(receipt.state.qtyPicked).toBe(4);
    });
});
