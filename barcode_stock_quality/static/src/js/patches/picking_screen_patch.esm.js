import {PickingScreen} from "@barcode_stock/js/screens/picking_screen.esm";
import {QualityTab} from "@barcode_stock_quality/js/components/quality_tab.esm";
import {patch} from "@web/core/utils/patch";

/**
 * Make the reception's PickingScreen aware of the Quality tab without changing
 * barcode_stock's source: register the tab component so the inherited template
 * can render a "Quality" tab for incoming pickings.
 */
patch(PickingScreen, {
    components: {...PickingScreen.components, QualityTab},
});

patch(PickingScreen.prototype, {
    setup() {
        super.setup(...arguments);
        // The Quality tab's answers not confirmed yet: kept here, where they
        // outlive the tab when the operator switches to another one.
        this.qualityAnswers = {};
    },
});
