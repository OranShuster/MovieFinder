from datetime import timedelta
from typing import List, Optional

import click

from adapters.common import today, Event
from adapters.enums import City, CityNamesAlternatives, Company


def parse_city(city: str) -> City:
    city_parsed: City = None
    for city_name_alt_enum in CityNamesAlternatives:
        city_name_alt_enum_value = city_name_alt_enum.value
        city_name_enum = city_name_alt_enum_value[0]
        city_name_alts_str_list = city_name_alt_enum_value[1]
        if city in city_name_alts_str_list:
            city_parsed = city_name_enum
            break
    return city_parsed


def parse_company(company):
    company_parsed: Company = None
    for company_enum in Company:
        company_value = company_enum.value
        if company_value == company:
            company_parsed = company_enum
            break
    return company_parsed


def parse_date(date):
    try:
        date_int = int(date)

        if date_int < 0:
            click.echo("Numerical date should be a positive number or 0")
            raise AssertionError("Numerical date is invalid")

        # This is a day delta type of input
        date_parsed = today() + timedelta(days=date_int)

    except (ValueError, TypeError):
        # Check if the argument is any of the special date strings
        date = date.lower()
        if date == "today":
            date_parsed = today()

        elif date == "tomorrow":
            date_parsed = today() + timedelta(days=1)

        else:
            raise AssertionError("Date given could not be parsed")
    return date_parsed