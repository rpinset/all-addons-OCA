import {_t} from "@web/core/l10n/translation";
import {barcodeMenuTiles} from "@barcode_scanner/js/registries.esm";

/**
 * Home-screen tile for creating purchase orders. Registers into the scanner
 * core without patching it, like every other feature module.
 */

barcodeMenuTiles.add(
    "purchase",
    {
        label: _t("Purchase Orders"),
        icon: "fa-shopping-cart",
        iconClass: "ilx-icon-purchase",
        action: ({navigate}) => navigate("purchase"),
    },
    {sequence: 50}
);
