import {GoogleMapController} from "./google_map_controller.esm";
import {GoogleMapRenderer} from "./google_map_renderer.esm";
import {registry} from "@web/core/registry";

function normalizeArch(arch) {
    if (arch && typeof arch !== "string") {
        return arch;
    }
    const xml = String(arch || "");
    const doc = new DOMParser().parseFromString(xml, "text/xml");
    return doc.documentElement;
}

export const googleMapView = {
    type: "google_map",
    display_name: "Google Map",
    icon: "fa fa-map-o",
    multiRecord: true,
    Controller: GoogleMapController,
    Renderer: GoogleMapRenderer,
    searchMenuTypes: ["filter", "favorite"],

    props: (genericProps) => {
        const archEl = normalizeArch(genericProps.arch);
        return {
            ...genericProps,
            Renderer: GoogleMapRenderer,
            archInfo: {
                arch: archEl,
            },
        };
    },
};

registry.category("views").add("google_map", googleMapView);
