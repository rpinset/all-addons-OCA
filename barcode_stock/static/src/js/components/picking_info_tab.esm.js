import {Component} from "@odoo/owl";

/**
 * Wrap a typed note as a paragraph, escaping it first: an operator may well
 * write "5 < 10", and the note is stored in an HTML field.
 */
function noteToHtml(text) {
    const escaped = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
    return `<p>${escaped}</p>`;
}

export class PickingInfoTab extends Component {
    get notePlainText() {
        const note = this.props.picking?.note;
        if (!note) return "";
        const tmp = document.createElement("div");
        tmp.innerHTML = note;
        return tmp.textContent || tmp.innerText || "";
    }

    onNoteInput(ev) {
        const text = ev.target.value.trim();
        this.props.picking.note = text ? noteToHtml(text) : "";
    }

    onSelectResponsible() {
        this.props.onSelectResponsible?.();
    }
}

PickingInfoTab.template = "barcode_scanner.PickingInfoTab";
PickingInfoTab.props = {
    picking: Object,
    pickingTypeCode: {type: String, optional: true},
    progressLabel: {type: String, optional: true},
    onSelectResponsible: {type: Function, optional: true},
};
