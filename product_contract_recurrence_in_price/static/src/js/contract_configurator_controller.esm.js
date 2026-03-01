/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {ProductContractConfiguratorController} from "@product_contract/js/contract_configurator_controller.esm";

patch(ProductContractConfiguratorController.prototype, {
    _getProductContractConfiguration(record) {
        const config = super._getProductContractConfiguration(record);
        config.include_recurrence_in_price = record.data.include_recurrence_in_price;
        return config;
    },
});
