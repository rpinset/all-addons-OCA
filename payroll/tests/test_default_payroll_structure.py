# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.payroll.tests.common import TestPayslipBase


class TestDefaultPayrollStructure(TestPayslipBase):
    """Default salary structure resolution (employee then company)."""

    def setUp(self):
        super().setUp()
        self.company = self.env.company
        self.struct_company = self.developer_pay_structure
        self.struct_employee = self.sales_pay_structure

    # Resolution helper
    def test_resolve_employee_takes_precedence(self):
        self.company.payroll_structure_id = self.struct_company
        self.richard_emp.payroll_structure_id = self.struct_employee
        resolved = self.Contract._get_default_payroll_structure(self.richard_emp)
        self.assertEqual(resolved, self.struct_employee)

    def test_resolve_falls_back_to_company(self):
        self.company.payroll_structure_id = self.struct_company
        self.richard_emp.payroll_structure_id = False
        resolved = self.Contract._get_default_payroll_structure(self.richard_emp)
        self.assertEqual(resolved, self.struct_company)

    def test_resolve_empty_when_no_default(self):
        self.company.payroll_structure_id = False
        self.richard_emp.payroll_structure_id = False
        resolved = self.Contract._get_default_payroll_structure(self.richard_emp)
        self.assertFalse(resolved)

    # Onchange (UI)
    def test_onchange_fills_when_empty(self):
        self.company.payroll_structure_id = self.struct_company
        contract = self.Contract.new({"name": "C", "employee_id": self.richard_emp.id})
        contract._onchange_employee_id_default_structure()
        self.assertEqual(contract.struct_id, self.struct_company)

    def test_onchange_updates_when_employee_changes(self):
        self.company.payroll_structure_id = self.struct_company
        self.richard_emp.payroll_structure_id = self.struct_employee
        contract = self.Contract.new(
            {
                "name": "C",
                "employee_id": self.richard_emp.id,
                "struct_id": self.struct_company.id,
            }
        )
        contract._onchange_employee_id_default_structure()
        self.assertEqual(contract.struct_id, self.struct_employee)

    # Mismatch warning (UI)
    def test_warning_when_struct_differs_from_default(self):
        self.richard_emp.payroll_structure_id = self.struct_employee
        contract = self.Contract.new(
            {
                "name": "C",
                "employee_id": self.richard_emp.id,
                "struct_id": self.struct_company.id,
            }
        )
        res = contract._onchange_struct_id_default_warning()
        self.assertTrue(res and res.get("warning"))

    def test_no_warning_when_struct_matches_default(self):
        self.richard_emp.payroll_structure_id = self.struct_employee
        contract = self.Contract.new(
            {
                "name": "C",
                "employee_id": self.richard_emp.id,
                "struct_id": self.struct_employee.id,
            }
        )
        self.assertFalse(contract._onchange_struct_id_default_warning())

    def test_no_warning_when_no_default(self):
        self.company.payroll_structure_id = False
        self.richard_emp.payroll_structure_id = False
        contract = self.Contract.new(
            {
                "name": "C",
                "employee_id": self.richard_emp.id,
                "struct_id": self.struct_company.id,
            }
        )
        self.assertFalse(contract._onchange_struct_id_default_warning())
