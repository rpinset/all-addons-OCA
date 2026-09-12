import {useService} from "@web/core/utils/hooks";

export function useBarcodeScanner() {
    const api = useService("barcodeApi");

    return {
        call: api.call.bind(api),
        searchRead: api.searchRead.bind(api),
        readGroup: api.readGroup.bind(api),
        read: api.read.bind(api),
        write: api.write.bind(api),
        create: api.create.bind(api),
        unlink: api.unlink.bind(api),
        notify: api.notify.bind(api),
        openDialog: api.openDialog.bind(api),
    };
}
