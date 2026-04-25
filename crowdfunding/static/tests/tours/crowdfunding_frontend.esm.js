import {registry} from "@web/core/registry";

export function crowdfunding_frontend_steps(values) {
    return [
        {
            content: "Select the first challenge",
            trigger: "main .card a[href$='-1']",
            run: "click",
        },
        {
            content: "Click the pledge button",
            trigger: "main .nav a[href$='crowdfunding/1/pay']",
            run: "click",
        },
        {
            content: "Fill in your name",
            trigger: "input#name",
            run: "fill Firstname Lastname",
        },
        {
            content: "Fill in your email",
            trigger: "input#email",
            run: "fill firstname.lastname@email.com",
        },
        {
            content: "Fill in your street",
            trigger: "input#street",
            run: "fill Streetname 42",
        },
        {
            content: "Fill in your zipcode",
            trigger: "input#zip",
            run: "fill " + values.zip,
        },
        {
            content: "Fill in your city",
            trigger: "input#city",
            run: "fill Testcity",
        },
        {
            content: "Fill in your country",
            trigger: "select#country_id",
            run: () => {
                $("select#country_id option:contains(" + values.country + ")").prop(
                    "selected",
                    true
                );
            },
        },
        {
            content: "Submit your credentials",
            trigger: "main form button[type='submit']",
            run: "click",
        },
        {
            content: "Fill in an amount",
            trigger: "main input#amount",
            run: "fill 4242",
        },
        {
            content: "Submit amount",
            trigger: "main form button[type='submit']",
            run: "click",
        },
        {
            content: "Submit payment",
            trigger: "main form#o_payment_form button[name='o_payment_submit_button']",
            run: "click",
        },
        {
            content: "Payment done",
            trigger: "#o_payment_status_message",
        },
    ];
}

registry.category("web_tour.tours").add("crowdfunding_frontend_us", {
    test: true,
    url: "/crowdfunding",
    steps: () =>
        crowdfunding_frontend_steps({
            zip: "4242",
            country: "United States",
        }),
});

registry.category("web_tour.tours").add("crowdfunding_frontend_nl", {
    test: true,
    url: "/crowdfunding",
    steps: () =>
        crowdfunding_frontend_steps({
            zip: "4242AB",
            country: "Netherlands",
        }),
});
