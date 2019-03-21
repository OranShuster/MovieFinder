from pytest import mark

from adapters.enums import CityNamesAlternatives, Company
from arguments_utils import parse_city, parse_company


class TestParseArguments:

    @mark.parametrize('city_alternative', [*CityNamesAlternatives])
    def test_parse_city(self, city_alternative):
        expected_city_parsed = city_alternative.value[0]
        city_alternative_names = city_alternative.value[1]
        for city_alternative_name in city_alternative_names:
            city_parsed = parse_city(city_alternative_name)
            assert expected_city_parsed == city_parsed

    @mark.parametrize('company', [*Company])
    def test_parse_company(self, company):
        company_name = company.value
        company_parsed = parse_company(company_name)
        assert company_parsed == company
