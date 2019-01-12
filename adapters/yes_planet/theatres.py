from adapters.enums import CityNames, CompanyNames
from adapters.yes_planet.lib import YesPlanetTheatre


class YesPlanetRishonLeZion(YesPlanetTheatre):
    THEATRE_ID = 1072

    def __init__(self):
        super(YesPlanetRishonLeZion, self).__init__(
            theatre_id=self.THEATRE_ID,
            display_name="Yes Planet Rishon Le Zion",
            city=CityNames.RishonLeZion,
            company=CompanyNames.YesPlanet,
        )


class YesPlanetBeerSheba(YesPlanetTheatre):
    THEATRE_ID = 1074

    def __init__(self):
        super(YesPlanetBeerSheba, self).__init__(
            theatre_id=self.THEATRE_ID,
            display_name="Yes Planet Beer Sheba",
            city=CityNames.BeerSheba,
            company=CompanyNames.YesPlanet,
        )
