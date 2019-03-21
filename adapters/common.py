import logging
from abc import ABCMeta, abstractmethod
from datetime import datetime
from time import time
from typing import List

import click
import tmdbsimple as tmdb
from tzlocal import get_localzone

from adapters.consts import UNICODE_HEBREW_RANGE_START, UNICODE_HEBREW_RANGE_END
from adapters.enums import Company, City, EventTags


logger = logging.getLogger(__name__)


def is_hebrew(s: str) -> bool:
    for char in s:
        if UNICODE_HEBREW_RANGE_START <= ord(char) <= UNICODE_HEBREW_RANGE_END:
            return True
    return False


def _handle_event_name(name: str) -> str:
    name_english = name
    if is_hebrew(name):
        start_time = time()
        search = tmdb.Search()
        response = search.movie(query=f'"{name}"', language="he")
        logger.debug(f"Time it took to translate {name} was {time() - start_time}")
        if len(response['results']) > 0:
            first_result = response['results'][0]
            if first_result['title'] == name:
                name_english = first_result['original_title']
    else:
        name_english = name
    return name_english


class Event(object):
    def __init__(
            self,
            name: str,
            date: datetime,
            city: City,
            company: Company,
            tags: List[EventTags],
    ):
        self.name = _handle_event_name(name)
        self.date = date
        self.city = city
        self.company = company
        self.tags = tags

    @property
    def tags_str(self):
        return " | ".join([click.style(tag.value, bg="red", bold=True) for tag in self.tags])

    @property
    def name_aligned(self):
        # Add unicode RTL modifier for hebrew text
        if is_hebrew(self.name):
            return "\u200E{name}".format(name=self.name)
        else:
            return self.name

    def as_table_row(self):
        return [self.date, self.name_aligned, self.tags_str, self.company.value, self.city.value]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "* {date} - {name} - {tags} - {company} {city}".format(
            date=self.date,
            name=self.name_aligned,
            tags=self.tags_str,
            company=self.company.value,
            city=self.city.value,
        )


class TheatreAdapter(metaclass=ABCMeta):
    def __init__(self, theatre_id: int, display_name: str, city: City, company: Company):
        self.theatre_id = theatre_id
        self.display_name = display_name
        self.city = city
        self.company = company

    @staticmethod
    def validate_event_date(event_date: datetime):
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


def query_adapters(event_date: datetime, city: City, company: Company, adapters: list) -> List[List]:
    adapters_responses = []
    with click.progressbar(adapters, length=len(adapters)) as adapters_progress:
        adapter: TheatreAdapter
        for adapter in adapters_progress:
            if city is not None and adapter.city != city:
                continue

            if company is not None and adapter.company != company:
                continue

            adapter_response = adapter.get_events(event_date=event_date)
            adapters_responses.append(adapter_response)

    return adapters_responses
