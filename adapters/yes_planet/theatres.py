from datetime import datetime
from typing import List

import requests

from adapters.yes_planet import enums
from adapters.common import TheatreAdapter, today, Event
from adapters.enums import CityNames, CompanyNames


class YesPlanetTheatre(TheatreAdapter):
    def _get_event_list(self, event_date: datetime) -> dict:
        url = enums.EVENT_LIST_URL.format(
            theatre_id=self.theatre_id, date=event_date.strftime(enums.DATE_URL_FORMAT)
        )
        response = requests.get(url=url)
        event_list_from_server = response.json()[enums.EventListKeys.Body]
        return event_list_from_server

    def _parse_event_list(self, event_list: dict) -> List[Event]:
        films_list = event_list[enums.EventListKeys.Films]
        event_ids_to_names = {}
        for film in films_list:
            event_ids_to_names[film[enums.EventListKeys.Id]] = film[
                enums.EventListKeys.Name
            ]
        parsed_event_list = []

        _event_list = event_list[enums.EventListKeys.Events]
        for event in _event_list:
            event_name = event_ids_to_names[event[enums.EventListKeys.FilmId]]
            event_datetime = datetime.strptime(
                event[enums.EventListKeys.EventDateTime], enums.EVENT_DATETIME_FORMAT
            )
            new_event = Event(
                name=event_name,
                date=event_datetime,
                city=self.city,
                company=self.company,
                tags=[],
            )
            parsed_event_list.append(new_event)

        return parsed_event_list

    def get_events(self, event_date: datetime):
        self.validate_event_date(event_date=event_date)
        event_list_from_server = self._get_event_list(event_date=event_date)
        parsed_event_list = self._parse_event_list(event_list=event_list_from_server)
        return parsed_event_list


class YesPlanetRishonLeZion(YesPlanetTheatre):
    def __init__(self):
        super(YesPlanetRishonLeZion, self).__init__(
            theatre_id=1072,
            display_name="Yes Planet Rishon Le Zion",
            city=CityNames.RishonLeZion,
            company=CompanyNames.YesPlanet,
        )
