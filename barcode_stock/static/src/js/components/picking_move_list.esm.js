import {Component} from "@odoo/owl";
import {PickingMoveCard} from "./picking_move_card.esm";
import {isMovePending} from "@barcode_stock/js/utils/move_progress.esm";

export class PickingMoveList extends Component {
    showMove(move) {
        return isMovePending(move);
    }

    getMoveStats(move) {
        return (
            this.props.moveStatsById?.[move.id] || {
                demandQty: move.product_uom_qty || move.quantity || 0,
                doneQty: move.qty_done_total || 0,
                remainingQty: Math.max(
                    (move.quantity || 0) - (move.qty_done_total || 0),
                    0
                ),
                completionLabel: "0%",
            }
        );
    }
}

PickingMoveList.template = "barcode_scanner.PickingMoveList";
PickingMoveList.components = {PickingMoveCard};
PickingMoveList.props = {
    moves: {type: Array},
    moveLines: {type: Array, optional: true},
    moveStatsById: {type: Object, optional: true},
    highlightedMoveId: {type: [Number, "null"], optional: true},
    onOpenWizard: Function,
};
