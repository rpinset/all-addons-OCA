/**
 * Copyright 2025 Camptocamp SA (http://www.camptocamp.com)
 * @author Simone Orsi <simahawk@gmail.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

import {demotools} from "/shopfloor_mobile_base/static/src/demo/demo.core.esm.js";
import {ScenarioBaseMixin} from "/shopfloor_mobile_base/static/src/scenario/mixins.esm.js";
import {process_registry} from "/shopfloor_mobile_base/static/src/services/process_registry.esm.js";

const DemoComponents = {
    mixins: [ScenarioBaseMixin],
    template: `
        <Screen :screen_info="screen_info">
            <template v-slot:header>
                <state-display-info :info="state.display_info" v-if="state.display_info"/>
            </template>
            <div v-if="state_is('packaging_qty_picker_display')"">
                <separator-title>Only qty to pick</separator-title>
                <v-card
                    v-for="line in packaging_qty_picker_display_get_lines()">
                    <packaging-qty-picker-display
                        :key="make_state_component_key(['qty-picker-widget', line.id])"
                        v-bind="utils.wms.move_line_qty_picker_props(line, {'qtyInit': line.quantity})"
                    />
                </v-card>
                <separator-title>All corresponding packaging</separator-title>
                <v-card
                    v-for="line in packaging_qty_picker_display_get_lines()">
                    <packaging-qty-picker-display
                        :nonZeroOnly="false"
                        :key="make_state_component_key(['qty-picker-widget', line.id])"
                        v-bind="utils.wms.move_line_qty_picker_props(line, {'qtyInit': line.quantity})"
                    />
                </v-card>
            </div>
            <div v-if="state_is('packaging_qty_picker_edit')">
                <separator-title>Edit mode</separator-title>
                <v-card
                    v-for="line in packaging_qty_picker_display_get_lines()">
                    <packaging-qty-picker
                        :key="make_state_component_key(['qty-picker-widget', line.id])"
                        v-bind="utils.wms.move_line_qty_picker_props(line, {'qtyInit': line.quantity})"
                    />
                </v-card>
            </div>
            <div class="button-list button-vertical-list full">
                <v-row align="center" v-if="state_is('packaging_qty_picker_display')">
                    <v-col class="text-center" cols="12">
                        <btn-action @click="state_to('packaging_qty_picker_edit')">Edit mode</btn-action>
                    </v-col>
                </v-row>
                <v-row align="center" v-if="state_is('packaging_qty_picker_edit')">
                    <v-col class="text-center" cols="12">
                        <btn-action @click="state_to('packaging_qty_picker_display')">Display mode</btn-action>
                    </v-col>
                </v-row>
            </div>
        </Screen>
    `,
    data: function () {
        return {
            usage: "demo_components",
            initial_state_key: "packaging_qty_picker_display",
            states: {
                packaging_qty_picker_display: {
                    display_info: {
                        title: "Packaging Qty Picker Display",
                    },
                },
                packaging_qty_picker_edit: {
                    display_info: {
                        title: "Packaging Qty Picker Edit",
                    },
                },
            },
        };
    },
    methods: {
        packaging_qty_picker_display_get_lines: function () {
            const lines = [];
            const product1 = demotools.makeProduct({uom: demotools.uom_unit});
            product1.packaging = [
                demotools.makePackaging({qty: 5, code: "TU", name: "Pack of 5"}),
                demotools.makePackaging({qty: 10, code: "BX", name: "Box of 10"}),
                demotools.makePackaging({qty: 20, code: "BBX", name: "Big Box of 20"}),
            ];
            const line1 = demotools.makeMoveLine({
                // This should be represented as: 1001 units (50 BBX, 1 TU, 1 unit)
                quantity: 1006,
                product: product1,
            });
            lines.push(line1);
            return lines;
        },
    },
};
process_registry.add("demo_components", DemoComponents);

const menuitem_id = demotools.addAppMenu(
    {
        name: "Demo components",
        scenario: "demo_components",
        sequence: 999,
    },
    "demo_cp_1"
);
const CASE = {
    demo_components: {
        next_state: "demo_components",
        data: {
            demo_components: {},
        },
    },
};
demotools.add_case("demo_components", menuitem_id, CASE);

export default DemoComponents;
