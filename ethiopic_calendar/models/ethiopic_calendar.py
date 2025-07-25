# Copyright (C) 2022 Trevi Software (https://trevi.et)
# Copyright (C) 2013 Michael Telahun Makonnen <mmakonnen@gmail.com>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime

from dateutil.relativedelta import relativedelta

from odoo import _

from .pycalcal import pycalcal as pcc

ET_MONTHS_AM = [
    "",
    "መስከረም",
    "ጥቅምት",
    "ህዳር",
    "ታህሳስ",
    "ጥር",
    "የካቲት",
    "መጋቢት",
    "ሚያዝያ",
    "ግንቦት",
    "ሰኔ",
    "ሃምሌ",
    "ነሐሴ",
    "ጳጉሜ",
]

ET_MONTHS_EN = [
    "",
    "Meskerem",
    "Tikimt",
    "Hedar",
    "Tahsas",
    "Tir",
    "Yekatit",
    "Megabit",
    "Miazia",
    "Genbot",
    "Senie",
    "Hamle",
    "Nehassie",
    "Pagume",
]

ET_MONTHS_SELECTION_AM = [
    ("1", "መስከረም"),
    ("2", "ጥቅምት"),
    ("3", "ህዳር"),
    ("4", "ታህሳስ"),
    ("5", "ጥር"),
    ("6", "የካቲት"),
    ("7", "መጋቢት"),
    ("8", "ሚያዝያ"),
    ("9", "ግንቦት"),
    ("10", "ሰኔ"),
    ("11", "ሃምሌ"),
    ("12", "ነሐሴ"),
    ("13", "ጳጉሜ"),
]

ET_MONTHS_SELECTION = [
    ("1", _("Meskerem")),
    ("2", _("Tikimt")),
    ("3", _("Hedar")),
    ("4", _("Tahsas")),
    ("5", _("Tir")),
    ("6", _("Yekatit")),
    ("7", _("Megabit")),
    ("8", _("Miazia")),
    ("9", _("Genbot")),
    ("10", _("Senie")),
    ("11", _("Hamle")),
    ("12", _("Nehassie")),
    ("13", _("Pagume")),
]

ET_DAYOFMONTH_SELECTION = [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
    ("13", "13"),
    ("14", "14"),
    ("15", "15"),
    ("16", "16"),
    ("17", "17"),
    ("18", "18"),
    ("19", "19"),
    ("20", "20"),
    ("21", "21"),
    ("22", "22"),
    ("23", "23"),
    ("24", "24"),
    ("25", "25"),
    ("26", "26"),
    ("27", "27"),
    ("28", "28"),
    ("29", "29"),
    ("30", "30"),
]


# Returns an array(et_year, et_month, et_day)
ethiopic_date = pcc.ethiopic_date


def get_etyear_selection(start_delta=-20, end_delta=100):

    res = []

    # Assume a period within the last 20 years and the next 100
    year = datetime.now().year
    year += start_delta

    # Convert to Ethiopic calendar
    pccDate = pcc.ethiopic_from_fixed(
        pcc.fixed_from_gregorian(pcc.gregorian_date(year, 1, 1))
    )
    year = pccDate[0]

    i = year
    while i < (year + end_delta):
        res.append((str(i), str(i)))
        i += 1

    return res


def ethiopic_date_str(et_date):
    """Returns an ethiopic_date as a string (Y-m-d)"""

    return str(et_date[0]) + "-%02d" % (et_date[1]) + "-%02d" % (et_date[2])


def date_gregorian_from_ethiopic_base(y, m, d):
    """Returns the gregorian date as a datetime.date object"""

    assert y and m and d, "Ethiopic year, month and day must not be false"
    pccDate = pcc.gregorian_from_fixed(
        pcc.fixed_from_ethiopic(pcc.ethiopic_date(int(y), int(m), int(d)))
    )
    res = date(pccDate[0], pccDate[1], pccDate[2])
    return res


def date_gregorian_from_ethiopic(et_date):
    """Returns the gregorian date of an ethiopic_date object as
    a datetime.date object"""

    return date_gregorian_from_ethiopic_base(et_date[0], et_date[1], et_date[2])


def ethiopic_from_gregorian_date(d):
    """Returns an ethiopic_date object from a gregorian datetime.date
    object"""

    pccDate = pcc.ethiopic_from_fixed(
        pcc.fixed_from_gregorian(
            pcc.gregorian_date(int(d.year), int(d.month), int(d.day))
        )
    )
    return pccDate


def str_ethiopic_from_gregorian_date(d):
    """Returns an ethiopic date string (Y-m-d) from a gregorian datetime.date
    object"""

    pccDate = ethiopic_from_gregorian_date(d)
    return ethiopic_date_str(pccDate)


def ethiopic_month_end(et_date):
    """Returns the end of the the month represented by ethiopic_date
    object et_date as an ethiopic_date object"""

    et_end = et_date
    if et_date[1] >= 1 and et_date[1] < 13:
        et_end[2] = 30
    elif et_date[1] == 13:
        if pcc.is_coptic_leap_year(et_date[0]):
            et_end[2] = 6
        else:
            et_end[2] = 5
    else:
        et_end = False
    return et_end


def ethiopic_next_day(et_date):
    """Returns an ethiopic_date object representing the day after et_date"""

    d = date_gregorian_from_ethiopic(et_date)
    d += relativedelta(days=1)
    return ethiopic_from_gregorian_date(d)


def ethiopic_prev_day(et_date):
    """Returns an ethiopic_date object representing the day before et_date"""

    d = date_gregorian_from_ethiopic(et_date)
    d += relativedelta(days=-1)
    return ethiopic_from_gregorian_date(d)
