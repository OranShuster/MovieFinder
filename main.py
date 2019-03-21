from datetime import datetime
from itertools import chain
from typing import List

import click
from tabulate import tabulate

import settings
from adapters.common import query_adapters, Event
from adapters.enums import City, Company
from arguments_utils import parse_city, parse_date, parse_company


@click.group("actions")
def actions():
    pass


@actions.command()
@click.argument("date", type=str, default="today")
@click.option("--city", help="Only show theatres from this city.")
@click.option("--company", help="Only show theatres from this company.")
def show_events(date: str, city: str, company: str):
    date_parsed: datetime = parse_date(date)
    city_parsed: City = parse_city(city)
    company_parsed: Company = parse_company(company)
    adapters_responses = query_adapters(date_parsed,city_parsed,company_parsed, settings.adapters)

    combined_adapters: List[Event] = list(chain(*adapters_responses))
    combined_adapters.sort(key=lambda x: x.date)

    events_table = [event.as_table_row() for event in combined_adapters]
    click.echo(tabulate(events_table, tablefmt="plain", numalign="left", stralign="left"))
    click.echo("")


if __name__ == "__main__":
    actions()
