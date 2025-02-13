# Import from DATEV into Odoo

## Requirements

1.  Make sure your user has group 'Full accounting features'
2.  Check if the file you want to import into Odoo is DATEV format .csv
    (move lines start is line 3)
3.  Check the description in order to check if your use case is
    supported
4.  Take care of the limitation to import account moves with taxes

## DATEV Import

1.  Go to Accounting/Actions/DATEV Import
2.  Upload your DATEV format .csv file from your tax advisor
3.  Take care the file format is "DATEV Format .csv" (old version:
    Generic CSV)
4.  Take care your file encoding fits to the provided file (usually
    "Western (Windows-1252)"), if it is the original file from your tax
    advisor
5.  Optionally you may activate "Post Journal Entry" in order to
    immidiately confirm the created Journal Entry
6.  Select the mandatory journal (f.e. "Payroll Account Moves"), usually
    the journal type will be "Miscellaneous"
7.  Enter optionally the "Force Date" field ((will be the field "Date"
    in your Journal Entry)
8.  Enter the mandatory field "Reference" (will be the field "Reference"
    in your Journal Entry)
9.  Enter optionally the field "Force Label" (will be the field "Name"
    in your Journal Items)
10. Finally click on "Run Import"

![image](../static/description/datev_import_csv_wizard.png)

If everyting works fine, you should now see your created Journal Entry
in draft (execept you activated "Post Journal Entry")

## Typical issue

If accounts doesen't exist in Odoo the wizard may interrupt and show you
potential missing accounts.

![image](../static/description/datev_import_csv_wizard_error.png)

In this case you have to ensure to create the missing accounts in Odoo.
