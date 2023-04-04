from requests import get
import requests
import os
import json

from PIL import Image
from io import BytesIO
from rich import print
from termcolor import colored
import cv2
import asciichartpy

ascii_char = [" ", "#", "S", "%", "?", "*", "+", ";", ":", ","]
fav = []


def search():
    pokemon_u = input("Please enter the name of the pokemeon you want to look up: ")
    pokemon = pokemon_u.lower()
    poke_data = get(f"http://127.0.0.1:5000/pokemon/{pokemon}").json()
    poke_info1(poke_data)


# I looked at Kali Zerwas' code to figure this out
def sprite(poke_data):
    sprite_url = poke_data["sprites"]["front_default"]
    response = requests.get(sprite_url)
    response_data = response.content
    image = Image.open(BytesIO(response_data))
    image.save("pokemon.png")
    image = cv2.imread("pokemon.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
    )
    resized = cv2.resize(thresh, (100, 100))
    ascii_chars = [
        " ",
        ".",
        ":",
        "o",
        "&",
        "8",
        "#",
        "@",
        "-",
        "/",
        "\\",
        "+",
        "$",
        "^",
        "~",
        "%",
        "=",
    ]
    ascii_img_data = [[ascii_chars[pixel // 32] for pixel in row] for row in resized]
    for row in ascii_img_data:
        print("".join(row))


def poke_info1(poke_data):
    sprite(poke_data)

    name = poke_data["name"]

    type_data = poke_data["types"]
    type_list = []
    for d in type_data:
        type_names = d["type"]["name"]
        type_list.append(type_names)
    print(f"Pokemon Name: {name}/n Types: ", type_list)
    menu(poke_data, name)


def poke_info2(poke_data, name):
    ability_list = poke_data["abilities"]
    ability_names = []
    for ability in ability_list:
        ability_names.append(ability["ability"]["name"])
    print(f"Abilities of {name} : \n")
    print(ability_names)
    stats = poke_data["stats"]
    stats_str = json.dumps(stats)
    print(f"{name}'s stats: \n")
    print(stats_str)
    menu(poke_data, name)


def poke_info3(poke_data, name):
    move_list = poke_data["moves"]

    move_names = []
    for moves in move_list:
        move_names.append(moves["move"]["name"])

    print(f"{name}'s moves: \n")
    print(move_names)
    menu(poke_data, name)


def favs(fav, name, poke_data):
    if name not in fav:
        fav.append(name)
        print(f"{name} Added to favortie list! \n below is the new favorites list: ")
        print(fav)
    else:
        print(f"{name} is already in the the favorite list")

    menu(poke_data, name)


def menu(poke_data, name):
    response = input(
        "Press a Button: \nS: Ability and stats \nM: Moves \nN: look up new pokemon \nB: name, type, and sprites \nH: home page \nF: add to favorites \nQ: quit program \n Type Response: "
    ).lower()
    if response == "s":
        poke_info2(poke_data, name)
    elif response == "m":
        poke_info3(poke_data, name)
    elif response == "n":
        search()
    elif response == "f":
        favs(fav, name, poke_data)
    elif response == "q":
        exit()
    elif response == "h":
        home_page()

    elif response == "b":
        poke_info1(poke_data)
    else:
        print("error, cannot use this button")


def filter_func(url, filter_list, x):
    lp = True
    while lp == True:
        print("Search by type, ability , or move")
        resp = input()
        if resp in filter_list:
            print("this has already been, filtered")
            second_chance = input("Filter again (Y/N)? ").lower
            if second_chance == "y":
                lp = True
            else:
                home_page()
        else:
            filter_list.append(resp)
            new_filter(url, x, filter_list, resp)


def new_filter(url, y, f_list, filt):
    type_name = input("What type do you want to filter by? ")
    if y == 0:
        url = url + f"?{filt}={type_name}"
    else:
        url = url + f"&{filt}={type_name}"
    poke_data = get(url).json()
    print(poke_data)
    x = True
    while x == True:
        dec5 = input("would like like to filter again? Y or N ")
        if dec5 == "Y":
            filter_func(url, f_list, 1)
        if dec5 == "N":
            home_page()


def home_page():
    print("Welcome to the Pokedex Home Page")
    print(
        "Would you like to search for a pokemon or look at your favorite pokemon? Press L for search and F for favorite and T for filter"
    )
    decision = input()

    if decision == "L":
        search()

        search()
    if decision == "F":
        print("---Here is your favorites list---------")
        print(favs)
        print("--------------------------------------")
        print("Enter a pokemone from your favorites list to see more detail")
        pokemon = input()
        poke_data = get(f"http://127.0.0.1:5000/pokemon/{pokemon}").json()
        poke_info1(poke_data)

    filter_list = []
    url = "http://127.0.0.1:5000//pokemon"
    x = 0
    if decision == "T":
        filter_func(url, filter_list, x)


def main():
    home_page()


if __name__ == "__main__":
    main()
