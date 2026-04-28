odoo.define("pos_partner_is_company.PartnerDetailsEdit", function (require) {
    const {useState} = owl;
    const PartnerDetailsEdit = require("point_of_sale.PartnerDetailsEdit");
    const Registries = require("point_of_sale.Registries");

    const PosPartnerDetailsEdit = (OriginalPartnerDetailsEdit) =>
        class extends OriginalPartnerDetailsEdit {
            setup() {
                super.setup();
                this.changes = useState({
                    ...this.changes,
                    is_company: this.props.partner.is_company || false,
                });
            }
        };

    Registries.Component.extend(PartnerDetailsEdit, PosPartnerDetailsEdit);

    return PosPartnerDetailsEdit;
});
