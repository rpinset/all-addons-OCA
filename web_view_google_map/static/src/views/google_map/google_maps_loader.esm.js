import {loadJS} from "@web/core/assets";

let googleMapsPromise = null;

/** Demo / unset values that must not be sent to Google. */
const UNUSABLE_API_KEYS = new Set(["", "YOUR_GOOGLE_MAPS_API_KEY"]);

/**
 * @param {String|false|null|undefined} apiKey
 * @returns {Boolean}
 */
export function isUsableGoogleMapsApiKey(apiKey) {
    return !UNUSABLE_API_KEYS.has(String(apiKey || "").trim());
}

/**
 * Load the Google Maps JS API using keys/libraries from ir.config_parameter.
 * Parameters are managed by base_google_map.
 * @param {Object} orm - ORM service (`useService("orm")`)
 * @returns {Promise<typeof google.maps|null>} maps API, or null if no usable key
 */
export async function loadGoogleMaps(orm) {
    if (window.google?.maps) {
        return window.google.maps;
    }
    if (googleMapsPromise) {
        return googleMapsPromise;
    }
    googleMapsPromise = (async () => {
        const [apiKey, libraries, lang, region] = await Promise.all([
            orm.call("ir.config_parameter", "get_param", [
                "google.api_key_geocode",
                "",
            ]),
            orm.call("ir.config_parameter", "get_param", [
                "google.maps_libraries",
                "geometry,places",
            ]),
            orm.call("ir.config_parameter", "get_param", [
                "google.lang_localization",
                "",
            ]),
            orm.call("ir.config_parameter", "get_param", [
                "google.region_localization",
                "",
            ]),
        ]);

        if (!isUsableGoogleMapsApiKey(apiKey)) {
            return null;
        }

        const url = new URL("https://maps.googleapis.com/maps/api/js");
        url.searchParams.set("v", "quarterly");
        url.searchParams.set(
            "libraries",
            String(libraries || "geometry,places").replace(/^,+|,+$/g, "")
        );
        url.searchParams.set("key", String(apiKey).trim());
        // Lang/region may already include "&language=xx" from base_google_map
        const langCode = String(lang || "").includes("=")
            ? String(lang).split("=").pop()
            : lang;
        const regionCode = String(region || "").includes("=")
            ? String(region).split("=").pop()
            : region;
        if (langCode) {
            url.searchParams.set("language", langCode);
        }
        if (regionCode) {
            url.searchParams.set("region", regionCode);
        }

        await loadJS(url.toString());
        return window.google.maps;
    })();

    try {
        return await googleMapsPromise;
    } catch (error) {
        googleMapsPromise = null;
        throw error;
    }
}
