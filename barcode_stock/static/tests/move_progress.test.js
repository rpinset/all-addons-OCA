import {describe, expect, test} from "@odoo/hoot";
import {isMovePending, tabForMove} from "@barcode_stock/js/utils/move_progress.esm";

describe("BarcodeStock", () => {
    test("a move is pending until the picked quantity reaches the reserved one", () => {
        expect(isMovePending({quantity: 5, qty_done_total: 0})).toBe(true);
        expect(isMovePending({quantity: 5, qty_done_total: 4.5})).toBe(true);
        // Nothing reserved: the move is still offered for scanning.
        expect(isMovePending({quantity: 0, qty_done_total: 0})).toBe(true);
        // Complete, and over-picked past the reservation.
        expect(isMovePending({quantity: 5, qty_done_total: 5})).toBe(false);
        expect(isMovePending({quantity: 5, qty_done_total: 7})).toBe(false);
        expect(isMovePending(null)).toBe(false);
    });

    test("a scan lands on the tab that renders the line", () => {
        // The To Do list hides a completed move, so a scan on one has to open
        // the Done tab or the operator sees a list without their line.
        expect(tabForMove({quantity: 5, qty_done_total: 2})).toBe("todo");
        expect(tabForMove({quantity: 5, qty_done_total: 5})).toBe("done");
    });
});
