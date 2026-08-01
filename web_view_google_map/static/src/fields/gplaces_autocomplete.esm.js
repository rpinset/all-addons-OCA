import {Component, onMounted, onWillStart, useRef} from "@odoo/owl";
import {_t} from "@web/core/l10n/translation";
import {loadGoogleMaps} from "../views/google_map/google_maps_loader.esm";
import {registry} from "@web/core/registry";
import {standardFieldProps} from "@web/views/fields/standard_field_props";
import {useInputField} from "@web/views/fields/input_field_hook";
import {useService} from "@web/core/utils/hooks";

/* global google */

const DEFAULT_FILLFIELDS = {
    general: {
        name: "name",
        website: "website",
        phone: ["international_phone_number", "formatted_phone_number"],
    },
    geolocation: {
        partner_latitude: "latitude",
        partner_longitude: "longitude",
    },
    address: {
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
    },
};

function getComponentValue(place, type, form = "long_name") {
    const component = (place.address_components || []).find((item) =>
        item.types.includes(type)
    );
    return component ? component[form] : "";
}

function resolveSource(place, source) {
    if (Array.isArray(source)) {
        return source.map((key) => place[key]).find(Boolean) || "";
    }
    return place[source] || "";
}

function resolveAddressSource(place, source) {
    if (Array.isArray(source)) {
        return source
            .map((type) => getComponentValue(place, type))
            .filter(Boolean)
            .join(" ");
    }
    return getComponentValue(place, source);
}

export class GplacesAutocompleteField extends Component {
    static template = "web_view_google_map.GplacesAutocompleteField";
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
            types: ["establishment"],
            fields: [
                "address_components",
                "geometry",
                "name",
                "website",
                "formatted_phone_number",
                "international_phone_number",
            ],
        });
        this.autocomplete.addListener("place_changed", () => this.onPlaceChanged());
    }

    _fillGeneral(place, values) {
        for (const [fieldName, source] of Object.entries(
            this.fillfields.general || {}
        )) {
            values[fieldName] = resolveSource(place, source);
        }
    }

    _fillGeolocation(place, values) {
        const location = place.geometry?.location;
        if (!location) {
            return;
        }
        for (const [fieldName, key] of Object.entries(
            this.fillfields.geolocation || {}
        )) {
            values[fieldName] = key === "latitude" ? location.lat() : location.lng();
        }
        if (this.props.lat) {
            values[this.props.lat] = location.lat();
        }
        if (this.props.lng) {
            values[this.props.lng] = location.lng();
        }
    }

    _fillAddress(place, values) {
        for (const [fieldName, source] of Object.entries(
            this.fillfields.address || {}
        )) {
            if (["state_id", "country_id"].includes(fieldName)) {
                continue;
            }
            values[fieldName] = resolveAddressSource(place, source);
        }
    }

    async onPlaceChanged() {
        const place = this.autocomplete.getPlace();
        if (!place) {
            return;
        }
        const values = {};
        this._fillGeneral(place, values);
        this._fillGeolocation(place, values);
        this._fillAddress(place, values);
        values[this.props.name] =
            place.name || place.formatted_address || this.input.el.value;
        await this.props.record.update(values);
    }
}

export const gplacesAutocompleteField = {
    component: GplacesAutocompleteField,
    displayName: _t("Google Places Autocomplete"),
    supportedTypes: ["char"],
    extractProps: ({options, placeholder}) => ({
        placeholder,
        fillfields: options.fillfields,
        lat: options.lat,
        lng: options.lng,
    }),
};

registry.category("fields").add("gplaces_autocomplete", gplacesAutocompleteField);
