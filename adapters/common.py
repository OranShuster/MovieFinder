from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List

import click
from tzlocal import get_localzone

from adapters.consts import UNICODE_HEBREW_RANGE_START, UNICODE_HEBREW_RANGE_END
from adapters.enums import CompanyNames, CityNames, EventTags


def is_hebrew(s: str) -> bool:
    for char in s:
        if UNICODE_HEBREW_RANGE_START <= ord(char) <= UNICODE_HEBREW_RANGE_END:
            return True
    return False


class Event(object):
    def __init__(
        self,
        name: str,
        date: datetime,
        city: CityNames,
        company: CompanyNames,
        tags: List[EventTags],
    ):
        self.name = name
        self.date = date
        self.city = city
        self.company = company
        self.tags = tags

    @property
    def tags_str(self):
        return " ".join([click.style(tag, bg="red", bold=True) for tag in self.tags])

    @property
    def name_aligned(self):
        # Add unicode RTL modifier for hebrew text
        if is_hebrew(self.name):
            return "\u200E{name}".format(name=self.name)
        else:
            return self.name

    def as_table_row(self):
        return [self.date, self.name_aligned, self.tags_str, self.company, self.city]

    def __str__(self):
        return "* {date} - {name} - {tags} - {company} {city}".format(
            date=self.date,
            name=self.name_aligned,
            tags=self.tags_str,
            company=self.company,
            city=self.city,
        )


class TheatreAdapter(metaclass=ABCMeta):
    def __init__(self, theatre_id: int, display_name: str, city: str, company: str):
        self.theatre_id = theatre_id
        self.display_name = display_name
        self.city = city
        self.company = company

    def validate_event_date(self, event_date: datetime):
        if event_date < today():
            raise AssertionError("Given date {} is in the past".format(event_date))

    @abstractmethod
    def _get_event_list(self, event_date: datetime) -> list:
        pass

    @abstractmethod
    def _parse_event_list(self, event_list: list) -> list:
        pass

    @abstractmethod
    def get_events(self, event_date: datetime) -> list:
        pass

    @abstractmethod
    def _parse_event_tags(self, *args, **kwargs):
        pass


def today():
    return datetime.now(tz=get_localzone()).replace(
        hour=0, minute=0, second=0, microsecond=0
    )


def query_adapters(event_date: datetime, adapters: list) -> List[List]:
    adapters_responses = []
    with click.progressbar(adapters, length=len(adapters)) as adapters_progress:
        adapter: TheatreAdapter
        for adapter in adapters_progress:
            adapter_response = adapter.get_events(event_date=event_date)
            adapters_responses.append(adapter_response)

    return adapters_responses
