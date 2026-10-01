import {Component} from "@odoo/owl";
import {PickingDoneCard} from "./picking_done_card.esm";

export class PickingDoneList extends Component {
    get doneLines() {
        return this.props.lines.filter((line) => line.qty_picked > 0);
    }
}

PickingDoneList.template = "barcode_scanner.PickingDoneList";
PickingDoneList.components = {PickingDoneCard};
PickingDoneList.props = {
    lines: {type: Array},
    highlightedMoveId: {type: [Number, "null"], optional: true},
    onDeleteLine: Function,
};
