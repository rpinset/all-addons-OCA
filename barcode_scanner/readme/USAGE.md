``barcode_scanner`` is a framework and is not useful on its own: install a
feature module such as ``barcode_stock`` to get actual operations.

To build your own feature module, register your pieces into the framework
registries — no change to the base module is required.

Register a screen:

```js
import {barcodeScreens} from "@barcode_scanner/js/registries";

barcodeScreens.add("my_screen", {component: MyScreen});
```

Register a scan handler (tried in ``sequence`` order; the first that returns a
truthy value consumes the scan):

```js
import {barcodeScanHandlers} from "@barcode_scanner/js/registries";

barcodeScanHandlers.add("my_handler", {
    async handle(barcode, parsed, {api, navigate, notify}) {
        // return true when handled
    },
}, {sequence: 50});
```

Register a home-screen tile:

```js
import {barcodeMenuTiles} from "@barcode_scanner/js/registries";

barcodeMenuTiles.add("my_tile", {
    label: "My Screen",
    icon: "fa-cube",
    action: ({navigate}) => navigate("my_screen"),
}, {sequence: 50});
```

Register a barcode parser (tried in ``sequence`` order before the built-in
EAN13 one; return ``null`` to let the next parser try):

```js
import {barcodeParsers} from "@barcode_scanner/js/registries";

barcodeParsers.add("my_symbology", (barcode) => {
    // return {type: "...", value: "<product code>", ...} or null
}, {sequence: 20});
```

Register a startup task, for data your module needs before the first scan
(``barcode_gs1`` reads its nomenclature this way). Tasks are awaited when the
app opens; one that fails is logged and skipped:

```js
import {barcodeStartupTasks} from "@barcode_scanner/js/registries";

barcodeStartupTasks.add("my_config", (env) => loadMyConfig(env.services.orm));
```
