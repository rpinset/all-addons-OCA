import {registry} from "@web/core/registry";

console.log("Registering portal_load_vcp tour");
registry.category("web_tour.tours").add("portal_load_vcp", {
    url: "/my",
    steps: () => [
        {
            content: "Check portal is loaded and Find Contributors menu",
            trigger: 'a[href*="/vcp"]:contains("Version Control Platforms"):first',
            run: "click",
            expectUnloadPage: true,
        },
        {
            content: "Check Contributors Page",
            trigger: 'a[href*="/vcp/oca"]:contains("OCA"):first',
            run: "click",
            expectUnloadPage: true,
        },
        {
            content: "Check Contributors Page",
            trigger: "owl-component",
        },
        {
            content: "Check Etobella",
            trigger: 'span:contains("Enric Tobella"):first',
        },
        {
            content: "Check LuisDixmit",
            trigger: 'span:contains("Luis Rodriguez"):first',
        },
        {
            content: "Check JordiBForgeFlow",
            trigger: 'span:contains("Jordi Ballester"):first',
        },
        {
            content: "Check Etobella Created Value",
            trigger: 'tr:contains("Enric Tobella") td:nth-child(2):contains("1"):first',
        },
        {
            content: "Check LuisDixmit Created Value",
            trigger:
                'tr:contains("Luis Rodriguez") td:nth-child(2):contains("1"):first',
        },
        {
            content: "Check JordiBForgeFlow Created Value",
            trigger:
                'tr:contains("Jordi Ballester") td:nth-child(2):contains("1"):first',
        },
        {
            content: "Check Etobella Merged Value",
            trigger: 'tr:contains("Enric Tobella") td:nth-child(3):contains("1"):first',
        },
        {
            content: "Check LuisDixmit Merged Value",
            trigger:
                'tr:contains("Luis Rodriguez") td:nth-child(3):contains("0"):first',
        },
        {
            content: "Check JordiBForgeFlow Merged Value",
            trigger:
                'tr:contains("Jordi Ballester") td:nth-child(3):contains("0"):first',
        },
        {
            content: "Change to Repositories",
            trigger: ".o_vcp_repositories button",
            run: "click",
        },
        {
            content: "Check Repository",
            trigger: 'span:contains("contributors-module"):first',
        },
        {
            content: "Check Created Requests Value",
            trigger:
                'tr:contains("contributors-module") td:nth-child(2):contains("3"):first',
        },
        {
            content: "Check Merged Requests Value",
            trigger:
                'tr:contains("contributors-module") td:nth-child(3):contains("1"):first',
        },
        {
            content: "Change to Organizations",
            trigger: ".o_vcp_organizations button",
            run: "click",
        },
        {
            content: "Check Dixmit",
            trigger: 'tr:contains("Dixmit"):first',
        },
        {
            content: "Check ForgeFlow",
            trigger: 'tr:contains("ForgeFlow"):first',
        },
        {
            content: "Check Dixmit Created Pull Requests Value",
            trigger: 'tr:contains("Dixmit") td:nth-child(2):contains("2"):first',
        },
        {
            content: "Check ForgeFlow Created Pull Requests Value",
            trigger: 'tr:contains("ForgeFlow") td:nth-child(2):contains("1"):first',
        },
        {
            content: "Check Dixmit Merged Pull Requests Value",
            trigger: 'tr:contains("Dixmit") td:nth-child(3):contains("1"):first',
        },
        {
            content: "Check ForgeFlow Merged Pull Requests Value",
            trigger: 'tr:contains("ForgeFlow") td:nth-child(3):contains("0"):first',
        },
    ],
});
