import {_t} from "@web/core/l10n/translation";
import {barcodeMenuTiles} from "@barcode_scanner/js/registries.esm";

/**
 * Home-screen tile for inventory adjustments. Registers into the scanner core
 * without patching it, like every other feature module.
 */

barcodeMenuTiles.add(
    "inventory_adjustment",
    {
        label: _t("Inventory Adjustment"),
        icon: "fa-balance-scale",
        iconClass: "ilx-icon-adjustment",
        action: ({navigate}) => navigate("inventory_location"),
    },
    {sequence: 40}
);
