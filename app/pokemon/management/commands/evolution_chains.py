from django.core.management.base import BaseCommand

from pokemon.services import PokemonApiService
from pokemon.api.serializers import PokemonSerializer


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('id', type=int, help="Indicate the id for evolution chains")

    def handle(self, *args, **options):
        _id = options['id']
        api_service = PokemonApiService()
        self.stdout.write(self.style.SUCCESS('Loading data from the api...'))
        evolution_chains = api_service.get_evolution_chains_by_id(_id)
        pokemon_list = []
        for pokemon_name in evolution_chains:
            self.stdout.write(self.style.HTTP_INFO(f'pokemon: {pokemon_name}'))
            pokemon = api_service.get_pokemon(pokemon_name)
            details = api_service.get_pokemon_details(pokemon)
            stats = api_service.get_stats(pokemon)
            evolutions = api_service.get_evolutions(pokemon_name, evolution_chains)
            pokemon_list.append({
                **details,
                "stats": stats,
                "evolutions": evolutions
            })
        self.stdout.write(self.style.SUCCESS('Saving data...'))
        serializer = PokemonSerializer(data=pokemon_list, many=True)
        if serializer.is_valid():
            serializer.save()
        self.stdout.write(self.style.SUCCESS('Done!'))
