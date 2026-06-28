To configure tier validation for HR expenses:

1. Go to *Settings > Technical > Tier Validations > Tier Definition*
2. Set the model to **Expense Report** (`hr.expense.sheet`).
3. Create the desired approval tiers with the appropriate conditions.

To define exception fields that can still be edited while the expense is under or after tier validation:

1. Go to *Settings > Technical > Tier Validations > Tier Validation Exceptions*
2. Create a new exception for model **Expense Report** (`hr.expense.sheet`) or **Expense** (`hr.expense`):
   - **Under Validation** — fields allowed to be modified while the expense sheet is in *Submitted* state and awaiting tier approval. Set *Allowed to Write Under Validation*.
   - **After Validation** — fields allowed to be modified after the expense sheet is fully approved (*Approved*, *Posted*, *Done*). Set *Allowed to Write After Validation*.
3. Optionally restrict the exception to specific user groups.
4. Add the field(s) you want to allow editing.
