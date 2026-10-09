/**
 * Copyright 2026 Camptocamp SA (http://www.camptocamp.com)
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

import {process_registry} from "/shopfloor_mobile_base/static/src/services/process_registry.esm.js";

const reception_scenario = process_registry.get("reception");
const _get_states = reception_scenario.component.methods._get_states;
// Get the original template of the reception scenario
const template = reception_scenario.component.template;
// Add a button in the `set_packaging_dimension` screen to access the new screen `use_measuring_device`
const button_placeholder = "<!-- measuring-device-placeholder -->";
const new_template_temp = template.replace(
    button_placeholder,
    `
        <v-row>
            <v-col class="text-center" cols="12">
                <btn-action @click="state.on_use_measuring_device">Use Measuring Device</btn-action>
            </v-col>
        </v-row>
    `
);
// Add in template: the new state
const pos_new_state = new_template_temp.indexOf("</Screen>");
const new_template =
    new_template_temp.substring(0, pos_new_state) +
    `
 <div v-if="state_is('use_measuring_device')">


    <v-card color="" class="detail v-card main mt-5 mb-2">
        <v-card-title>Go to the measuring device</v-card-title>
        <v-card-text class="details pt-0">
            <p>The measuring device <b>{{ state.data.measuring_device.name }}</b> has been assigned for measurement of the packaging <b>{{ state.data.packaging.name }}</b>.</p>
            <p>When done, click on OK</p>
        </v-card-text>

    </v-card>
     <div class="button-list button-vertical-list full">
         <v-row align="center">
             <v-col class="text-center" cols="12">
                 <btn-action @click="state.on_confirm_measurement">OK</btn-action>
             </v-col>
         </v-row>
     </div>

 </div>

    ` +
    new_template_temp.substring(pos_new_state);

// // Extend the reception scenario with :
// //   - the new patched template
// //   - the js code for the new state
const ReceptionMeasuringDevice = process_registry.extend("reception", {
    template: new_template,
    "methods._get_states": function () {
        const states = _get_states.bind(this)();
        // Add the handler for the Use Measuring Device button in the `set_packaging_dimension` screen
        states.set_packaging_dimension.on_use_measuring_device = () => {
            const values = {
                picking_id: this.state.data.picking.id,
                selected_line_id: this.state.data.selected_move_line.id,
                packaging_id: this.state.data.packaging.id,
            };
            this.wait_call(
                this.odoo.call(
                    "set_packaging_dimension__measuring_device_assign",
                    values
                )
            );
        };
        // Add the new state `use_measuring_device`
        states.use_measuring_device = {
            display_info: {
                title: "Using measuring device",
            },
            on_confirm_measurement: () => {
                this.wait_call(
                    this.odoo.call(
                        "set_packaging_dimension__measuring_device_release",
                        {
                            picking_id: this.state.data.picking.id,
                            selected_line_id: this.state.data.selected_move_line.id,
                            packaging_id: this.state.data.packaging.id,
                        }
                    )
                );
            },
        };
        return states;
    },
});

process_registry.replace("reception", ReceptionMeasuringDevice);
