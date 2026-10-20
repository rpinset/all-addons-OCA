import {Component, useState} from "@odoo/owl";
import {BarcodeDialog} from "@web/core/barcode/barcode_dialog";
import {barcodeAppWidgets} from "@barcode_scanner/js/registries.esm";
import {isBarcodeScannerSupported} from "@web/core/barcode/barcode_video_scanner";
import {useService} from "@web/core/utils/hooks";

const SCAN_EVENT = "barcode_scanned";

/**
 * Open Odoo's scanner dialog on the back camera. Settles with the code read, or
 * with null once the dialog closes without one: closed by hand, or after it
 * showed that the camera was refused. (`scanBarcode` from `@web` stays pending
 * then, which would keep the button hidden for good.)
 */
function readWithCamera(env) {
    return new Promise((resolve) => {
        env.services.dialog.add(
            BarcodeDialog,
            {
                facingMode: "environment",
                onResult: resolve,
                // Required by the dialog, which shows a camera error itself and
                // stays open: the read settles when it is closed (onClose).
                onError: () => undefined,
            },
            {
                // The dialog closes itself before it hands over what it read:
                // let that result, which follows the close, win.
                onClose: () => Promise.resolve().then(() => resolve(null)),
            }
        );
    });
}

/**
 * A floating action button that opens the device camera to scan a barcode and
 * feeds it into the same event bus the hardware scanner uses, so the active
 * screen handles it identically.
 *
 * It plugs into the base app through the `barcode_app_widgets` registry — no
 * patching of BarcodeScannerApp.
 */
export class CameraFab extends Component {
    static template = "barcode_camera.CameraFab";
    static props = {};

    setup() {
        this.barcode = useService("barcodeScannerBarcode");
        // The screens reading scans right now, whichever module they come from.
        this.readers = useState(this.barcode.readers);
        this.state = useState({scanning: false});
    }

    get isVisible() {
        // Offered while the screen on display reads scans and, like Odoo's own
        // camera buttons, only when the browser can open the camera (HTTPS or
        // localhost, with getUserMedia).
        return (
            this.readers.count > 0 &&
            !this.state.scanning &&
            isBarcodeScannerSupported()
        );
    }

    async onScanClick() {
        if (this.state.scanning) {
            return;
        }
        this.state.scanning = true;
        try {
            const barcode = await readWithCamera(this.env);
            if (barcode) {
                this.barcode.bus.trigger(SCAN_EVENT, {
                    barcode,
                    parsed: this.barcode.parseBarcode(barcode),
                    source: "camera",
                });
            }
        } finally {
            this.state.scanning = false;
        }
    }
}

barcodeAppWidgets.add("camera_fab", {component: CameraFab});
