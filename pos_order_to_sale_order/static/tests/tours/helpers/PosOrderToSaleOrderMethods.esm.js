/** @odoo-module **/
/*
    Copyright 2024 Camptocamp SA (https://www.camptocamp.com).
    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/

import {Do} from "point_of_sale.tour.ProductScreenTourMethods";
import {createTourMethods} from "point_of_sale.tour.utils";

class DoExt extends Do {
    clickCreateOrderButton() {
        return [
            {
                content: "Click on 'Create Order' Button",
                trigger:
                    ".control-buttons .control-button span:contains('Create Order')",
            },
        ];
    }
    clickCreateInvoicedOrderButton() {
        return [
            {
                content: "Click on 'Create invoiced order' Button",
                trigger:
                    ".popup-create-sale-order .button-sale-order span:contains('Create Invoiced Sale Order')",
            },
            // Wait for the request to complete
            {
                content: "Wait for popup to be closed",
                trigger: "body:not(:has(div.popup-create-sale-order:not(.oe_hidden))",
                run: () => {}, // eslint-disable-line no-empty-function
            },
        ];
    }
    addCommitmentDate() {
        return [
            {
                content: "Add Commitment Date",
                trigger: ".popup-create-sale-order input[name='commitment_date']",
                run: () => {
                    this.trigger("input", {
                        target: {value: "2024-01-01T16:00:00"},
                    });
                },
            },
        ];
    }
}

const methods = createTourMethods("PosOrderToSaleOrder", DoExt);
export const PosOrderToSaleOrder = methods.PosOrderToSaleOrder;
