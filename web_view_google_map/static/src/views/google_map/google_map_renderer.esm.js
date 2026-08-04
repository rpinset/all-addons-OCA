import {Component, onMounted, onPatched, onWillStart, useRef} from "@odoo/owl";
import {MAP_THEMES} from "./map_themes.esm";
import {evaluateBooleanExpr} from "@web/core/py_js/py";
import {loadGoogleMaps} from "./google_maps_loader.esm";
import {rpc} from "@web/core/network/rpc";
import {useService} from "@web/core/utils/hooks";

/* global google, MarkerClusterer */

const MARKER_COLORS = [
    "black",
    "blue",
    "brown",
    "cyan",
    "green",
    "grey",
    "orange",
    "pink",
    "purple",
    "red",
    "white",
    "yellow",
];

function normalizeArch(arch) {
    if (arch && typeof arch !== "string") {
        return arch;
    }
    const xml = String(arch || "");
    const doc = new DOMParser().parseFromString(xml, "text/xml");
    return doc.documentElement;
}

function parseMarkerColors(colorsAttr) {
    if (!colorsAttr) {
        return [];
    }
    return colorsAttr
        .split(";")
        .map((pair) => pair.trim())
        .filter(Boolean)
        .map((pair) => {
            const idx = pair.indexOf(":");
            if (idx === -1) {
                return null;
            }
            return [pair.slice(0, idx).trim(), pair.slice(idx + 1).trim()];
        })
        .filter(Boolean);
}

export class GoogleMapRenderer extends Component {
    static template = "web_view_google_map.GoogleMapRenderer";
    static props = {
        "*": true,
    };

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.mapRef = useRef("mapContainer");
        this.gmap = null;
        this.markerCluster = null;
        this.markers = [];
        this.infoWindow = null;
        this.records = [];
        this.theme = "default";
        this.missingApiKey = false;

        const archEl = normalizeArch(this.props.archInfo?.arch || this.props.arch);
        const attrs = archEl.attributes || {};
        this.fieldLat = attrs.getNamedItem("lat")?.value || "partner_latitude";
        this.fieldLng = attrs.getNamedItem("lng")?.value || "partner_longitude";
        this.markerColor = attrs.getNamedItem("color")?.value || null;
        this.markerColors = parseMarkerColors(attrs.getNamedItem("colors")?.value);
        this.defaultMarkerColor = "red";
        this.iconUrl = "/web_view_google_map/static/src/img/markers/";
        this.resModel = this.props.resModel;
        this.archFields = [...archEl.querySelectorAll(":scope > field")].map((node) =>
            node.getAttribute("name")
        );

        onWillStart(async () => {
            const maps = await loadGoogleMaps(this.orm);
            if (!maps) {
                this.missingApiKey = true;
                return;
            }
            await this.loadTheme();
            await this.loadRecords();
        });

        onMounted(() => {
            if (this.missingApiKey) {
                return;
            }
            this.initMap();
            this.renderMarkers();
        });

        onPatched(() => {
            if (this.gmap) {
                this.renderMarkers();
            }
        });
    }

    openGoogleMapsSettings() {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: "res.config.settings",
            views: [[false, "form"]],
            target: "current",
            context: {module: "base_google_map"},
        });
    }

    async loadTheme() {
        try {
            const data = await rpc("/web/map_theme");
            if (
                data?.theme &&
                Object.prototype.hasOwnProperty.call(MAP_THEMES, data.theme)
            ) {
                this.theme = data.theme;
            }
        } catch {
            this.theme = "default";
        }
    }

    async loadRecords() {
        const fields = new Set(["id", "display_name", this.fieldLat, this.fieldLng]);
        for (const name of this.archFields) {
            if (name) {
                fields.add(name);
            }
        }
        try {
            this.records = await this.orm.searchRead(
                this.resModel,
                this.props.domain || [],
                [...fields],
                {
                    limit: this.props.limit || 80,
                    context: this.props.context || {},
                }
            );
        } catch {
            this.records = [];
        }
    }

    initMap() {
        const mapDiv = this.mapRef.el;
        if (!mapDiv || !window.google?.maps) {
            return;
        }
        this.infoWindow = new google.maps.InfoWindow();
        this.gmap = new google.maps.Map(mapDiv, {
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            minZoom: 3,
            maxZoom: 20,
            fullscreenControl: true,
            mapTypeControl: true,
            center: {lat: 0, lng: 0},
            zoom: 2,
        });
        this.applyTheme();
        this.initMarkerCluster();
    }

    applyTheme() {
        if (!this.gmap || this.theme === "default" || !MAP_THEMES[this.theme]) {
            return;
        }
        const styledMapType = new google.maps.StyledMapType(MAP_THEMES[this.theme], {
            name: "Styled Map",
        });
        this.gmap.mapTypes.set("styled_map", styledMapType);
        this.gmap.setMapTypeId("styled_map");
    }

    initMarkerCluster() {
        if (typeof MarkerClusterer === "undefined") {
            return;
        }
        this.markerCluster = new MarkerClusterer(this.gmap, [], {
            gridSize: 40,
            maxZoom: 7,
            zoomOnClick: true,
            imagePath: "/web_view_google_map/static/lib/markerclusterer/img/m",
        });
    }

    clearMarkers() {
        for (const marker of this.markers) {
            marker.setMap(null);
        }
        this.markers = [];
        if (this.markerCluster) {
            this.markerCluster.clearMarkers();
        }
    }

    renderMarkers() {
        if (!this.gmap) {
            return;
        }
        this.clearMarkers();
        const bounds = new google.maps.LatLngBounds();
        let hasPoint = false;

        for (const record of this.records) {
            const lat = Number(record[this.fieldLat]);
            const lng = Number(record[this.fieldLng]);
            if (!lat || !lng) {
                continue;
            }
            const latLng = new google.maps.LatLng(lat, lng);
            const color = this.getIconColor(record);
            const marker = new google.maps.Marker({
                position: latLng,
                map: this.markerCluster ? null : this.gmap,
                animation: google.maps.Animation.DROP,
                icon: this.getIconColorPath(color),
                title: record.display_name || "",
            });
            marker.addListener("click", () => this.onMarkerClick(marker, record));
            this.markers.push(marker);
            if (this.markerCluster) {
                this.markerCluster.addMarker(marker);
            }
            bounds.extend(latLng);
            hasPoint = true;
        }

        if (hasPoint) {
            this.gmap.fitBounds(bounds);
        }
    }

    getIconColor(record) {
        if (this.markerColor) {
            return this.markerColor;
        }
        for (const [color, expression] of this.markerColors) {
            try {
                if (evaluateBooleanExpr(expression, record)) {
                    return color;
                }
            } catch {
                // Ignore invalid color expressions from the arch
            }
        }
        return this.defaultMarkerColor;
    }

    getIconColorPath(color) {
        const name = MARKER_COLORS.includes(color) ? color : this.defaultMarkerColor;
        return `${this.iconUrl}${name}.png`;
    }

    onMarkerClick(marker, record) {
        const email = record.email ? `<div>${record.email}</div>` : "";
        const city = record.city ? `<div>${record.city}</div>` : "";
        this.infoWindow.setContent(`
            <div class="o_google_map_info" data-res-id="${record.id}">
                <strong>${record.display_name || ""}</strong>
                ${email}${city}
                <a href="#" class="o_google_map_open_record">Open</a>
            </div>
        `);
        this.infoWindow.open(this.gmap, marker);
        google.maps.event.addListenerOnce(this.infoWindow, "domready", () => {
            const link = document.querySelector(".o_google_map_open_record");
            if (link) {
                link.addEventListener("click", (ev) => {
                    ev.preventDefault();
                    this.openRecord(record);
                });
            }
        });
    }

    openRecord(record) {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: this.resModel,
            res_id: record.id,
            views: [[false, "form"]],
            target: "current",
        });
    }
}
