import logging

_logger = logging.getLogger(__name__)


def assign_account_tags(env):
    """Assign tags to specific accounts."""
    # List of account codes and the corresponding tags to assign
    account_tags = {
        "transfer_account_id": "l10n_ch_account_tags.account_tag_ch_106",
        "ch_coa_1060": "l10n_ch_account_tags.account_tag_ch_106",
        "ch_coa_1069": "l10n_ch_account_tags.account_tag_ch_106",
        "ch_coa_1091": "l10n_ch_account_tags.account_tag_ch_106",
        "ch_coa_1099": "l10n_ch_account_tags.account_tag_ch_106",
        "ch_coa_1100": "l10n_ch_account_tags.account_tag_ch_110",
        "ch_coa_1109": "l10n_ch_account_tags.account_tag_ch_110",
        "ch_coa_1140": "l10n_ch_account_tags.account_tag_ch_114",
        "ch_coa_1149": "l10n_ch_account_tags.account_tag_ch_114",
        "ch_coa_1170": "l10n_ch_account_tags.account_tag_ch_114",
        "ch_coa_1171": "l10n_ch_account_tags.account_tag_ch_114",
        "ch_coa_1176": "l10n_ch_account_tags.account_tag_ch_114",
        "ch_coa_1180": "l10n_ch_account_tags.account_tag_ch_114",
        "ch_coa_1189": "l10n_ch_account_tags.account_tag_ch_114",
        "ch_coa_1190": "l10n_ch_account_tags.account_tag_ch_114",
        "ch_coa_1199": "l10n_ch_account_tags.account_tag_ch_114",
        "ch_coa_1200": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1207": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1208": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1209": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1210": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1217": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1218": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1219": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1220": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1230": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1250": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1260": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1267": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1269": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1270": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1277": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1279": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1280": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1287": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1289": "l10n_ch_account_tags.account_tag_ch_120",
        "ch_coa_1300": "l10n_ch_account_tags.account_tag_ch_130",
        "ch_coa_1301": "l10n_ch_account_tags.account_tag_ch_130",
        "ch_coa_1400": "l10n_ch_account_tags.account_tag_ch_140",
        "ch_coa_1409": "l10n_ch_account_tags.account_tag_ch_140",
        "ch_coa_1440": "l10n_ch_account_tags.account_tag_ch_140",
        "ch_coa_1441": "l10n_ch_account_tags.account_tag_ch_140",
        "ch_coa_1449": "l10n_ch_account_tags.account_tag_ch_140",
        "ch_coa_1480": "l10n_ch_account_tags.account_tag_ch_148",
        "ch_coa_1489": "l10n_ch_account_tags.account_tag_ch_148",
        "ch_coa_1500": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1509": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1510": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1519": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1520": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1529": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1530": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1539": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1540": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1549": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1550": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1559": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1570": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1579": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1590": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1599": "l10n_ch_account_tags.account_tag_ch_150",
        "ch_coa_1600": "l10n_ch_account_tags.account_tag_ch_160",
        "ch_coa_1609": "l10n_ch_account_tags.account_tag_ch_160",
        "ch_coa_1700": "l10n_ch_account_tags.account_tag_ch_170",
        "ch_coa_1709": "l10n_ch_account_tags.account_tag_ch_170",
        "ch_coa_1770": "l10n_ch_account_tags.account_tag_ch_170",
        "ch_coa_1779": "l10n_ch_account_tags.account_tag_ch_170",
        "ch_coa_1850": "l10n_ch_account_tags.account_tag_ch_180",
        "ch_coa_2000": "l10n_ch_account_tags.account_tag_ch_200",
        "ch_coa_2030": "l10n_ch_account_tags.account_tag_ch_200",
        "ch_coa_2100": "l10n_ch_account_tags.account_tag_ch_210",
        "ch_coa_2120": "l10n_ch_account_tags.account_tag_ch_210",
        "ch_coa_2140": "l10n_ch_account_tags.account_tag_ch_210",
        "ch_coa_2160": "l10n_ch_account_tags.account_tag_ch_210",
        "ch_coa_2200": "l10n_ch_account_tags.account_tag_ch_220",
        "ch_coa_2201": "l10n_ch_account_tags.account_tag_ch_220",
        "ch_coa_2206": "l10n_ch_account_tags.account_tag_ch_220",
        "ch_coa_2208": "l10n_ch_account_tags.account_tag_ch_220",
        "ch_coa_2210": "l10n_ch_account_tags.account_tag_ch_220",
        "ch_coa_2261": "l10n_ch_account_tags.account_tag_ch_220",
        "ch_coa_2270": "l10n_ch_account_tags.account_tag_ch_220",
        "ch_coa_2279": "l10n_ch_account_tags.account_tag_ch_220",
        "ch_coa_2300": "l10n_ch_account_tags.account_tag_ch_230",
        "ch_coa_2301": "l10n_ch_account_tags.account_tag_ch_230",
        "ch_coa_2330": "l10n_ch_account_tags.account_tag_ch_230",
        "ch_coa_2400": "l10n_ch_account_tags.account_tag_ch_240",
        "ch_coa_2420": "l10n_ch_account_tags.account_tag_ch_240",
        "ch_coa_2430": "l10n_ch_account_tags.account_tag_ch_240",
        "ch_coa_2450": "l10n_ch_account_tags.account_tag_ch_240",
        "ch_coa_2451": "l10n_ch_account_tags.account_tag_ch_240",
        "ch_coa_2500": "l10n_ch_account_tags.account_tag_ch_250",
        "ch_coa_2600": "l10n_ch_account_tags.account_tag_ch_260",
        "ch_coa_2800": "l10n_ch_account_tags.account_tag_ch_280",
        "ch_coa_2900": "l10n_ch_account_tags.account_tag_ch_290",
        "ch_coa_2940": "l10n_ch_account_tags.account_tag_ch_290",
        "ch_coa_2950": "l10n_ch_account_tags.account_tag_ch_290",
        "ch_coa_2960": "l10n_ch_account_tags.account_tag_ch_290",
        "ch_coa_2970": "l10n_ch_account_tags.account_tag_ch_290",
        "ch_coa_2979": "l10n_ch_account_tags.account_tag_ch_297",
        "ch_coa_2980": "l10n_ch_account_tags.account_tag_ch_290",
        "ch_coa_3000": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3009": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3200": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3400": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3600": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3700": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3710": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3800": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3801": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3802": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3803": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3804": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3805": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3806": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3807": "l10n_ch_account_tags.account_tag_ch_30",
        "ch_coa_3900": "l10n_ch_account_tags.account_tag_ch_39",
        "ch_coa_3901": "l10n_ch_account_tags.account_tag_ch_39",
        "ch_coa_3940": "l10n_ch_account_tags.account_tag_ch_39",
        "ch_coa_4000": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4008": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4009": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4070": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4071": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4072": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4080": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4086": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4092": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4200": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4400": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4500": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4510": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4520": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4521": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4530": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4540": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4800": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4801": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4900": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4901": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4903": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_4906": "l10n_ch_account_tags.account_tag_ch_4",
        "ch_coa_5000": "l10n_ch_account_tags.account_tag_ch_5",
        "ch_coa_5700": "l10n_ch_account_tags.account_tag_ch_5",
        "ch_coa_5800": "l10n_ch_account_tags.account_tag_ch_5",
        "ch_coa_5900": "l10n_ch_account_tags.account_tag_ch_5",
        "ch_coa_6000": "l10n_ch_account_tags.account_tag_ch_60",
        "ch_coa_6100": "l10n_ch_account_tags.account_tag_ch_60",
        "ch_coa_6105": "l10n_ch_account_tags.account_tag_ch_60",
        "ch_coa_6200": "l10n_ch_account_tags.account_tag_ch_60",
        "ch_coa_6260": "l10n_ch_account_tags.account_tag_ch_60",
        "ch_coa_6300": "l10n_ch_account_tags.account_tag_ch_60",
        "ch_coa_6400": "l10n_ch_account_tags.account_tag_ch_60",
        "ch_coa_6500": "l10n_ch_account_tags.account_tag_ch_60",
        "ch_coa_6570": "l10n_ch_account_tags.account_tag_ch_60",
        "ch_coa_6600": "l10n_ch_account_tags.account_tag_ch_60",
        "ch_coa_6700": "l10n_ch_account_tags.account_tag_ch_60",
        "ch_coa_6800": "l10n_ch_account_tags.account_tag_ch_68",
        "ch_coa_6900": "l10n_ch_account_tags.account_tag_ch_69",
        "ch_coa_6950": "l10n_ch_account_tags.account_tag_ch_69",
        "ch_coa_7000": "l10n_ch_account_tags.account_tag_ch_7",
        "ch_coa_7010": "l10n_ch_account_tags.account_tag_ch_7",
        "ch_coa_7500": "l10n_ch_account_tags.account_tag_ch_7",
        "ch_coa_7510": "l10n_ch_account_tags.account_tag_ch_7",
        "ch_coa_8000": "l10n_ch_account_tags.account_tag_ch_80",
        "ch_coa_8100": "l10n_ch_account_tags.account_tag_ch_80",
        "ch_coa_8500": "l10n_ch_account_tags.account_tag_ch_85",
        "ch_coa_8510": "l10n_ch_account_tags.account_tag_ch_85",
        "ch_coa_8900": "l10n_ch_account_tags.account_tag_ch_89",
    }

    # Search for companies with chart template 'ch'
    companies = env["res.company"].search([("chart_template", "=", "ch")])

    # Create a dictionary to hold account IDs and their corresponding tags
    account_tag_mapping = {}

    # Loop through the companies and account_tags to group account-tag pairs
    for company in companies:
        for account_code, tag_code in account_tags.items():
            # Construct the xml_id of the account based on company ID and account code
            xml_id = f"account.{company.id}_{account_code}"

            try:
                # Use env.ref() to search for the account by xml_id
                account = env.ref(xml_id)

                # Use env.ref() to search for the tag by tag_code
                tag = env.ref(tag_code)

                if account and tag:
                    # If the account is found, group the tags by account_id
                    if account.id not in account_tag_mapping:
                        account_tag_mapping[account.id] = []

                    account_tag_mapping[account.id].append(tag.id)
                else:
                    if not account:
                        _logger.warning(f"Account with xml_id {xml_id} not found.")
                    if not tag:
                        _logger.warning(f"Tag with code {tag_code} not found.")

            except (ValueError, KeyError, AttributeError) as e:
                _logger.error(
                    f"Error processing account {xml_id} and tag {tag_code}: "
                    f"{str(e)}"
                )

    # Perform bulk updates for each account by adding new tags
    for account_id, tag_ids in account_tag_mapping.items():
        account = env["account.account"].browse(account_id)

        if account:
            # Get the IDs of existing tags assigned to the account
            existing_tags = account.tag_ids.ids

            # Filter out the tags that are already assigned
            new_tags = list(set(tag_ids) - set(existing_tags))

            if new_tags:
                # Add the new tags to the account
                account.tag_ids = [(4, tag_id) for tag_id in new_tags]


def post_init(env):
    assign_account_tags(env)
