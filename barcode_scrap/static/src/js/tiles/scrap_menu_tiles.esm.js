import {_t} from "@web/core/l10n/translation";
import {barcodeMenuTiles} from "@barcode_scanner/js/registries.esm";

/**
 * Home-screen tile for scrapping goods. Registers into the scanner core without
 * patching it, like every other feature module.
 */

barcodeMenuTiles.add(
    "scrap",
    {
        label: _t("Scrap Products"),
        icon: "fa-trash-o",
        iconClass: "ilx-icon-scrap",
        action: ({navigate}) => navigate("scrap_location"),
    },
    {sequence: 60}
);
