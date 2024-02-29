import datetime
import zoneinfo

from kw import find_end_date_for_kw


def test_find_end_date_for_kw():
    week_number = 1
    date = datetime.datetime(2024, 1, 1)
    expected = datetime.datetime(2024, 1, 7, tzinfo=zoneinfo.ZoneInfo("Europe/Berlin"))
    assert find_end_date_for_kw(week_number, date) == expected
