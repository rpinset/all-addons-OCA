odoo.define("pos_container_deposit.test_tour", function (require) {
    "use strict";

    const {ProductScreen} = require("point_of_sale.tour.ProductScreenTourMethods");
    const {getSteps, startSteps} = require("point_of_sale.tour.utils");
    const Tour = require("web_tour.tour");
    const product_name = "Generic sugar liquid";
    const deposit_product_name = "Bottle deposit .25";

    startSteps();

    ProductScreen.do.clickHomeCategory();
    ProductScreen.do.clickDisplayedProduct(product_name);
    ProductScreen.do.clickDisplayedProduct(product_name);
    ProductScreen.check.checkOrderlinesNumber(2);
    ProductScreen.check.selectedOrderlineHas(product_name);
    getSteps().push({
        content: `selecting orderline with product '${deposit_product_name}' and quantity '2.0'`,
        trigger: `.order .orderline:not(:has(.selected)) .product-name:contains("${deposit_product_name}") ~ .info-list em:contains("2.0")`,
    });
    ProductScreen.check.selectedOrderlineHas(product_name);
    ProductScreen.do.pressNumpad("Price");
    ProductScreen.check.modeIsActive("Price");
    ProductScreen.do.pressNumpad("5");
    ProductScreen.check.selectedOrderlineHas(product_name, "2", "10");
    ProductScreen.do.clickDisplayedProduct(product_name);
    ProductScreen.do.clickDisplayedProduct(product_name);
    ProductScreen.check.checkOrderlinesNumber(4);
    ProductScreen.do.pressNumpad("Qty");
    ProductScreen.do.pressNumpad("Backspace");
    ProductScreen.do.pressNumpad("Backspace");
    ProductScreen.check.modeIsActive("Qty");
    ProductScreen.check.selectedOrderlineHas(product_name, "2", "10");
    ProductScreen.check.checkOrderlinesNumber(2);
    ProductScreen.do.pressNumpad("Qty");
    ProductScreen.do.pressNumpad("Backspace");
    ProductScreen.do.pressNumpad("Backspace");
    ProductScreen.check.modeIsActive("Qty");
    ProductScreen.check.orderIsEmpty();

    Tour.register(
        "pos_container_deposit.test_tour",
        {test: true, url: "/pos/ui"},
        getSteps()
    );
});
