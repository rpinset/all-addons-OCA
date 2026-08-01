// Extracted from legacy web_view_google_map Utils
export const MAP_THEMES = {
    default: [],
    aubergine: [
        {
            elementType: "geometry",
            stylers: [
                {
                    color: "#1d2c4d",
                },
            ],
        },
        {
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#8ec3b9",
                },
            ],
        },
        {
            elementType: "labels.text.stroke",
            stylers: [
                {
                    color: "#1a3646",
                },
            ],
        },
        {
            featureType: "administrative.country",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#4b6878",
                },
            ],
        },
        {
            featureType: "administrative.land_parcel",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#64779e",
                },
            ],
        },
        {
            featureType: "administrative.province",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#4b6878",
                },
            ],
        },
        {
            featureType: "landscape.man_made",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#334e87",
                },
            ],
        },
        {
            featureType: "landscape.natural",
            elementType: "geometry",
            stylers: [
                {
                    color: "#023e58",
                },
            ],
        },
        {
            featureType: "poi",
            elementType: "geometry",
            stylers: [
                {
                    color: "#283d6a",
                },
            ],
        },
        {
            featureType: "poi",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#6f9ba5",
                },
            ],
        },
        {
            featureType: "poi",
            elementType: "labels.text.stroke",
            stylers: [
                {
                    color: "#1d2c4d",
                },
            ],
        },
        {
            featureType: "poi.business",
            stylers: [
                {
                    visibility: "off",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "geometry.fill",
            stylers: [
                {
                    color: "#023e58",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "labels.text",
            stylers: [
                {
                    visibility: "off",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#3C7680",
                },
            ],
        },
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [
                {
                    color: "#304a7d",
                },
            ],
        },
        {
            featureType: "road",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#98a5be",
                },
            ],
        },
        {
            featureType: "road",
            elementType: "labels.text.stroke",
            stylers: [
                {
                    color: "#1d2c4d",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [
                {
                    color: "#2c6675",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#255763",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#b0d5ce",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "labels.text.stroke",
            stylers: [
                {
                    color: "#023e58",
                },
            ],
        },
        {
            featureType: "transit",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#98a5be",
                },
            ],
        },
        {
            featureType: "transit",
            elementType: "labels.text.stroke",
            stylers: [
                {
                    color: "#1d2c4d",
                },
            ],
        },
        {
            featureType: "transit.line",
            elementType: "geometry.fill",
            stylers: [
                {
                    color: "#283d6a",
                },
            ],
        },
        {
            featureType: "transit.station",
            elementType: "geometry",
            stylers: [
                {
                    color: "#3a4762",
                },
            ],
        },
        {
            featureType: "water",
            elementType: "geometry",
            stylers: [
                {
                    color: "#0e1626",
                },
            ],
        },
        {
            featureType: "water",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#4e6d70",
                },
            ],
        },
    ],
    night: [
        {
            elementType: "geometry",
            stylers: [
                {
                    color: "#242f3e",
                },
            ],
        },
        {
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#746855",
                },
            ],
        },
        {
            elementType: "labels.text.stroke",
            stylers: [
                {
                    color: "#242f3e",
                },
            ],
        },
        {
            featureType: "administrative.locality",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#d59563",
                },
            ],
        },
        {
            featureType: "poi",
            elementType: "labels.text",
            stylers: [
                {
                    visibility: "off",
                },
            ],
        },
        {
            featureType: "poi",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#d59563",
                },
            ],
        },
        {
            featureType: "poi.business",
            stylers: [
                {
                    visibility: "off",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "geometry",
            stylers: [
                {
                    color: "#263c3f",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#6b9a76",
                },
            ],
        },
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [
                {
                    color: "#38414e",
                },
            ],
        },
        {
            featureType: "road",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#212a37",
                },
            ],
        },
        {
            featureType: "road",
            elementType: "labels.icon",
            stylers: [
                {
                    visibility: "off",
                },
            ],
        },
        {
            featureType: "road",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#9ca5b3",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [
                {
                    color: "#746855",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#1f2835",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#f3d19c",
                },
            ],
        },
        {
            featureType: "transit",
            stylers: [
                {
                    visibility: "off",
                },
            ],
        },
        {
            featureType: "transit",
            elementType: "geometry",
            stylers: [
                {
                    color: "#2f3948",
                },
            ],
        },
        {
            featureType: "transit.station",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#d59563",
                },
            ],
        },
        {
            featureType: "water",
            elementType: "geometry",
            stylers: [
                {
                    color: "#17263c",
                },
            ],
        },
        {
            featureType: "water",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#515c6d",
                },
            ],
        },
        {
            featureType: "water",
            elementType: "labels.text.stroke",
            stylers: [
                {
                    color: "#17263c",
                },
            ],
        },
    ],
    dark: [
        {
            elementType: "geometry",
            stylers: [
                {
                    color: "#212121",
                },
            ],
        },
        {
            elementType: "labels.icon",
            stylers: [
                {
                    visibility: "off",
                },
            ],
        },
        {
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#757575",
                },
            ],
        },
        {
            elementType: "labels.text.stroke",
            stylers: [
                {
                    color: "#212121",
                },
            ],
        },
        {
            featureType: "administrative",
            elementType: "geometry",
            stylers: [
                {
                    color: "#757575",
                },
            ],
        },
        {
            featureType: "administrative.country",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#9e9e9e",
                },
            ],
        },
        {
            featureType: "administrative.land_parcel",
            stylers: [
                {
                    visibility: "off",
                },
            ],
        },
        {
            featureType: "administrative.locality",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#bdbdbd",
                },
            ],
        },
        {
            featureType: "poi",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#757575",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "geometry",
            stylers: [
                {
                    color: "#181818",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#616161",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "labels.text.stroke",
            stylers: [
                {
                    color: "#1b1b1b",
                },
            ],
        },
        {
            featureType: "road",
            elementType: "geometry.fill",
            stylers: [
                {
                    color: "#2c2c2c",
                },
            ],
        },
        {
            featureType: "road",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#8a8a8a",
                },
            ],
        },
        {
            featureType: "road.arterial",
            elementType: "geometry",
            stylers: [
                {
                    color: "#373737",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [
                {
                    color: "#3c3c3c",
                },
            ],
        },
        {
            featureType: "road.highway.controlled_access",
            elementType: "geometry",
            stylers: [
                {
                    color: "#4e4e4e",
                },
            ],
        },
        {
            featureType: "road.local",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#616161",
                },
            ],
        },
        {
            featureType: "transit",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#757575",
                },
            ],
        },
        {
            featureType: "water",
            elementType: "geometry",
            stylers: [
                {
                    color: "#000000",
                },
            ],
        },
        {
            featureType: "water",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#3d3d3d",
                },
            ],
        },
    ],
    retro: [
        {
            elementType: "geometry",
            stylers: [
                {
                    color: "#ebe3cd",
                },
            ],
        },
        {
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#523735",
                },
            ],
        },
        {
            elementType: "labels.text.stroke",
            stylers: [
                {
                    color: "#f5f1e6",
                },
            ],
        },
        {
            featureType: "administrative",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#c9b2a6",
                },
            ],
        },
        {
            featureType: "administrative.land_parcel",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#dcd2be",
                },
            ],
        },
        {
            featureType: "administrative.land_parcel",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#ae9e90",
                },
            ],
        },
        {
            featureType: "landscape.natural",
            elementType: "geometry",
            stylers: [
                {
                    color: "#dfd2ae",
                },
            ],
        },
        {
            featureType: "poi",
            elementType: "geometry",
            stylers: [
                {
                    color: "#dfd2ae",
                },
            ],
        },
        {
            featureType: "poi",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#93817c",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "geometry.fill",
            stylers: [
                {
                    color: "#a5b076",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#447530",
                },
            ],
        },
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [
                {
                    color: "#f5f1e6",
                },
            ],
        },
        {
            featureType: "road.arterial",
            elementType: "geometry",
            stylers: [
                {
                    color: "#fdfcf8",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [
                {
                    color: "#f8c967",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#e9bc62",
                },
            ],
        },
        {
            featureType: "road.highway.controlled_access",
            elementType: "geometry",
            stylers: [
                {
                    color: "#e98d58",
                },
            ],
        },
        {
            featureType: "road.highway.controlled_access",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#db8555",
                },
            ],
        },
        {
            featureType: "road.local",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#806b63",
                },
            ],
        },
        {
            featureType: "transit.line",
            elementType: "geometry",
            stylers: [
                {
                    color: "#dfd2ae",
                },
            ],
        },
        {
            featureType: "transit.line",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#8f7d77",
                },
            ],
        },
        {
            featureType: "transit.line",
            elementType: "labels.text.stroke",
            stylers: [
                {
                    color: "#ebe3cd",
                },
            ],
        },
        {
            featureType: "transit.station",
            elementType: "geometry",
            stylers: [
                {
                    color: "#dfd2ae",
                },
            ],
        },
        {
            featureType: "water",
            elementType: "geometry.fill",
            stylers: [
                {
                    color: "#b9d3c2",
                },
            ],
        },
        {
            featureType: "water",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#92998d",
                },
            ],
        },
    ],
    silver: [
        {
            elementType: "geometry",
            stylers: [
                {
                    color: "#f5f5f5",
                },
            ],
        },
        {
            elementType: "labels.icon",
            stylers: [
                {
                    visibility: "off",
                },
            ],
        },
        {
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#616161",
                },
            ],
        },
        {
            elementType: "labels.text.stroke",
            stylers: [
                {
                    color: "#f5f5f5",
                },
            ],
        },
        {
            featureType: "administrative.land_parcel",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#bdbdbd",
                },
            ],
        },
        {
            featureType: "poi",
            elementType: "geometry",
            stylers: [
                {
                    color: "#eeeeee",
                },
            ],
        },
        {
            featureType: "poi",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#757575",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "geometry",
            stylers: [
                {
                    color: "#e5e5e5",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#9e9e9e",
                },
            ],
        },
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [
                {
                    color: "#ffffff",
                },
            ],
        },
        {
            featureType: "road.arterial",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#757575",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [
                {
                    color: "#dadada",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#616161",
                },
            ],
        },
        {
            featureType: "road.local",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#9e9e9e",
                },
            ],
        },
        {
            featureType: "transit.line",
            elementType: "geometry",
            stylers: [
                {
                    color: "#e5e5e5",
                },
            ],
        },
        {
            featureType: "transit.station",
            elementType: "geometry",
            stylers: [
                {
                    color: "#eeeeee",
                },
            ],
        },
        {
            featureType: "water",
            elementType: "geometry",
            stylers: [
                {
                    color: "#c9c9c9",
                },
            ],
        },
        {
            featureType: "water",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#9e9e9e",
                },
            ],
        },
    ],
    atlas: [
        {
            stylers: [
                {
                    visibility: "on",
                },
            ],
        },
        {
            featureType: "administrative",
            elementType: "geometry.fill",
            stylers: [
                {
                    color: "#f5f5f5",
                },
            ],
        },
        {
            featureType: "administrative",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#003975",
                },
            ],
        },
        {
            featureType: "administrative.locality",
            elementType: "labels.text.fill",
            stylers: [
                {
                    weight: 1,
                },
            ],
        },
        {
            featureType: "administrative.neighborhood",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#90b1d5",
                },
            ],
        },
        {
            featureType: "landscape.man_made",
            elementType: "geometry",
            stylers: [
                {
                    color: "#fcfcfc",
                },
                {
                    visibility: "on",
                },
            ],
        },
        {
            featureType: "landscape.natural",
            elementType: "geometry",
            stylers: [
                {
                    color: "#fcfcfc",
                },
            ],
        },
        {
            featureType: "landscape.natural.landcover",
            elementType: "geometry",
            stylers: [
                {
                    color: "#f2f2f2",
                },
            ],
        },
        {
            featureType: "landscape.natural.terrain",
            elementType: "geometry",
            stylers: [
                {
                    color: "#bfeecd",
                },
            ],
        },
        {
            featureType: "poi.attraction",
            elementType: "labels.icon",
            stylers: [
                {
                    color: "#32b2c3",
                },
            ],
        },
        {
            featureType: "poi.attraction",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#32b2c3",
                },
            ],
        },
        {
            featureType: "poi.business",
            elementType: "labels.icon",
            stylers: [
                {
                    color: "#6c87ea",
                },
            ],
        },
        {
            featureType: "poi.business",
            elementType: "labels.text.fill",
            stylers: [
                {
                    weight: 2,
                },
            ],
        },
        {
            featureType: "poi.government",
            elementType: "geometry",
            stylers: [
                {
                    color: "#ebf7ff",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "geometry",
            stylers: [
                {
                    color: "#dafbe2",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "labels.icon",
            stylers: [
                {
                    color: "#44ca66",
                },
            ],
        },
        {
            featureType: "poi.park",
            elementType: "labels.text.fill",
            stylers: [
                {
                    color: "#33a34f",
                },
            ],
        },
        {
            featureType: "poi.school",
            elementType: "geometry",
            stylers: [
                {
                    color: "#f5e0f3",
                },
            ],
        },
        {
            featureType: "road.arterial",
            elementType: "geometry.fill",
            stylers: [
                {
                    color: "#ededed",
                },
            ],
        },
        {
            featureType: "road.arterial",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#cfcfcf",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "geometry.fill",
            stylers: [
                {
                    color: "#90d59c",
                },
            ],
        },
        {
            featureType: "road.highway",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#598860",
                },
            ],
        },
        {
            featureType: "road.highway.controlled_access",
            elementType: "geometry.fill",
            stylers: [
                {
                    color: "#8ac0f0",
                },
            ],
        },
        {
            featureType: "road.highway.controlled_access",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#2e7dc2",
                },
            ],
        },
        {
            featureType: "road.local",
            elementType: "geometry.fill",
            stylers: [
                {
                    color: "#fcfcfc",
                },
            ],
        },
        {
            featureType: "road.local",
            elementType: "geometry.stroke",
            stylers: [
                {
                    color: "#93d3fb",
                },
            ],
        },
        {
            featureType: "transit",
            stylers: [
                {
                    visibility: "off",
                },
            ],
        },
        {
            featureType: "water",
            elementType: "geometry",
            stylers: [
                {
                    color: "#bde6fa",
                },
            ],
        },
    ],
};
