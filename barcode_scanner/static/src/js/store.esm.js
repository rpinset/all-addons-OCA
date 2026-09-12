import {registry} from "@web/core/registry";

export const barcodeStoreService = {
    dependencies: ["barcodeRouter"],
    start(env, {barcodeRouter}) {
        return barcodeRouter;
    },
};

registry.category("services").add("barcodeStore", barcodeStoreService, {
    force: true,
});
