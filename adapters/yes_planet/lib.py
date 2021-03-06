from datetime import datetime
from typing import List

import requests

from adapters.common import Event, TheatreAdapter
from adapters.enums import EventTags
from adapters.yes_planet import enums


class YesPlanetTheatre(TheatreAdapter):
    def _parse_event_tags(self, event_attributes: List[str]):
        _event_attributes = set(event_attributes)
        event_tags: List[EventTags] = []

        for event_attributes_sets in enums.EventAttributeSets:
            attribute_set = event_attributes_sets.value[0]
            event_tag = event_attributes_sets.value[1]
            if _event_attributes.issuperset(attribute_set):
                event_tags.append(event_tag)
                _event_attributes = _event_attributes.difference(attribute_set)
        return event_tags

    def _get_event_list(self, event_date: datetime) -> dict:
        url = enums.EVENT_LIST_URL.format(
            theatre_id=self.theatre_id, date=event_date.strftime(enums.DATE_URL_FORMAT)
        )
        response = requests.get(url=url)
        event_list_from_server = response.json()[enums.EventListKeys.Body]
        return event_list_from_server

    def _parse_event_list(self, event_list: dict) -> List[Event]:
        parsed_event_list = []

        films_list = event_list[enums.EventListKeys.Films]
        event_ids_to_names = {}
        for film in films_list:
            event_ids_to_names[film[enums.EventListKeys.Id]] = film[
                enums.EventListKeys.Name
            ]

        _event_list = event_list[enums.EventListKeys.Events]
        for event in _event_list:
            event_name = event_ids_to_names[event[enums.EventListKeys.FilmId]]
            event_datetime = datetime.strptime(
                event[enums.EventListKeys.EventDateTime], enums.EVENT_DATETIME_FORMAT
            )
            tags = self._parse_event_tags(event[enums.EventListKeys.Attributes])
            new_event = Event(
                name=event_name,
                date=event_datetime,
                city=self.city,
                company=self.company,
                tags=tags,
            )
            parsed_event_list.append(new_event)

        return parsed_event_list

    def get_events(self, event_date: datetime):
        self.validate_event_date(event_date=event_date)
        event_list_from_server = self._get_event_list(event_date=event_date)
        parsed_event_list = self._parse_event_list(event_list=event_list_from_server)
        return parsed_event_list
