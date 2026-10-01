import {barcodeMatchDomain} from "@barcode_scanner/js/utils/scan_match.esm";
import {barcodeScanHandlers} from "@barcode_scanner/js/registries.esm";

/**
 * Home-screen scan recognition for stock. Isolated in its own file so it can be
 * moved to `barcode_stock` untouched in phase 2.
 */

barcodeScanHandlers.add(
    "stock_picking",
    {
        async handle(barcode, parsed, {api, navigate}) {
            // A picking reference is client-configurable: its name comes from the
            // operation type's sequence, whose prefix is the warehouse's own code
            // (AC-HAU, DI-LIC, JOBS...), not necessarily WH or INT. Never gate the
            // lookup on a hard-coded prefix — search by name and fall through when
            // nothing matches, exactly like the product and location handlers.
            const pickings = await api.searchRead(
                "stock.picking",
                [["name", "=", barcode]],
                ["id"]
            );
            if (!pickings.length) {
                return false;
            }
            navigate("picking", {pickingId: pickings[0].id});
            return true;
        },
    },
    {sequence: 10}
);

barcodeScanHandlers.add(
    "product",
    {
        async handle(barcode, parsed, {api, navigate}) {
            const productCode = parsed?.value || barcode;
            const productDomain = barcodeMatchDomain(productCode);
            const products = productDomain
                ? await api.searchRead("product.product", productDomain, [
                      "id",
                      "display_name",
                  ])
                : [];
            if (!products.length) {
                return false;
            }
            navigate("quick_info", {result: products[0], result_type: "product"});
            return true;
        },
    },
    {sequence: 20}
);

barcodeScanHandlers.add(
    "location",
    {
        async handle(barcode, parsed, {api, navigate}) {
            const locationDomain = barcodeMatchDomain(barcode);
            const locations = locationDomain
                ? await api.searchRead("stock.location", locationDomain, [
                      "id",
                      "display_name",
                  ])
                : [];
            if (!locations.length) {
                return false;
            }
            navigate("quick_info", {result: locations[0], result_type: "location"});
            return true;
        },
    },
    {sequence: 30}
);
