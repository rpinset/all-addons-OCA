/** @odoo-module **/
/*
  Copyright 2025 Akretion France (https://www.akretion.com/)
  @author: Alexis de Lattre <alexis.delattre@akretion.com>
  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
*/

import {
    AccountDropZone,
    DashboardKanbanRecord,
    DashboardKanbanRenderer,
} from "@account/components/bills_upload/bills_upload";
import {kanbanView} from "@web/views/kanban/kanban_view";
import {onWillStart} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

export class DashboardKanbanRendererBanner extends DashboardKanbanRenderer {
    setup() {
        super.setup();
        this.orm = useService("orm");

        onWillStart(async () => {
            this.state.banner = await this.orm.call(
                "account.dashboard.banner.cell",
                "get_banner_data"
            );
        });
    }
}

DashboardKanbanRendererBanner.components = {
    ...DashboardKanbanRenderer.components,
    AccountDropZone,
    KanbanRecord: DashboardKanbanRecord,
};
DashboardKanbanRendererBanner.template =
    "account_dashboard_banner.AccountDashboardBannerRenderer";

export const accountDashboardKanbanBanner = {
    ...kanbanView,
    Renderer: DashboardKanbanRendererBanner,
};

registry
    .category("views")
    .add("account_dashboard_kanban_banner", accountDashboardKanbanBanner);
