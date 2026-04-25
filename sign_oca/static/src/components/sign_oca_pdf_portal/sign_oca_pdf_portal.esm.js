/** @odoo-module **/

const {App, mount, useRef} = owl;

import SignOcaPdfCommon from "../sign_oca_pdf_common/sign_oca_pdf_common.esm.js";

import env from "web.public_env";
import {registry} from "@web/core/registry";
import {renderToString} from "@web/core/utils/render";
import session from "web.session";
import {templates} from "@web/core/assets";
const SignRegistry = registry.category("sign_oca");
import {startSignItemNavigator} from "./sign_oca_navigator.esm";

export class SignOcaPdfPortal extends SignOcaPdfCommon {
    setup() {
        super.setup(...arguments);
        this.to_sign = false;
        this.signOcaFooter = useRef("sign_oca_footer");
    }
    async willStart() {
        this.info = await this.env.services.rpc({
            route:
                "/sign_oca/info/" +
                this.props.signer_id +
                "/" +
                this.props.access_token,
        });
    }

    getPdfUrl() {
        return (
            "/sign_oca/content/" + this.props.signer_id + "/" + this.props.access_token
        );
    }
    checkToSign() {
        this.to_sign = this.to_sign_update;
        if (this.to_sign_update) {
            $(this.signOcaFooter.el).show();
            $("#sign_oca_button").removeAttr("disabled");
        } else {
            $(this.signOcaFooter.el).hide();
            $("#sign_oca_button").prop("disabled", true);
        }
    }
    postIframeField(item) {
        /* eslint-disable */
        var result = undefined;
        /* eslint-enable */
        if (item.role_id === this.info.role_id) {
            var signatureItem = super.postIframeField(...arguments);
            signatureItem[0].append(
                SignRegistry.get(item.field_type).generate(this, item, signatureItem)
            );
            result = signatureItem;
        }
        this.checkFilledAll();
        return result;
    }
    async _onClickSign() {
        const position = await this.getLocation();
        this.env.services
            .rpc({
                route:
                    "/sign_oca/sign/" +
                    this.props.signer_id +
                    "/" +
                    this.props.access_token,
                params: {
                    items: this.info.items,
                    latitude: position && position.coords && position.coords.latitude,
                    longitude: position && position.coords && position.coords.longitude,
                },
            })
            .then((action) => {
                // As we are on frontend env, it is not possible to use do_action(), so we
                // redirect to the corresponding URL or reload the page if the action is not
                // an url.
                if (action.type === "ir.actions.act_url") {
                    window.location = action.url;
                } else {
                    window.location.reload();
                }
            });
    }
    _trigger_up(ev) {
        const evType = ev.name;
        const payload = ev.data;
        if (evType === "call_service") {
            let args = payload.args || [];
            if (payload.service === "ajax" && payload.method === "rpc") {
                // Ajax service uses an extra 'target' argument for rpc
                args = args.concat(ev.target);
            }
            const service = this.env.services[payload.service];
            const result = service[payload.method].apply(service, args);
            payload.callback(result);
        } else if (evType === "get_session") {
            if (payload.callback) {
                payload.callback(this.env.session);
            }
        } else if (evType === "load_views") {
            const params = {
                model: payload.modelName,
                context: payload.context,
                views_descr: payload.views,
            };
            this.env.dataManager
                .load_views(params, payload.options || {})
                .then(payload.on_success);
        } else if (evType === "load_filters") {
            return this.env.dataManager.load_filters(payload).then(payload.on_success);
        } else {
            payload.__targetWidget = ev.target;
            this.trigger(evType.replace(/_/g, "-"), payload);
        }
    }
    async getLocation() {
        if (!this.info.ask_location || !navigator.geolocation) {
            return {};
        }
        try {
            return await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject);
            });

            // Do something with the latitude and longitude
        } catch (error) {
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    console.debug("User denied the request for geolocation.");
                    break;
                case error.POSITION_UNAVAILABLE:
                    console.debug("Location information is unavailable.");
                    break;
                case error.TIMEOUT:
                    console.debug("The request to get user location timed out.");
                    break;
                default:
                    console.debug("An unknown error occurred.");
                    break;
            }
        }
        return {};
    }
    checkFilledAll() {
        this.to_sign_update =
            _.filter(this.info.items, (item) => {
                return (
                    item.required &&
                    item.role_id === this.info.role_id &&
                    !SignRegistry.get(item.field_type).check(item)
                );
            }).length === 0;
        this.checkToSign();
    }
    postIframeFields() {
        super.postIframeFields(...arguments);
        // Is essential to make sure the navigator will never duplicate
        const target = $(
            this.iframe.el.contentDocument.getElementById("viewerContainer")
        );
        const navigator = $(
            this.iframe.el.contentDocument.getElementsByClassName(
                "o_sign_sign_item_navigator"
            )
        );
        const navLine = $(
            this.iframe.el.contentDocument.getElementsByClassName(
                "o_sign_sign_item_navline"
            )
        );
        if (navLine.length === 0) {
            target.append($("<div class='o_sign_sign_item_navline'/>"));
        }
        if (navigator.length === 0) {
            target.append($("<div class='o_sign_sign_item_navigator'/>"));
        }
        // Load navigator
        this.navigate();
    }
    navigate() {
        const target = this.iframe.el.contentDocument.getElementById("viewerContainer");
        this.navigator = startSignItemNavigator(this, target, this.env);
    }
}
SignOcaPdfPortal.template = "sign_oca.SignOcaPdfPortal";
SignOcaPdfPortal.props = {
    access_token: {type: String},
    signer_id: {type: Number},
};
export function initDocumentToSign(properties) {
    return session.session_bind(session.origin).then(function () {
        return Promise.all([
            session.load_translations(["web", "portal", "sign_oca"]),
        ]).then(async function () {
            var app = new App(null, {templates, test: true});
            renderToString.app = app;

            let dialogService = env.services.dialog;
            const dialogServiceInterval = setInterval(() => {
                if (dialogService) {
                    clearInterval(dialogServiceInterval);
                    mount(SignOcaPdfPortal, document.body, {
                        env,
                        props: properties,
                        templates: templates,
                    });
                } else {
                    dialogService = env.services.dialog;
                }
            }, 100);
        });
    });
}
