/**
 * A move belongs to the "To Do" list while the picked quantity has not caught
 * up with what the picking reserved; from then on only the "Done" tab renders
 * it. The rule lives here so the list that hides a move and the screen that
 * sends a scan to a tab can never disagree -- when they did, scanning a line
 * that was already complete jumped to "To Do" and showed nothing but the
 * notification.
 *
 * @param {Object} move
 * @returns {Boolean}
 */
export function isMovePending(move) {
    if (!move) {
        return false;
    }
    return move.quantity === 0 || move.qty_done_total < move.quantity;
}

/**
 * The tab that actually renders the given move.
 *
 * @param {Object} move
 * @returns {String}
 */
export function tabForMove(move) {
    return isMovePending(move) ? "todo" : "done";
}
