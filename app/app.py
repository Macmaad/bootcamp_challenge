import http

import requests
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return "Hello World!"


def make_poke_api_request(url):
    data = None
    result = requests.get(url)

    if result.status_code == http.HTTPStatus.OK:
        data = result.json()

    return data


def search_pokemon(pokemons_data, pokemon_id):
    pokemon_data = {}

    for pokemon in pokemons_data:
        if pokemon["entry_number"] == pokemon_id:
            pokemon_data = pokemon
            break

    return pokemon_data


def get_pokemon_language(pokemon_species_url):
    text, flavour_text_entries = "", {}
    species_data = make_poke_api_request(pokemon_species_url)

    if species_data:
        flavour_text_entries = species_data["flavor_text_entries"]

    for flavour_text in flavour_text_entries:
        if flavour_text["language"]["name"] == "en":
            text = flavour_text["flavor_text"]

    return text


@app.route("/pokedex/<int:pokemon_id>", methods=["GET"])
def pokedex(pokemon_id=1):
    """
    Using the Kanto pokedex, this endpoint return the name of the pokemon with the messages that
    explains some information about it.

    :param pokemon_id: Int number from 1 to 150 to retrieve the data of the pokemon.
    :return: Json data with 2 keys, status, and result. If the endpoint is executed correctly
    the result key will have the name and the language of the pokemon.
    """
    request_result = {
        "result": "Bad Request",
        "status_code": http.HTTPStatus.BAD_REQUEST,
    }
    if 0 < pokemon_id <= 150:
        pokedex_data = make_poke_api_request("https://pokeapi.co/api/v2/pokedex/2")

        if pokedex_data:
            pokemon = search_pokemon(pokedex_data["pokemon_entries"], pokemon_id)
            if pokemon:
                pokemon = pokemon["pokemon_species"]
                name = pokemon["name"]
                pokemon_language = get_pokemon_language(pokemon["url"])
                request_result = {
                    "result": {
                        "pokemon_name": name,
                        "pokemon_language": pokemon_language,
                    },
                    "status_code": http.HTTPStatus.OK,
                }

            else:
                request_result = {
                    "result": "Not found",
                    "status_code": http.HTTPStatus.NOT_FOUND,
                }

        else:
            request_result = {
                "result": "Could not retrieve data",
                "status_code": http.HTTPStatus.INTERNAL_SERVER_ERROR,
            }

    return jsonify(request_result)


if __name__ == "__main__":
    app.run(debug=True)
