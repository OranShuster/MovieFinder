from enum import Enum


class ParsedEventListKey(Enum):
    Name = "name"
    Date = "date"
    Location = "location"
    City = "city"


class Company(Enum):
    CinemaCity = "Cinema City"
    YesPlanet = "Yes Planet"


class City(Enum):
    RishonLeZion = "Rishon Le Zion"
    Glilot = "Glilot"
    BeerSheba = "Beer Sheba"


class CityNamesAlternatives(Enum):
    BeerSheba = (
        City.BeerSheba,
        ["beer sheba", "beer-sheba", "beer-sheva", "beer sheva"],
    )
    RishonLeZion = (
        City.RishonLeZion,
        ["rishon le zion", "rishon le tzion", "rishon lezion", "rishon letzion"],
    )
    Glilot = (City.Glilot, ["glilot"])


class EventTags(Enum):
    SubbedHebrew = "Hebrew Subbed"
    Subbed = "Subbed"
    English = "English"
    Hebrew = "Hebrew"
    ScreenX2D = "ScreenX 2D"
    In3D = "3D"
    DubbedHebrew = "Dubbed Hebrew"
