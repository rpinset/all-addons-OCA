import {Component, onMounted, onWillStart, useRef} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {loadGoogleMaps} from "../views/google_map/google_maps_loader.esm";
import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
import {useInputField} from "@web/views/fields/input_field_hook";
import {useService} from "@web/core/utils/hooks";

/* global google */

const DEFAULT_FILLFIELDS = {
    street: ["street_number", "route"],
    street2: [
        "administrative_area_level_3",
        "administrative_area_level_4",
        "administrative_area_level_5",
    ],
    city: ["locality", "administrative_area_level_2"],
    zip: "postal_code",
    state_id: "administrative_area_level_1",
    country_id: "country",
};

function getComponentValue(place, type, form = "long_name") {
    const component = (place.address_components || []).find((item) =>
        item.types.includes(type)
    );
    return component ? component[form] : "";
}

export class GplacesAddressFormField extends Component {
    static template = "web_view_google_map.GplacesAddressFormField";
    static props = {
        ...standardFieldProps,
        placeholder: {type: String, optional: true},
        fillfields: {type: Object, optional: true},
        lat: {type: String, optional: true},
        lng: {type: String, optional: true},
    };

    setup() {
        this.orm = useService("orm");
        this.input = useRef("input");
        this.fillfields = {
            ...DEFAULT_FILLFIELDS,
            ...(this.props.fillfields || {}),
        };
        useInputField({
            getValue: () => this.props.record.data[this.props.name] || "",
        });

        onWillStart(async () => {
            await loadGoogleMaps(this.orm);
        });

        onMounted(() => {
            this.initAutocomplete();
        });
    }

    get formattedValue() {
        return this.props.record.data[this.props.name] || "";
    }

    initAutocomplete() {
        if (this.props.readonly || !this.input.el || !window.google?.maps?.places) {
            return;
        }
        this.autocomplete = new google.maps.places.Autocomplete(this.input.el, {
            types: ["address"],
            fields: ["address_components", "geometry", "formatted_address", "name"],
        });
        this.autocomplete.addListener("place_changed", () => this.onPlaceChanged());
    }

    async onPlaceChanged() {
        const place = this.autocomplete.getPlace();
        if (!place) {
            return;
        }
        const values = {};
        for (const [fieldName, source] of Object.entries(this.fillfields)) {
            if (["state_id", "country_id"].includes(fieldName)) {
                continue;
            }
            if (Array.isArray(source)) {
                values[fieldName] = source
                    .map((type) => getComponentValue(place, type))
                    .filter(Boolean)
                    .join(" ");
            } else {
                values[fieldName] = getComponentValue(place, source);
            }
        }
        const location = place.geometry?.location;
        if (this.props.lat && location) {
            values[this.props.lat] = location.lat();
        }
        if (this.props.lng && location) {
            values[this.props.lng] = location.lng();
        }
        values[this.props.name] =
            values.street || place.formatted_address || this.input.el.value;
        await this.props.record.update(values);
    }
}

export const gplacesAddressFormField = {
    component: GplacesAddressFormField,
    displayName: _t("Google Places Address Form"),
    supportedTypes: ["char"],
    extractProps: ({options, placeholder}) => ({
        placeholder,
        fillfields: options.fillfields,
        lat: options.lat,
        lng: options.lng,
    }),
};

registry.category("fields").add("gplaces_address_form", gplacesAddressFormField);
// Legacy widget name used in older docs / views
registry
    .category("fields")
    .add("gplaces_address_autocomplete", gplacesAddressFormField);
