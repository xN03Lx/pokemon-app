from django.urls import path, include

from rest_framework.routers import DefaultRouter

from pokemon.api.views import PokemonViewsets


router = DefaultRouter()

router.register('pokemon', PokemonViewsets)

app_name = 'pokemon'

urlpatterns = [
    path('', include(router.urls))
]
