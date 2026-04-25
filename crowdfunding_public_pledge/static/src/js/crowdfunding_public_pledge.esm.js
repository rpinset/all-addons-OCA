import publicWidget from "@web/legacy/js/public/public_widget";
import {rpc} from "@web/core/network/rpc";

export const CrowdfundingPublicPledgePortalInvoiceForm = publicWidget.Widget.extend({
    selector: ".crowdfunding_public_pledge_portal_invoice_form",
    events: {
        "change #crowdfunding_public_pledge_flag": "_onchangePublic",
    },

    _onchangePublic: async function () {
        const is_public =
            this.$el.find("#crowdfunding_public_pledge_flag:checked").length > 0;
        const access_token = new URLSearchParams(document.location.search).get(
            "access_token"
        );
        await rpc(this.$el.data("flag-route"), {
            access_token: access_token,
            is_public: is_public,
        });
        this.$el.find("#crowdfunding_public_pledge_link").toggle(is_public);
    },
});

publicWidget.registry.CrowdfundingPublicPledgePortalInvoiceForm =
    CrowdfundingPublicPledgePortalInvoiceForm;
