import {Component} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";

export class PickingMoveCard extends Component {
    get linesForMove() {
        if (!this.props.moveLines) {
            return [];
        }
        // Only list lines that already carry a lot/serial and still have
        // something pending. Reserved lines without a lot showed up as noisy,
        // repeated "No lot" rows -- one per unit on a serial move -- while the
        // demand/done/remaining figures already cover the untracked case.
        return this.props.moveLines.filter(
            (line) =>
                line.move_id?.[0] === this.props.move.id &&
                line.lot_id &&
                line.quantity > 0 &&
                line.qty_picked < line.quantity
        );
    }

    get remainingQty() {
        return this.props.stats?.remainingQty ?? 0;
    }

    get doneQty() {
        return this.props.stats?.doneQty ?? this.props.move.qty_done_total ?? 0;
    }

    get demandQty() {
        return (
            this.props.stats?.demandQty ??
            this.props.move.quantity ??
            this.props.move.product_uom_qty ??
            0
        );
    }

    get pendingLabel() {
        return _t("pending");
    }
}

PickingMoveCard.template = "barcode_scanner.PickingMoveCard";
PickingMoveCard.props = {
    move: Object,
    moveLines: {type: Array, optional: true},
    stats: {type: Object, optional: true},
    highlighted: {type: Boolean, optional: true},
    onClick: Function,
};
