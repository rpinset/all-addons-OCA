import {Component} from "@odoo/owl";

export class PopoverTooltip extends Component {
    static template = "vcp_portal.PopoverTooltip";
    static props = {
        content: String,
    };
}
