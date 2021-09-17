from rest_framework import serializers

from pokemon.models import Pokemon, Stat, Evolution


class StatSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ('name', 'base_stat')


class EvolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evolution
        fields = ('id', 'type', 'name')
        extra_kwargs = {'id': {'read_only': True}}


class PokemonSerializer(serializers.ModelSerializer):
    stats = StatSerializers(many=True)
    evolutions = EvolutionSerializer(many=True)

    class Meta:
        model = Pokemon
        fields = ['ref_api_id', 'name', 'height', 'weight', 'stats', 'evolutions']

    def create(self, validate_data):
        stats_data = validate_data.pop('stats')
        evolution_data = validate_data.pop('evolutions')
        pokemon, _ = Pokemon.objects.get_or_create(**validate_data)
        for stat_data in stats_data:
            Stat.objects.get_or_create(pokemon=pokemon, **stat_data)

        for evolution_data in evolution_data:
            Evolution.objects.get_or_create(pokemon=pokemon, **evolution_data)

        return pokemon
