import {describe, expect, test} from "@odoo/hoot";
import {PickingInfoTab} from "@barcode_stock/js/components/picking_info_tab.esm";

describe("BarcodeStock", () => {
    test("a typed note is escaped before it is stored as HTML", () => {
        const tab = Object.create(PickingInfoTab.prototype);
        const picking = {note: ""};
        tab.props = {picking};

        tab.onNoteInput({target: {value: "  pick 5 < 10 & check  "}});
        expect(picking.note).toBe("<p>pick 5 &lt; 10 &amp; check</p>");

        // What the operator typed is what they read back.
        tab.props = {picking};
        expect(tab.notePlainText).toBe("pick 5 < 10 & check");

        // Markup an operator could type is stored as text, never as tags.
        tab.onNoteInput({target: {value: "<b>bold</b>"}});
        expect(picking.note).toBe("<p>&lt;b&gt;bold&lt;/b&gt;</p>");
        expect(tab.notePlainText).toBe("<b>bold</b>");

        // An emptied field clears the note instead of storing "<p></p>".
        tab.onNoteInput({target: {value: "   "}});
        expect(picking.note).toBe("");
    });
});
