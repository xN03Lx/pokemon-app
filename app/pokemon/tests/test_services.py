from django.test import TestCase

from pokemon.services import PokemonApiService


class TestPokemonService(TestCase):
    def test_get_evolutions(self):
        expected_output = [
            {"type": "Preevolution", "name": "charmander"},
            {"type": "Evolution", "name": "charizard"},
        ]
        evolution_chains_list = ["charmander", "charmeleon", "charizard"]
        service = PokemonApiService()
        res = service.get_evolutions("charmeleon", evolution_chains_list)
        self.assertEqual(expected_output, res)
