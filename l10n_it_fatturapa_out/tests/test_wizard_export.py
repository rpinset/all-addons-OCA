#  Copyright 2026 Nextev Srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo.tests import tagged
from odoo.tools.safe_eval import safe_eval

from .fatturapa_common import FatturaPACommon


@tagged("post_install", "-at_install")
class TestWizardExport(FatturaPACommon):
    def _get_wizard_model(self):
        """Get the export wizard as a non admin user opens it.

        The wizard is opened by the 'Export Electronic Invoice' item
        of the invoices' 'Action' menu, so its action passes
        the invoices' model in the context.
        """
        self.assertFalse(
            self.account_manager.has_group("base.group_system"),
            "These tests require a non admin user",
        )
        return self.wizard_model.with_user(self.account_manager).with_context(
            active_model=self.invoice_model._name,
        )

    def _get_report_print_menu_domain(self, wizard_model):
        """Get the domain of `report_print_menu` like the client does.

        When the wizard's form is loaded, the client gets the domain
        from the view, if it is set there,
        otherwise from the field's definition;
        then it evaluates the domain against the values of the record
        being created, that at that point are only the default ones.
        """
        arch = etree.fromstring(wizard_model.get_view(view_type="form")["arch"])
        field_nodes = arch.xpath("//field[@name='report_print_menu']")
        self.assertTrue(field_nodes, "report_print_menu field not found in the view")

        domain = field_nodes[0].get("domain")
        if domain is None:
            domain = wizard_model.fields_get(
                allfields=["report_print_menu"],
                attributes=["domain"],
            )["report_print_menu"]["domain"]

        if isinstance(domain, str):
            field_names = list(wizard_model._fields)
            default_values = wizard_model.default_get(field_names)
            eval_context = {
                field_name: default_values.get(field_name, False)
                for field_name in field_names
            }
            eval_context["context"] = wizard_model.env.context
            domain = safe_eval(domain, eval_context)
        self.assertIsInstance(domain, list, f"{domain} is not a valid domain")
        return domain

    def test_report_print_menu_selection(self):
        """A non admin user can open the export wizard.

        Filling the selection of `report_print_menu` is the last thing
        the client does when the wizard's form is loaded:
        it searches the reports allowed by the field's domain.
        A domain referring to `ir.actions.report` `binding_model_id`
        by model name makes this search raise an AccessError,
        because non admin users cannot search `ir.model`.
        """
        wizard_model = self._get_wizard_model()

        domain = self._get_report_print_menu_domain(wizard_model)

        wizard_model.env["ir.actions.report"].name_search("", args=domain)

    def test_report_print_menu_bound_reports(self):
        """Only the reports shown in the invoices' 'Print' menu can be selected.

        `model` and `binding_model_id` are not interchangeable:
        a report might have `account.move` as `model`
        but not be shown in the invoices' 'Print' menu.
        """
        report_model = self.env["ir.actions.report"].sudo()
        bound_report = report_model.create(
            {
                "name": "Test bound report",
                "model": self.invoice_model._name,
                "report_name": "l10n_it_fatturapa_out.test_bound_report",
                "binding_model_id": self.env["ir.model"]
                ._get(self.invoice_model._name)
                .id,
            }
        )
        not_bound_report = report_model.create(
            {
                "name": "Test not bound report",
                "model": self.invoice_model._name,
                "report_name": "l10n_it_fatturapa_out.test_not_bound_report",
                "binding_model_id": False,
            }
        )
        wizard_model = self._get_wizard_model()

        domain = self._get_report_print_menu_domain(wizard_model)

        selectable_reports = wizard_model.env["ir.actions.report"].search(domain)
        self.assertIn(bound_report, selectable_reports)
        self.assertNotIn(not_bound_report, selectable_reports)
