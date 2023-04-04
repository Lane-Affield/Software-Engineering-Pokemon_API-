from unittest.mock import patch
from src.api_wrapper import *
from pytest import fixture
import sys
from io import StringIO
from src.pokedex import favs, poke_info2, poke_info3, search


# ----------------------------------------------------
# Tests for returning the objects
# Test for the get_pokemon_by_name
@patch("src.api_wrapper.poke_getter")
def test_get_pokemon_by_name(mock_poke_getter):
    bubl = {"name": "bubl"}
    mock_poke_getter.return_value = {"name": "bubl"}
    ret = get_pokemon_by_name("bubl")
    assert ret == bubl


# Test for the get_ability_by_name
@patch("src.api_wrapper.ability_getter")
def test_get_ability_by_name(mock_ability_getter):
    bubl = {"name": "walking"}
    mock_ability_getter.return_value = {"name": "walking"}
    ret = get_ability_by_name("walking")
    assert ret == bubl


# test for the get_move_name
@patch("src.api_wrapper.move_getter")
def test_get_move_by_name(mock_move_getter):
    bubl = {"name": "kick"}
    mock_move_getter.return_value = {"name": "kick"}
    ret = get_move_by_name("kick")
    assert ret == bubl


# test for the get_sprite
@patch("src.api_wrapper.poke_getter")
def test_get_sprites(mock_poke_getter):
    bubl = {"name": "god", "sprites": "website.com"}
    mock_poke_getter.return_value = {"name": "god", "sprites": "website.com"}
    ret = get_sprite("god")
    assert ret == "website.com"


@patch("src.api_wrapper.poke_getter")
def get_pokemon_by_id(mock_poke_getter):
    bubl = {"name": "", "id": "123"}
    mock_poke_getter.return_value = {"name": "rock", "id": "123"}
    ret = get_pokemon_by_id("123")
    assert ret == bubl


"""
@patch('src.api_wrapper.all_pokemon_getter')
def test_get_all(mock_all_pokemon_getter):
    bubl = {'name' : 'all' , 'url' : 'www.all.com'}
    mock_all_pokemon_getter.return_value = bubl.json
    ret = get_all_pokemon()
    assert ret == bubl
"""


# ----------------------------------------------------
# Tests for returning the filters
# got inspiration for this from Kali Zerwas
@patch("src.api_wrapper.ability_getter")
def test_ability_filter(mock_ability_getter):
    bubl = {"name": "white", "pokemon": "orb"}
    mock_ability_getter.return_value = bubl
    ret = filter_ability("white")
    assert ret == "orb"


@patch("src.api_wrapper.type_getter")
def test_type_filter(mock_type_getter):
    bubl = {"name": "smoke", "pokemon": "smog"}
    mock_type_getter.return_value = bubl
    ret = filter_type("smoke")
    assert ret == "smog"


@patch("src.api_wrapper.move_getter")
def test_move_filter(mock_move_getter):
    bubl = {"name": "wham", "learned_by_pokemon": "george_michael"}
    mock_move_getter.return_value = bubl
    ret = filter_move("wham")
    assert ret == "george_michael"


# ----------------------------------------------------
@patch("src.api_wrapper.poke_getter")
@patch("src.cache.write_cache")
@patch("src.cache.read_cache")
def test_get_pokemon_by_name_no_cache(
    mock_read_cache, mock_write_cache, mock_poke_getter
):
    bubl = {"name": "bubl"}
    mock_read_cache.return_value = {"Pokemon": {}}
    mock_poke_getter.return_value = bubl
    ret = get_pokemon_by_name("bubl")
    assert ret == bubl


@patch("src.api_wrapper.poke_getter")
@patch("src.cache.read_cache")
def test_get_pokemon_by_name_in_cache(mock_read_cache, mock_poke_getter):
    bubl = {"name": "bubl"}
    mock_read_cache.return_value = {"Pokemon": {"name": "bubl"}}
    mock_poke_getter.return_value = bubl
    ret = get_pokemon_by_name("bubl")
    assert ret == bubl


@patch("src.api_wrapper.poke_getter")
@patch("src.cache.write_cache")
@patch("src.cache.read_cache")
def test_get_sprite_by_name_no_cache(
    mock_read_cache, mock_write_cache, mock_poke_getter
):
    bubl = {"name": "hello", "sprites": "hey.com"}
    mock_read_cache.return_value = {"Sprites": {}}
    mock_poke_getter.return_value = bubl
    ret = get_sprite("hello")
    assert ret == "hey.com"


@patch("src.api_wrapper.poke_getter")
@patch("src.cache.write_cache")
@patch("src.cache.read_cache")
def test_get_sprite_by_name_other_cache(
    mock_read_cache, mock_write_cache, mock_poke_getter
):
    bubl = {"name": "yellow", "sprites": "rubber_duck.com"}
    mock_read_cache.return_value = {
        "Pokemon": {"name": "yellow", "sprites": "rubber_duck"},
        "Sprites": "rubber_duck.com",
    }
    mock_poke_getter.return_value = bubl
    ret = get_sprite("yellow")
    assert ret == "rubber_duck.com"


# ----------------------------------------------------
# from professors code
def my_poke_cache():
    return {
        "pokemon": {"1": "bulb"},
    }


@patch("src.cache.read_cache")
def get_pokemon_by_ID_cache_r(mock_read_cache, my_poke_cache):
    mock_read_cache.return_value = my_poke_cache
    result = get_pokemon_by_id("1")
    assert result == my_poke_cache["pokemon"]["1"]


# got the following code from kali zerwas
@patch("src.api_wrapper.ability_getter")
@patch("src.cache.write_cache")
@patch("src.cache.read_cache")
def test_get_poke_move_cache_f(mock_read_cache, mock_write_cache, mock_ability_getter):
    bubl = {"name": "drizzling", "pokemon": "kyogre"}
    mock_read_cache.return_value = {
        "poke_ability": {"name": "drizzling", "pokemon": "kyogre"}
    }
    mock_ability_getter.return_value = bubl
    ret = filter_ability("drizzling")
    assert ret == "kyogre"


# TESTS FOR Pokedex
@fixture
def Gallade():
    {
        "name": "Gallade",
        "abilities": [
            {"ability": {"name": "Sharpness"}},
            {"ability": {"name": "Steadfast"}},
        ],
        "stats": [
            {"base_stat": 100, "stat": {"name": "hp"}},
            {"base_stat": 200, "stat": {"name": "attack"}},
            {"base_stat": 300, "stat": {"name": "defense"}},
            {"base_stat": 450, "stat": {"name": "special-attack"}},
            {"base_stat": 460, "stat": {"name": "special-defense"}},
            {"base_stat": 470, "stat": {"name": "speed"}},
        ],
    }


def test_page_1():
    pass


def test_page_2(capfd):
    poke_data = {
        "name": "Gallade",
        "abilities": [
            {"ability": {"name": "Sharpness"}},
            {"ability": {"name": "Steadfast"}},
        ],
        "stats": [{"base_stat": 100, "stat": {"name": "hp"}}],
    }
    name = "Gallade"

    with patch("builtins.input", return_value="B"), patch(
        "src.pokedex.menu"
    ) as menu_patch:
        output = poke_info2(poke_data, name)
        out, _ = capfd.readouterr()
        expected = (
            "Abilities of Gallade : \n"
            "\n"
            "['Sharpness', 'Steadfast']\n"
            "Gallade's stats: \n"
            "\n"
            '[{"base_stat": 100, "stat": {"name": "hp"}}]'
        )
        assert out.strip() == expected.strip()


def test_page_3(capfd):
    poke_data = {
        "name": "Gallade",
        "moves": [{"move": {"name": "Kick"}}, {"move": {"name": "Jump"}}],
    }

    name = "Gallade"
    with patch("builtins.input", return_value="b"), patch(
        "src.pokedex.menu"
    ) as button_patch:
        poke_info3(poke_data, name)
        # Check that the output matches the expected output
        out, _ = capfd.readouterr()
        expected_out = "Gallade's moves: \n" "\n" "['Kick', 'Jump']\n"
        assert out.strip() == expected_out.strip()


def test_search():
    pass
