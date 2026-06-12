import {MailComposerTemplateSelector} from "@mail/core/web/mail_composer_template_selector";
import {patch} from "@web/core/utils/patch";

patch(MailComposerTemplateSelector.prototype, {
    setup() {
        super.setup(...arguments);
        // It is important to increase this limit to prevent a situation where,
        // for example, 7 templates are retrieved but only the first 3 are displayed;
        // since the “Search more” option is not shown, it would not be possible to
        // access all of them.
        // TODO: Delete at 20.0 (https://github.com/odoo/odoo/blob/adab3e6898bb3a65da3217630b89f2d217142ad4/addons/mail/static/src/core/web/mail_composer_template_selector.js#L20)
        this.limit = 80;
    },
    async fetchTemplates() {
        await super.fetchTemplates();
        const templates = this.state.templates || [];
        const domain = this.props.record.data.domain_template_id;
        if (!domain || !domain.length) {
            return;
        }
        const templates2 = await this.orm.searchRead("mail.template", domain, [
            "display_name",
        ]);
        const validIds = new Set(templates2.map((t) => t.id));
        this.state.templates = templates.filter((t) => validIds.has(t.id));
    },
});
