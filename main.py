from datetime import datetime
from datetime import timedelta
from itertools import chain

import click

import settings
from adapters.common import query_adapters, Event


@click.group("actions")
def actions():
    pass


@actions.command()
@click.argument("date", type=str, default="today")
@click.option("--city", help="Only show theatres from this city.")
@click.option("--company", help="Only show theatres from this company.")
def show_events(date: str, city, company):
    try:
        date_int = int(date)

        if date_int < 0:
            click.echo("Numerical date should be a positive number or 0")
            raise AssertionError("Numerical date is invalid")

        # This is a day delta type of input
        date_parsed = datetime.now() + timedelta(days=date_int)

    except (ValueError, TypeError):
        # Check if the argument is any of the special date strings
        date = date.lower()
        if date == "today":
            date_parsed = datetime.now()

        elif date == "tomorrow":
            date_parsed = datetime.now() + timedelta(days=1)

        else:
            raise AssertionError("Date given could not be parsed")

    adapters_responses = query_adapters(date_parsed)
    combined_adapters: list = list(chain(*adapters_responses))
    combined_adapters.sort(key=lambda x: x.date)
    event: Event
    for event in combined_adapters:
        event_str = "* {date} - \u200E{name} - {location}".format(
            name=event.name, date=event.date, location=event
        )
        click.echo(event_str)
    click.echo("")


if __name__ == "__main__":
    actions()
