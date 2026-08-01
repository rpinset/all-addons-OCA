import {Component, useRef} from "@odoo/owl";
import {GoogleMapRenderer} from "./google_map_renderer.esm";
import {Layout} from "@web/search/layout";
import {executeButtonCallback} from "@web/views/view_button/view_button_hook";

export class GoogleMapController extends Component {
    static template = "web_view_google_map.GoogleMapView";
    static components = {Layout, GoogleMapRenderer};
    static props = {
        "*": true,
    };

    setup() {
        this.rootRef = useRef("root");
    }

    async onClickCreate() {
        return executeButtonCallback(this.rootRef.el, () => this.createRecord());
    }

    async createRecord() {
        if (this.props.createRecord) {
            await this.props.createRecord();
        }
    }
}
