import {onMounted, onWillUnmount} from "@odoo/owl";
import {useService} from "@web/core/utils/hooks";

export function useBarcode(callback) {
    const barcodeService = useService("barcodeScannerBarcode");

    function normalizeEvent(ev) {
        if (ev?.detail?.barcode) {
            return ev;
        }
        if (ev?.barcode) {
            return {detail: ev};
        }
        return {detail: {barcode: ev}};
    }

    const listener = (ev) => callback(normalizeEvent(ev));

    onMounted(() => {
        barcodeService.bus.addEventListener("barcode_scanned", listener);
    });

    onWillUnmount(() => {
        barcodeService.bus.removeEventListener("barcode_scanned", listener);
    });
}
