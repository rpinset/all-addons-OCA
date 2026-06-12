import {MapRenderer} from "@web_view_leaflet_map/views/leaflet_map/leaflet_map_renderer.esm";
import {patch} from "@web/core/utils/patch";

/* global L */

patch(MapRenderer.prototype, {
    getFields() {
        const fields = super.getFields();
        if (this.resModel === "route.checkpoint") {
            fields.push("sequence");
        }
        return fields;
    },
    prepareMarkerOptions(record) {
        const result = super.prepareMarkerOptions(record);
        if (this.resModel === "route.checkpoint") {
            // Custom marker showing the sequence number
            result.icon = L.divIcon({
                className: "custom-marker",
                html: `<div style="background: #007bff;color:white;border-radius:50%;text-align:center;line-height:28px;font-weight:bold;font-size:14px;">${record.sequence}</div>`,
                iconSize: [28, 28],
                iconAnchor: [14, 14],
            });
        }
        return result;
    },
});
