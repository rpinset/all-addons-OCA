To configure HNB currency rates

Go to *Invoicing > Configuration > Currency update providers*
create new provider : HR-HNB, and configure currencies.

HNB Provides 3 rates: buy, mid and sell. By default mid rate is covered,
as it is only legaly required, but if you want to use buy or sell rate...
there is a config parameter: currency_rate_update_hr_hnb.rate_type
with values accepted: srednji | kupovni | prodajni
