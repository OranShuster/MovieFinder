from adapters.enums import City, Company
from adapters.yes_planet.lib import YesPlanetTheatre


class YesPlanetRishonLeZion(YesPlanetTheatre):
    THEATRE_ID = 1072

    def __init__(self):
        super(YesPlanetRishonLeZion, self).__init__(
            theatre_id=self.THEATRE_ID,
            display_name="Yes Planet Rishon Le Zion",
            city=City.RishonLeZion,
            company=Company.YesPlanet,
        )


class YesPlanetBeerSheba(YesPlanetTheatre):
    THEATRE_ID = 1074

    def __init__(self):
        super(YesPlanetBeerSheba, self).__init__(
            theatre_id=self.THEATRE_ID,
            display_name="Yes Planet Beer Sheba",
            city=City.BeerSheba,
            company=Company.YesPlanet,
        )
