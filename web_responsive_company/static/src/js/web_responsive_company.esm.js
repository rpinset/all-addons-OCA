/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {SwitchCompanyMenu} from "@web/webclient/switch_company_menu/switch_company_menu";
import {useRef, useState} from "@odoo/owl";
import {fuzzyLookup} from "@web/core/utils/search";

patch(SwitchCompanyMenu.prototype, "web_responsive_company.SwitchCompanyMenu", {
    setup() {
        this._super();

        this.state = useState({
            companiesToToggle: [],
            results: Object.values(this.companyService.availableCompanies || {}),
            hasResults: false,
        });
        this.searchInputRef = useRef("SearchBarInput");
    },

    /* Search-input is built on DOM with toggle dropdown
        Can surely be handled more cleanly */
    _onClickToggler() {
        const tryFocus = (retries = 10) => {
            const input = document.querySelector("#search-input");
            if (input) {
                input.focus();
                this._searchCompanies();
            } else if (retries > 0) {
                setTimeout(() => tryFocus(retries - 1), 100);
            }
        };

        tryFocus();
    },

    _searchCompanies() {
        const query = this.searchInputRef.el.value;
        this.state.hasResults = query !== "";
        const companies = Object.values(this.companyService.availableCompanies || {});
        this.state.results = this.state.hasResults
            ? fuzzyLookup(query, companies, (c) => c.name)
            : companies;
    },

    /* Key down on input search bar*/
    _onKeyDownSearchInput(ev) {
        if (ev.code === "Tab" || ev.code === "ArrowDown") {
            if (this.state.results.length) {
                ev.preventDefault();
                document.querySelector(".company-card").focus();
            }
        }
    },

    /* Key down on company cards*/
    _onKeyDownCompanyCard(ev, companyId) {
        if (ev.code === "Enter") {
            this.logIntoCompany(companyId);
        } else if (ev.code === "Space") {
            this.toggleCompany(companyId);
        }
    },
});
