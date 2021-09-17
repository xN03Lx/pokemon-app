import logging

import requests

import pokebase as pb
from pokebase import cache
cache.API_CACHE

logging.getLogger().setLevel(logging.INFO)


class PokemonApiService:
    def __init__(self):
        self.raw_evolution_chain = {}
        self._evolution_chains_list = []

    def get_evolution_chains_by_id(self, evolution_chain_id):
        try:
            self.raw_evolution_chain = pb.evolution_chain(evolution_chain_id)
            return self._get_evolution_chains_list()
        except requests.HTTPError as exception:
            logging.error(exception)

    def get_pokemon(self, name):
        return pb.pokemon(name)

    def get_pokemon_details(self, pokemon):
        return self._build_pokemon_details_from_response(pokemon)

    def _build_pokemon_details_from_response(self, pokemon):
        return {
            "ref_api_id": pokemon.id,
            "name": pokemon.name,
            "weight": pokemon.weight,
            "height": pokemon.height
        }

    def get_evolutions(self, pokemon, evolution_chains_list):
        index_pokemon = evolution_chains_list.index(pokemon)
        evolutions = []
        for index, evolution in enumerate(evolution_chains_list):
            if index_pokemon != index:
                evolution_type = ''
                if index_pokemon < index:
                    evolution_type = "Evolution"
                if index_pokemon > index:
                    evolution_type = "Preevolution"
                evolutions.append({
                    "type": evolution_type,
                    "name": evolution
                })
        return evolutions

    def _get_evolution_chains_list(self):
        first_pokemon_in_chain = self.raw_evolution_chain.chain.species.name
        self._evolution_chains_list.append(first_pokemon_in_chain)
        evolves_to = self.raw_evolution_chain.chain.evolves_to
        self.fill_evolution_chains_recursively(evolves_to)
        return self._evolution_chains_list

    def fill_evolution_chains_recursively(self, evolves):
        for pokemon in evolves:
            pokemon_name = pokemon.species.name
            self._evolution_chains_list.append(pokemon_name)
            if (pokemon.evolves_to):
                self.fill_evolution_chains_recursively(pokemon.evolves_to)

    def get_stats(self, pokemon):
        return [
            {
                "base_stat": stat.base_stat,
                "name": stat.stat.name
            }
            for stat in pokemon.stats
        ]
