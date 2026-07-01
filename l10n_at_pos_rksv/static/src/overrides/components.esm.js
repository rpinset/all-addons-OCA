// Copyright 2024 Weboffice IT-Service und Marketing GmbH & Co KG <https://weboffice.at>
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import {OrderReceipt} from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import {generateQRCodeDataUrl} from "@point_of_sale/utils";
import {patch} from "@web/core/utils/patch";

patch(OrderReceipt.prototype, {
    get asignQrCode() {
        return generateQRCodeDataUrl(this.order.asign_qrcode);
    },
});
