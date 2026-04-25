/**
 * Copyright 2025 Camptocamp SA
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
 */

import {process_registry} from "/shopfloor_mobile_base/static/src/services/process_registry.esm.js";

const reception_scenario = process_registry.get("reception");
const _get_states = reception_scenario.component.methods._get_states;
// Get the original template of the reception scenario
const template = reception_scenario.component.template;
const pos = template.indexOf("<!-- Package Detail Slot -->");
const new_template =
    template.substring(0, pos) +
    `
    <div class="v-card__text details">
    <v-form ref="form_dimension">
        <v-container style="padding-top: 0; padding-bottom: 0">
            <v-row v-if="state.is_height_required()">
                <v-text-field
                    label="Package Height"
                    type="number"
                    :suffix="state.data.selected_move_line[0].package_dest.height_uom"
                    placeholder="Package Height"
                    v-model="state.data.selected_move_line[0].package_dest.height"
                ></v-text-field>
            </v-row>
        </v-container>
    </v-form>
    </div>

    ` +
    template.substring(pos);

const ReceptionPackageDimension = process_registry.extend("reception", {
    template: new_template,
    "methods._get_states": function () {
        const states = _get_states.bind(this)();
        const _get_set_destination_data =
            states.set_destination._get_set_destination_data;
        const overriden = function (location) {
            const data = _get_set_destination_data(location);
            const height = this.line_being_handled.package_dest.height;
            data.height = Number(height);
            return data;
        };
        states.set_destination._get_set_destination_data = overriden.bind(this);
        const is_height_required = function () {
            const pack = this.state.data.selected_move_line[0].package_dest;
            if (pack.package_type && pack.package_type.height_required) {
                return true;
            }
            return false;
        };
        states.set_destination.is_height_required = is_height_required.bind(this);
        return states;
    },
});

process_registry.replace("reception", ReceptionPackageDimension);
