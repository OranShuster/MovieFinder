from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List

import click
from tzlocal import get_localzone

import settings
from adapters.enums import CompanyNames, CityNames
from adapters.enums import CompanyNames, CityNames, EventTags




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

    def __str__(self):
        return "{} {}".format(self.company, self.city)


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


def query_adapters(event_date) -> List[List]:
    adapters_responses = []
    adapters = settings.adapters
    with click.progressbar(adapters, length=len(adapters)) as adapters_progress:
        adapter: TheatreAdapter
        for adapter in adapters_progress:
            adapter_response = adapter.get_events(event_date=event_date)
            adapters_responses.append(adapter_response)

    return adapters_responses
