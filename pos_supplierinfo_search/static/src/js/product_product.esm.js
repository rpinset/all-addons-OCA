import {ProductProduct} from "@point_of_sale/app/models/product_product";
import {patch} from "@web/core/utils/patch";

patch(ProductProduct.prototype, {
    get searchString() {
        let res = super.searchString;
        const supplier_data_list = JSON.parse(this.supplier_data_json || "[]");
        for (var i = 0, len = supplier_data_list.length; i < len; i++) {
            var supplier_data = supplier_data_list[i];
            if (supplier_data.supplier_name) {
                res += "|" + supplier_data.supplier_name.replace(/:/g, "");
            }
            if (supplier_data.supplier_product_code) {
                res += "|" + supplier_data.supplier_product_code.replace(/:/g, "");
            }
            if (supplier_data.supplier_product_name) {
                res += "|" + supplier_data.supplier_product_name.replace(/:/g, "");
            }
        }
        return res;
    },
});
