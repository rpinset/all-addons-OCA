import {
    getService,
    mockService,
    mountWithCleanup,
    patchWithCleanup,
} from "@web/../tests/web_test_helpers";
import {Component, useState, xml} from "@odoo/owl";
import {animationFrame, click, waitFor, waitForNone} from "@odoo/hoot-dom";
import {describe, expect, test} from "@odoo/hoot";
import {BarcodeDialog} from "@web/core/barcode/barcode_dialog";
import {CameraFab} from "@barcode_camera/js/camera_fab.esm";
import {barcodeAppWidgets} from "@barcode_scanner/js/registries.esm";
import {browser} from "@web/core/browser/browser";
import {useBarcodeHandler} from "@barcode_scanner/js/hooks/use_barcode_handler.esm";

// A browser that can open the camera.
function withCamera() {
    patchWithCleanup(browser.navigator, {
        mediaDevices: {getUserMedia: () => Promise.resolve()},
    });
}

/**
 * A camera button, without mounting it, while `reading` screens read scans.
 * `dialog` plays the part of Odoo's scanner dialog: it gets the dialog's props
 * and options and answers the way the camera would. What the button feeds the
 * scanner bus lands in `scans`.
 */
function cameraFab({reading = 1, dialog = () => undefined} = {}) {
    withCamera();
    const fab = Object.create(CameraFab.prototype);
    const scans = [];
    const dialogs = [];
    fab.env = {
        services: {
            dialog: {
                add(component, props, options) {
                    dialogs.push({component, props});
                    dialog(props, options);
                },
            },
        },
    };
    fab.readers = {count: reading};
    fab.barcode = {
        bus: {trigger: (name, payload) => scans.push({name, payload})},
        parseBarcode: (barcode) => ({type: "product", value: barcode}),
    };
    fab.state = {scanning: false};
    return {fab, scans, dialogs};
}

// What Odoo's dialog does once the camera reads a code: it closes itself, then
// hands the code over.
function readsCode(code) {
    return (props, options) => {
        options.onClose();
        props.onResult(code);
    };
}

// A screen of the app, with the camera button the app shell renders next to
// it. Whether it reads scans is up to `state.reading`.
class Reader extends Component {
    static template = xml`<div class="o-reader"/>`;
    static props = {onScan: Function};
    setup() {
        useBarcodeHandler({onScan: (barcode) => this.props.onScan(barcode)});
    }
}

class AppScreen extends Component {
    static template = xml`<Reader t-if="state.reading" onScan="props.onScan"/><CameraFab/>`;
    static components = {Reader, CameraFab};
    static props = {onScan: Function};
    setup() {
        this.state = useState({reading: false});
    }
}

describe("BarcodeCamera", () => {
    test("the button joins the app through the widgets registry", () => {
        expect(barcodeAppWidgets.get("camera_fab").component).toBe(CameraFab);
    });

    test("the button follows the screens reading scans, and feeds them", async () => {
        withCamera();
        const opened = [];
        mockService("dialog", {
            add(component, props, options) {
                opened.push(component);
                readsCode("9501101020917")(props, options);
                return () => undefined;
            },
        });
        const scanned = [];
        const screen = await mountWithCleanup(AppScreen, {
            props: {onScan: (barcode) => scanned.push(barcode)},
        });
        // The warehouse picker, say, reads no scan.
        expect(".barcode-camera-fab").toHaveCount(0);

        // The screen counts once mounted; the button follows on the next render.
        screen.state.reading = true;
        await waitFor(".barcode-camera-fab");
        expect(getService("barcodeScannerBarcode").readers.count).toBe(1);
        expect(".barcode-camera-fab").toHaveAttribute("aria-label", "Camera scan");
        expect(".barcode-camera-fab").toHaveAttribute("title", "Camera scan");

        await click(".barcode-camera-fab");
        await animationFrame();
        expect(opened).toEqual([BarcodeDialog]);
        expect(scanned).toEqual(["9501101020917"]);
        expect(".barcode-camera-fab").toHaveCount(1);

        screen.state.reading = false;
        await waitForNone(".barcode-camera-fab");
        expect(getService("barcodeScannerBarcode").readers.count).toBe(0);
    });

    test("the button shows while the screen on display reads a scan", () => {
        expect(cameraFab({reading: 1}).fab.isVisible).toBe(true);
        expect(cameraFab({reading: 0}).fab.isVisible).toBe(false);
    });

    test("the button hides when the browser cannot open the camera", () => {
        const {fab} = cameraFab();
        // Outside a secure context (plain HTTP) there is no mediaDevices at all.
        patchWithCleanup(browser.navigator, {mediaDevices: undefined});
        expect(fab.isVisible).toBe(false);
        patchWithCleanup(browser.navigator, {mediaDevices: {}});
        expect(fab.isVisible).toBe(false);
    });

    test("a code the camera reads is scanned like a hardware scan", async () => {
        const {fab, scans, dialogs} = cameraFab({dialog: readsCode("9501101020917")});
        await fab.onScanClick();
        expect(dialogs[0].component).toBe(BarcodeDialog);
        expect(dialogs[0].props.facingMode).toBe("environment");
        expect(scans).toEqual([
            {
                name: "barcode_scanned",
                payload: {
                    barcode: "9501101020917",
                    parsed: {type: "product", value: "9501101020917"},
                    source: "camera",
                },
            },
        ]);
        expect(fab.state.scanning).toBe(false);
    });

    test("a dialog closed without a code brings the button back", async () => {
        const {fab, scans} = cameraFab({dialog: (props, options) => options.onClose()});
        await fab.onScanClick();
        expect(scans).toEqual([]);
        expect(fab.isVisible).toBe(true);
    });

    test("a refused camera keeps the button hidden until the dialog closes", async () => {
        // The dialog shows the error itself and stays open; it never calls the
        // onError it is given.
        let close = null;
        const {fab, scans} = cameraFab({
            dialog: (props, options) => {
                close = options.onClose;
            },
        });
        const scanning = fab.onScanClick();
        expect(fab.isVisible).toBe(false);
        close();
        await scanning;
        expect(scans).toEqual([]);
        expect(fab.isVisible).toBe(true);
    });

    test("the button hides and ignores taps while the camera is open", async () => {
        let read = null;
        const {fab, scans, dialogs} = cameraFab({
            dialog: (props, options) => {
                read = readsCode("9501101020917").bind(null, props, options);
            },
        });
        const scanning = fab.onScanClick();
        expect(fab.isVisible).toBe(false);
        await fab.onScanClick();
        expect(dialogs.length).toBe(1);
        read();
        await scanning;
        expect(scans.length).toBe(1);
        expect(fab.isVisible).toBe(true);
    });
});
