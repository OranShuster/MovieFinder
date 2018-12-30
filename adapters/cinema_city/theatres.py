import logging
from datetime import datetime

import requests
from babel.dates import format_datetime

from adapters.cinema_city import enums
from adapters.common import TheatreAdapter, Event
from adapters.enums import CompanyNames, CityNames

logger = logging.getLogger("CinemaCityTheatre")


class CinemaCityTheatre(TheatreAdapter):
    def _get_event_list(self, event_date: datetime):
        today_babel = format_datetime(
            event_date, format=enums.DATE_URL_FORMAT, locale=enums.THEATRE_LOCALE
        )
        url = enums.EVENT_LIST_URL.format(theatre_id=self.theatre_id, date=today_babel)
        logger.debug("Get event list from server using url - {}".format(url))
        response = requests.get(url)
        return response.json()

    def _parse_event_list(self, event_list_from_server: list):
        parsed_event_list = []
        for event in event_list_from_server:
            event_datetime = datetime.strptime(
                event[enums.EventListKeys.Dates][enums.EventListKeys.Date],
                enums.EVENT_LIST_DATETIME_FORMAT,
            )
            new_event = Event(
                name=event[enums.EventListKeys.Name],
                date=event_datetime,
                city=self.city,
                company=self.company,
                tags=[],
            )
            parsed_event_list.append(new_event)

        return parsed_event_list

    def get_events(self, event_date):
        if event_date < datetime.now().replace(hour=0, minute=0, second=0):
            raise AssertionError("Given date {} is in the past".format(event_date))

        event_list_from_server = self._get_event_list(event_date)
        parsed_event_list = self._parse_event_list(event_list_from_server)
        return parsed_event_list


class CinemaCityRishonLeZion(CinemaCityTheatre):
    THEATRE_ID = 1173

    def __init__(self):
        super(CinemaCityRishonLeZion, self).__init__(
            display_name="Cinema City Rishon LeZion",
            theatre_id=self.THEATRE_ID,
            company=CompanyNames.CinemaCity,
            city=CityNames.RishonLeZion,
        )
