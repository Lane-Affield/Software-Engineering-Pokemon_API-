from flask import Flask
from requests import get
from src.cache import read_cache, write_cache

app = Flask(__name__)
POKE_URI_BASE = "https://pokeapi.co/api/v2/"  # saves URL as variable
# ----------------------------------------------------
# getters
"""
the following retrieves the info from the API and returns it
"""


def poke_getter(pokemon_name):
    return get(
        f"{POKE_URI_BASE}pokemon/{pokemon_name}"
    ).json()  # returns the pokemon name if it exists in the AP


def ability_getter(ability_name):  # tries to get the pokemon ability
    return get(
        f"{POKE_URI_BASE}ability/{ability_name}"
    ).json()  # retrives the ability if it is in the API


def move_getter(move_name):
    return get(
        f"{POKE_URI_BASE}move/{move_name}"
    ).json()  # retrieves the move if in the API


def type_getter(type_name):
    return get(
        f"{POKE_URI_BASE}type/{type_name}"
    ).json()  # retrieves the move if in the API


def all_pokemon_getter():  # returns all pokemon
    return get(
        "https://pokeapi.co/api/v2/pokemon"
    )  # takes the entire list of pokemon, make sure the limit is this size


# ----------------------------------------------------
#
"""
The Following code should return a list of all the pokemon in the API (contains name and the URL)

NOTE: I got inspiration for this from Kali Zerwas
"""


@app.route("/pokemon?limit=100000")  # ensures all pokemon are returned in the API
def get_all_pokemon():
    CACHE = read_cache()

    if (
        len(CACHE["Pokedex"]) == 0
    ):  # checks to see if the list already exists in the cache
        pokedex = []  # list of pokemon, the "pokedex"
        catch_em_all = (
            all_pokemon_getter()
        )  # variable that contains all of the pokemons data
        pokedex_info = catch_em_all.json()[
            "results"
        ]  # returns the results from the pokedex
        for caught_pokemon in pokedex_info:
            pokedex.append(
                {"Name": caught_pokemon["name"], "URL": caught_pokemon["url"]}
            )  # appends to the pokedex list
            CACHE["Pokedex"] = pokedex
            write_cache(CACHE)

        return CACHE["Pokedex"]
    else:
        return CACHE["Pokedex"]


"""
The Code Below is for retrieving pokemon by name OR by id, it returns the whole pokemon object
"""


@app.route("/pokemon/<pokemon_name>")
def get_pokemon_by_name(pokemon_name):
    if pokemon_name == str(pokemon_name):
        pokemon_name = (
            pokemon_name.lower()
        )  # makes sure that there are no caps from the user, otherwise will throw off the program
    CACHE = read_cache()
    if pokemon_name in CACHE["Pokemon"]:  # checks to see if name is in cache
        print(
            f"found {pokemon_name} in the cache!"
        )  # tells user that the pokemon was found in the cache
        return CACHE["Pokemon"][pokemon_name]
    else:
        print(f"Retrieving {pokemon_name} from the PokeAPI")
        CACHE["Pokemon"][pokemon_name] = poke_getter(
            pokemon_name
        )  # retrieves the pokemon from the API
        write_cache(CACHE)  # puts pokemon in the Cache with the write function
        return CACHE["Pokemon"][pokemon_name]


"""
the following code should retrieve an ability object from the cache or API
"""


@app.route("/ability/<ability_name>")
def get_ability_by_name(ability_name):
    ability_name = (
        ability_name.lower()
    )  # makes sure that there are no caps from the user, otherwise will throw off the program
    CACHE = read_cache()
    if ability_name in CACHE["Abilities"]:  # checks to see if name is in cache
        return CACHE["Abilities"][ability_name]
    else:
        CACHE["Abilities"][ability_name] = ability_getter(
            ability_name
        )  # retrieves the pokemon from the API
        write_cache(CACHE)  # puts pokemon in the Cache with the write function
        return CACHE["Abilities"][ability_name]


"""
the following code should retrieve a move object form the cache or API
"""


@app.route("/move/<move_name>")
def get_move_by_name(move_name):
    move_name = (
        move_name.lower()
    )  # makes sure that there are no caps from the user, otherwise will throw off the program
    CACHE = read_cache()
    if move_name in CACHE["Moves"]:  # checks to see if name is in cache
        return CACHE["Moves"][move_name]
    else:
        CACHE["Moves"][move_name] = move_getter(
            move_name
        )  # retrieves the pokemon from the API
        write_cache(CACHE)  # puts pokemon in the Cache with the write function
        return CACHE["Moves"][move_name]


"""
the following code should retrieve a sprite from the cache or API
"""


@app.route("/pokemon/<pokemon_name>/sprites")
def get_sprite(pokemon_name):
    CACHE = read_cache()
    sprite = []  # empty list of sprites
    pokemon_name = pokemon_name.lower()
    if pokemon_name in CACHE["Sprites"]:  # if already in the sprite cache
        return CACHE["Sprites"][pokemon_name]
    elif pokemon_name in CACHE["Pokemon"]:  # if in the cache but not under the sprites
        found_in_cache = CACHE["Pokemon"][pokemon_name]
        CACHE["Sprites"][pokemon_name] = found_in_cache["sprites"]
        write_cache(CACHE)
        return CACHE["Sprites"][pokemon_name]
    else:  # retrieve from the API
        api_pokemon = poke_getter(pokemon_name)
        CACHE["Sprites"][pokemon_name] = api_pokemon["sprites"]
        write_cache(CACHE)
        return CACHE["Sprites"][pokemon_name]


"""
gets pokemon by id
"""


@app.route("/pokemon/<pokemon_id>")
def get_pokemon_by_id(pokemon_id):
    CACHE = read_cache()
    if pokemon_id in CACHE["Pokemon"]:  # checks to see if name is in cache
        return CACHE["Pokemon"][pokemon_id]
    else:
        retrieved_pokemon = poke_getter(pokemon_id)
        CACHE["Pokemon"][
            pokemon_id
        ] = retrieved_pokemon  # retrieves the pokemon from the API
        write_cache(CACHE)  # puts pokemon in the Cache with the write function
        return retrieved_pokemon


# ----------------------------------------------------
# Filters for the pokemon
"""
THe code below should return a list of pokemon with the ability searched
"""


@app.route("/pokemon?ability=<ability_name>")
def filter_ability(ability_name):
    CACHE = read_cache()
    ability_name = ability_name.lower()
    if ability_name in CACHE["Ability_Filter"]:
        return CACHE["Ability_Filter"][ability_name]
    elif (
        ability_name in CACHE["Abilities"]
    ):  # this may be in the cache already, just not saved in the ability filter section
        ability_in_cache = CACHE["Abilities"][ability_name]
        CACHE["Ability_Filter"][ability_name] = ability_in_cache["pokemon"]
        write_cache(CACHE)
        return CACHE["Ability_Filter"][ability_name]
    else:
        ability_in_API = ability_getter(ability_name)
        CACHE["Ability_Filter"][ability_name] = ability_in_API["pokemon"]
        write_cache(CACHE)
        return CACHE["Ability_Filter"][ability_name]


"""
returns a list of pokemon that can learn a specific move
"""


@app.route("/pokemon?move=<move_name>")
def filter_move(move_name):
    CACHE = read_cache()
    move_name = move_name.lower()
    if move_name in CACHE["Move_Filter"]:
        return CACHE["Move_Filter"][move_name]
    elif move_name in CACHE["Moves"]:
        move_in_cache = CACHE["Moves"][move_name]
        CACHE["Move_Filter"][move_name] = move_in_cache["learned_by_pokemon"]
        write_cache(CACHE)
        return CACHE["Move_Filter"][move_name]
    else:
        move_in_API = move_getter(move_name)
        CACHE["Move_Filter"][move_name] = move_in_API["learned_by_pokemon"]
        write_cache(CACHE)
        return CACHE["Move_Filter"][move_name]


"""
returns a list of pokemon that are a given type
"""


@app.route("/pokemon?type=<type_name>")
def filter_type(type_name):
    CACHE = read_cache()
    type_name = type_name.lower()
    if type_name in CACHE["Type_Filter"]:
        return CACHE["Type_Filter"][type_name]
    else:
        type_in_API = type_getter(type_name)
        CACHE["Type_Filter"][type_name] = type_in_API["pokemon"]
        write_cache(CACHE)
        return CACHE["Type_Filter"][type_name]
