/* global document */
import * as Chrome from "@point_of_sale/../tests/tours/utils/chrome_util";
import * as Dialog from "@point_of_sale/../tests/tours/utils/dialog_util";
import * as ProductScreen from "@point_of_sale/../tests/tours/utils/product_screen_util";

import {inLeftSide} from "@point_of_sale/../tests/tours/utils/common";
import {registry} from "@web/core/registry";

const INFO_BUTTON = ".product-information-tag";
const MODAL_BODY = "main.modal-body";
const SUPPLIER_SECTION = `${MODAL_BODY} .section-supplier`;
const CLOSE_BUTTON = ".modal .btn-close, .modal .close, button.btn-close, button.close";

function openProductInfoPopup(productName) {
    return [
        ProductScreen.clickDisplayedProduct(productName, true),
        inLeftSide([
            {
                trigger: INFO_BUTTON,
                run: "click",
            },
        ]),
        {
            trigger: MODAL_BODY,
        },
    ];
}

registry.category("web_tour.tours").add("pos_supplier_info_visible_for_manager", {
    steps: () =>
        [
            Chrome.startPoS(),
            Dialog.confirm("Open Register"),
            ...openProductInfoPopup("Desk Organizer"),
            {trigger: SUPPLIER_SECTION},
            {trigger: CLOSE_BUTTON, run: "click"},
        ].flat(),
});

registry.category("web_tour.tours").add("pos_supplier_info_hidden_for_non_manager", {
    steps: () =>
        [
            Chrome.startPoS(),
            Dialog.confirm("Open Register"),

            ...openProductInfoPopup("Desk Organizer"),
            {
                trigger: MODAL_BODY,
                run: function () {
                    const root = document.querySelector("main.modal-body");
                    const el = root && root.querySelector(".section-supplier");
                    if (el) {
                        throw new Error(
                            "Supplier section should be hidden for non POS managers."
                        );
                    }
                },
            },
            {trigger: CLOSE_BUTTON, run: "click"},
        ].flat(),
});
