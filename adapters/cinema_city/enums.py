from enum import Enum

DATE_URL_FORMAT = "EEE dd/MM/yyyy"
THEATRE_LOCALE = "he_IL"

EVENT_LIST_DATETIME_FORMAT = "%d/%m/%Y %H:%M"
EVENT_LIST_URL = "https://www.cinema-city.co.il/tickets/EventsFlat?TheatreId={theatre_id}&VenueTypeId=0&date={date}"  # noqa


class EventListKeys(Enum):
    Name = "Name"
    Dates = "Dates"
    Date = "Date"


class EventNameTagEndings(Enum):
    English = " אנגלית"
    Hebrew = " עברית"
    EnglishWithHyphen = " - אנגלית"
    HebrewWithHyphen = " - עברית"
    Dubbed = " מדובב"
    DubbedWithHyphen = " - מדובב"
