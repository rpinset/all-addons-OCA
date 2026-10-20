import {Component, useState, xml} from "@odoo/owl";
import {describe, expect, test} from "@odoo/hoot";
import {getService, mountWithCleanup} from "@web/../tests/web_test_helpers";
import {animationFrame} from "@odoo/hoot-dom";
import {useBarcode} from "@barcode_scanner/js/hooks/use_barcode.esm";

class Reader extends Component {
    static template = xml`<div class="o-reader"/>`;
    static props = {onScan: Function};
    setup() {
        useBarcode((ev) => this.props.onScan(ev.detail.barcode));
    }
}

class Screen extends Component {
    static template = xml`<Reader t-if="state.reading" onScan="props.onScan"/>`;
    static components = {Reader};
    static props = {onScan: Function};
    setup() {
        this.state = useState({reading: true});
    }
}

describe("BarcodeScanner", () => {
    test("the components reading scans are counted while mounted", async () => {
        const scanned = [];
        const screen = await mountWithCleanup(Screen, {
            props: {onScan: (barcode) => scanned.push(barcode)},
        });
        const barcode = getService("barcodeScannerBarcode");
        expect(barcode.readers.count).toBe(1);
        barcode.bus.trigger("barcode_scanned", {barcode: "9501101020917"});
        expect(scanned).toEqual(["9501101020917"]);

        screen.state.reading = false;
        await animationFrame();
        expect(barcode.readers.count).toBe(0);
        barcode.bus.trigger("barcode_scanned", {barcode: "9501101020917"});
        expect(scanned.length).toBe(1);
    });
});
