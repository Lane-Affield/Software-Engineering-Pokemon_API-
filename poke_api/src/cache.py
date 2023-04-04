import json
import os


# ----------------------------------------------------
"""
the following code attempts to read the cache, if it exists it opens it, if not it creates the file with an empty discitonary inside
"""


def read_cache():
    try:
        if os.path.exists("poke.cache"):  # checks to see if the path exists
            with open("poke.cache", "r") as cache:
                return json.load(cache)  # returns the cache
        else:
            # NOTE: I got inspiration for the below code from Kali Zerwas
            # EXPLANATION: this code creates a framework for api_wrapper.pi to go off of when there is no cache file
            framework = {
                "Pokedex": {},  # list of pokemon
                "Pokemon": {},  # dictionary of pokemon objects
                "Sprites": {},  # dictionary of sprites
                "Abilities": {},  # dictionary of abilities
                "Moves": {},  # dictionary of moves
                "Move_Filter": {},  # dictionary of move filters
                "Ability_Filter": {},  # dictionaty of ability filters
                "Type_Filter": {},  # dictionary of type filters
            }
            return framework

    except:  # error for when the cache does not load
        print("Error creating cache")


# ----------------------------------------------------
"""
the following code writes the data retrieved from the Poke API into the Cache
"""


def write_cache(poke_data):
    with open("poke.cache", "w") as cache:
        json.dump(poke_data, cache)


# ----------------------------------------------------
