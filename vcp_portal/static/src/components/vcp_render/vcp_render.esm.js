import {Component, markup, onMounted, useState} from "@odoo/owl";
import {Dropdown} from "@web/core/dropdown/dropdown";
import {DropdownItem} from "@web/core/dropdown/dropdown_item";
import {PopoverTooltip} from "../popover_tooltip/popover_tooltip.esm";
import {formatFloat} from "@web/core/utils/numbers";
import {registry} from "@web/core/registry";
import {renderToString} from "@web/core/utils/render";
import {rpc} from "@web/core/network/rpc";
import {usePopover} from "@web/core/popover/popover_hook";

export class VcpRender extends Component {
    static template = "vcp_portal.VcpRender";
    setup() {
        const year = new Date().getFullYear();
        const month = new Date().getMonth() + 1;
        this.state = useState({
            sort: {
                contributors: "index",
                organizations: "merged_pull_requests",
                repositories: "merged_pull_requests",
            },
            columns: {},
            period: "YTD",
            contributors: [],
            organizations: [],
            repositories: [],
            year: month === 1 ? year - 1 : year,
            month: (month === 1 ? 12 : month - 1).toString(),
            kind: "contributors",
        });
        onMounted(this.fetchData.bind(this));
        this.popover = usePopover(PopoverTooltip);
    }
    selectPeriod(period) {
        this.state.period = period;
        this.fetchData();
    }
    initColumnTooltip(ev, column) {
        this.popover.open(ev.currentTarget, {
            content: markup(column.tooltip),
        });
    }
    initDateTooltip(ev) {
        this.popover.open(ev.currentTarget, {
            content: markup(renderToString("vcp_portal.DateSelectionTooltip")),
        });
    }
    async fetchData() {
        const data = await rpc("/vcp-fetch", this.getParameters());
        if (this.state.kind === "contributors") {
            this.state.contributors = data.data;
        } else if (this.state.kind === "organizations") {
            this.state.organizations = data.data;
        } else if (this.state.kind === "repositories") {
            this.state.repositories = data.data;
        }
        this.state.columns = data.columns;
        return data;
    }
    getParameters() {
        return {
            year: parseInt(this.state.year, 10),
            month: parseInt(this.state.month, 10),
            vcp_id: this.props.vcp,
            kind: this.state.kind,
            period: this.state.period,
        };
    }
    get rowIds() {
        if (this.state.kind === "contributors") {
            return Object.keys(this.state.contributors).sort(
                (a, b) =>
                    this.state.contributors[b][this.state.sort.contributors] -
                    this.state.contributors[a][this.state.sort.contributors]
            );
        } else if (this.state.kind === "organizations") {
            return Object.keys(this.state.organizations).sort(
                (a, b) =>
                    this.state.organizations[b][this.state.sort.organizations] -
                    this.state.organizations[a][this.state.sort.organizations]
            );
        } else if (this.state.kind === "repositories") {
            return Object.keys(this.state.repositories).sort(
                (a, b) =>
                    this.state.repositories[b][this.state.sort.repositories] -
                    this.state.repositories[a][this.state.sort.repositories]
            );
        }
        return [];
    }
    getRowData(row_id) {
        if (this.state.kind === "organizations") {
            return this.state.organizations[row_id];
        }
        if (this.state.kind === "repositories") {
            return this.state.repositories[row_id];
        }
        if (this.state.kind === "contributors") {
            return this.state.contributors[row_id];
        }
        return {};
    }
    formatFloat(value, digits) {
        return formatFloat(value, {digits: [digits, digits]});
    }
    setKind(kind) {
        this.state.kind = kind;
        this.fetchData();
    }
    sortBy(field) {
        this.state.sort[this.state.kind] = field;
    }
}

VcpRender.props = {
    vcp: Number,
};
VcpRender.components = {
    Dropdown,
    DropdownItem,
};
registry.category("public_components").add("vcp_portal.VcpRender", VcpRender);
