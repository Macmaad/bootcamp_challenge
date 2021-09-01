import pytest
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

from app import app


@pytest.fixture
def client():
    client = app.app.test_client()

    yield client


class TestPokedex:
    def test_get_pokemon_data(self, client):
        expected_result = {
            "result": {
                "pokemon_language": "While it is young, it uses the nutrients that are\nstored in the seed on its back in order to grow.",
                "pokemon_name": "bulbasaur",
            },
            "status_code": 200,
        }
        result = client.get("/pokedex/1")

        assert expected_result == result.json

    def test_bad_request(self, client):
        expected_result = {"result": "Bad Request", "status_code": 400}
        result = client.get("/pokedex/0")

        assert expected_result == result.json

    def test_get_pokemon_language(self):
        expected_result = "Exposure to sunlight adds to its strength.\nSunlight also makes the bud on its back\ngrow larger."
        result = app.get_pokemon_language(
            "https://pokeapi.co/api/v2/pokemon-species/2/"
        )

        assert expected_result == result

    def test_empty_pokemon_language(self):
        expected_result = ""
        result = app.get_pokemon_language(
            "https://pokeapi.co/api/v2/pokemon-species/12321/"
        )

        assert expected_result == result

    def test_search_pokemon(self):
        data = [
            {
                "entry_number": 1,
                "pokemon_species": {
                    "name": "bulbasaur",
                    "url": "https://pokeapi.co/api/v2/pokemon-species/1/",
                },
            },
            {
                "entry_number": 2,
                "pokemon_species": {
                    "name": "ivysaur",
                    "url": "https://pokeapi.co/api/v2/pokemon-species/2/",
                },
            },
            {
                "entry_number": 3,
                "pokemon_species": {
                    "name": "venusaur",
                    "url": "https://pokeapi.co/api/v2/pokemon-species/3/",
                },
            },
            {
                "entry_number": 4,
                "pokemon_species": {
                    "name": "charmander",
                    "url": "https://pokeapi.co/api/v2/pokemon-species/4/",
                },
            },
        ]
        result = app.search_pokemon(data, 1)
        expected_result = {
            "entry_number": 1,
            "pokemon_species": {
                "name": "bulbasaur",
                "url": "https://pokeapi.co/api/v2/pokemon-species/1/",
            },
        }

        assert expected_result == result

    def test_empty_search_pokemon(self):
        result = app.search_pokemon([], 1)
        expected_result = {}

        assert expected_result == result
