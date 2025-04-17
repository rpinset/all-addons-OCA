import {WebClient} from "@web/webclient/webclient";
import {patch} from "@web/core/utils/patch";

patch(WebClient.prototype, {
    setup() {
        super.setup();
        // Patch the bus notification handling
        const originalNotifyCallback = this.env.services.bus_service._notifCallback;
        this.env.services.bus_service._notifCallback = (notifications) => {
            let processedNotifications = notifications;
            const shuttleNotifications = notifications.filter((n) =>
                this.isShuttleNotification(n)
            );

            if (shuttleNotifications.length > 0) {
                const filteredShuttleNotifications =
                    this.filterShuttleNotifications(shuttleNotifications);
                processedNotifications = notifications.filter(
                    (n) =>
                        !this.isShuttleNotification(n) ||
                        filteredShuttleNotifications.includes(n)
                );
            }
            originalNotifyCallback(processedNotifications);
        };
    },

    isShuttleNotification([, message]) {
        return message?.params?.shuttle_info !== undefined;
    },

    filterShuttleNotifications(notifications) {
        const filteredNotifications = [];
        const pathParts = globalThis.location.pathname.split("/");
        // Find model in the path and get the next element as ID
        const shuttleModels = this.getShuttleModels();
        let recModel = null;
        let recId = null;

        for (let i = 0; i < pathParts.length; i++) {
            if (shuttleModels.includes(pathParts[i])) {
                recModel = pathParts[i];
                const parsedId = parseInt(pathParts[i + 1], 10);
                recId = isNaN(parsedId) ? -1 : parsedId;
                break;
            }
        }
        const isValidShuttlePage =
            this.getShuttleModels().includes(recModel) && recId > 0;

        if (isValidShuttlePage) {
            for (const notification of notifications) {
                const [, message] = notification;
                const shuttleInfo = message.params.shuttle_info;
                if (shuttleInfo[recModel] === recId) {
                    filteredNotifications.push(notification);
                }
            }
        }
        return filteredNotifications;
    },

    getShuttleModels() {
        return [
            "vertical.lift.shuttle",
            "vertical.lift.operation.inventory",
            "vertical.lift.operation.pick",
            "vertical.lift.operation.put",
        ];
    },
});
