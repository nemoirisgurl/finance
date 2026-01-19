import re

DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD format


def is_valid_date(date):
    if not date or not DATE_REGEX.match(date):
        return False
    date_parts = date.split("-")
    year, month, day = map(int, date_parts)
    if not (1 <= month <= 12):
        return False
    else:
        month_days = [
            31,
            29 if is_leap_year(year) else 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ]
        if not (1 <= day <= month_days[month - 1]):
            return False
    return True


def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
