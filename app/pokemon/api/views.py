from rest_framework import viewsets, mixins

from pokemon.models import Pokemon
from pokemon.api.serializers import PokemonSerializer


class PokemonViewsets(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):

    queryset = Pokemon.objects.all()
    serializer_class = PokemonSerializer
    lookup_field = "name"
    lookup_value_regex = "[^/]+"
