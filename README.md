# Software-Engineering-Pokemon_API

This was an assignment in my software engineering class, where I took information from the API, made a wrapper, and created a 'pokedex' program!

The cache.py file creates a cache for users to call from, if the item input has already been called. this prevents any damage to the Poke_API, with too many requests in a certain amount of time. 

The api_wrapper.py is the file that takes an input, and will search either the cache or the API for the result and returns it. there is also the ability to filter and get a list of pokemon based on move, type, and ability. 

the pokedex.py file creates an interface for a user to work with. After a user inputs a pokemon the program displays various bits of informaation about the pokemon, as well as, allow for pokemon to be added to a favorites list. 

the test_api_wrapper.py file, conatains tests for the program, making sure that everything runs properly
