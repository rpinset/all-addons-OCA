import re


def check_all_accounts_loaded(self, wizard_model, **kwargs):
    # Checks if all accounts which code is number are loaded
    # when the account_code_ fields changed
    all_accounts = (
        self.env["account.account"]
        .search([], order="code")
        .filtered(lambda acc: re.fullmatch(r"[0-9]+(\.[0-9]+)?", acc.code))
    )
    company = self.env.user.company_id
    wizard = self.env[wizard_model].create(
        {
            "target_move": "posted",
            "hide_account_at_0": False,
            "company_id": company.id,
            "fy_start_date": self.fy_date_start,
            "account_code_from": self.account001.id,
            "account_code_to": all_accounts[-1].id,
            **kwargs,
        }
    )
    wizard.on_change_account_range()
    # sets are needed because some codes are duplicated and
    # thus the length of all_accounts would be higher
    all_accounts_code_set = set()
    wizard_code_set = set()
    [all_accounts_code_set.add(account.code) for account in all_accounts]
    [wizard_code_set.add(account.code) for account in wizard.account_ids]
    self.assertEqual(len(wizard_code_set), len(all_accounts_code_set))
    self.assertTrue(wizard_code_set == all_accounts_code_set)
