import {Component, onMounted, onWillStart, onWillUnmount, useState} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

import "@barcode_scanner/js/services/feedback_service.esm";

import {
    barcodeAppWidgets,
    barcodeScreens,
    barcodeStartupTasks,
} from "@barcode_scanner/js/registries.esm";

export class BarcodeScannerApp extends Component {
    setup() {
        this.barcode = useService("barcodeScannerBarcode");
        this.feedback = useState(useService("barcodeScannerFeedback"));
        this.dialog = useService("dialog");
        this.router = useState(useService("barcodeRouter"));
        if (!this.router.currentRoute) {
            this.router.navigate("main");
        }
        onWillStart(() => this.runStartupTasks());
        // Capture scans (incl. Android IME/soft-input PDAs) only while the app
        // is open, so it never steals focus on the rest of the back office.
        onMounted(() => this.barcode.activate());
        onWillUnmount(() => this.barcode.deactivate());
    }

    /**
     * Let the installed feature modules warm up before the first scan. One
     * failing task (a missing record, no access) must not keep the app closed,
     * so each is caught on its own.
     */
    async runStartupTasks() {
        await Promise.all(
            barcodeStartupTasks.getAll().map(async (task) => {
                try {
                    await task(this.env);
                } catch (error) {
                    console.warn("Barcode: a startup task failed", error);
                }
            })
        );
    }

    get currentScreen() {
        const name = this.router.currentRoute?.name;
        return name ? barcodeScreens.get(name, null) : null;
    }

    get currentScreenProps() {
        const entry = this.currentScreen;
        const params = this.router.routeParams || {};
        const navigate = this.router.navigate.bind(this.router);
        const extra = entry && entry.props ? entry.props(params) : {params};
        return {navigate, ...extra};
    }

    get appWidgets() {
        return barcodeAppWidgets.getAll();
    }
}

BarcodeScannerApp.template = "barcode_scanner.App";

registry.category("actions").add("barcode_scanner_app", BarcodeScannerApp);
