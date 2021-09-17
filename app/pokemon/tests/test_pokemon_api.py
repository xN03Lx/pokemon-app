from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from pokemon.models import Pokemon, Stat, Evolution
from pokemon.api.serializers import PokemonSerializer

POKEMON_URL = reverse("pokemon:pokemon-list")


def detail_url(pokemon_name):
    return reverse("pokemon:pokemon-detail", args=[pokemon_name])


def sample_pokemon(**params):
    defaults = {
        "ref_api_id": 4,
        "height": 6,
        "weight": 85,
    }
    defaults.update(params)
    pokemon = Pokemon.objects.create(**defaults)
    sample_stats(pokemon)
    sample_evolution(pokemon)
    return pokemon


def sample_stats(pokemon):
    defaults = {"name": "hp", "base_stat": 39}
    return Stat.objects.create(pokemon=pokemon, **defaults)


def sample_evolution(pokemon):
    defaults = {"type": "Evolution", "name": "pokemon-sample"}
    return Evolution.objects.create(pokemon=pokemon, **defaults)


class PokemonApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_all_pokemon(self):
        sample_pokemon(name="pokemon-sample")
        sample_pokemon(name="pokemon-sample2")

        res = self.client.get(POKEMON_URL)

        pokemon = Pokemon.objects.all()
        serializer = PokemonSerializer(pokemon, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_valid_pokemon_success(self):
        payload = {
            "ref_api_id": 4,
            "name": "charmanders",
            "height": 6,
            "weight": 85,
            "stats": [{"name": "hp", "base_stat": 39}],
            "evolutions": [{"type": "Evolution", "name": "charmeleon"}],
        }

        res = self.client.post(POKEMON_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Pokemon.objects.filter(name=payload["name"]).exists()
        self.assertTrue(exists)

        pokemon = Pokemon.objects.get(name=res.data["name"])
        self.assertEqual(len(pokemon.stats.all()), 1)
        self.assertEqual(len(pokemon.evolutions.all()), 1)

    def test_pokemon_exists(self):
        payload = {
            "ref_api_id": 4,
            "name": "charmanders",
            "height": 6,
            "weight": 85,
        }
        sample_pokemon(**payload)
        res = self.client.post(POKEMON_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_pokemon_by_name(self):
        name = "pokemon-sample"
        pokemon = sample_pokemon(name=name)
        url = detail_url(name)
        res = self.client.get(url)
        serializer = PokemonSerializer(pokemon)
        self.assertEqual(res.data, serializer.data)
