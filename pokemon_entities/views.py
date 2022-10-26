import folium
import json

from django.http import HttpResponseNotFound, request
from django.shortcuts import render
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from pokemon_entities.models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_datetime = timezone.localtime()
    for pokemon in Pokemon.objects.all():
        if pokemon.image:
            for pokemon_entity in PokemonEntity.objects.filter(
                pokemon=pokemon,
                appeared_at__lte=current_datetime,
                disappeared_at__gte=current_datetime
            ):
                add_pokemon(
                    folium_map, pokemon_entity.latitude,
                    pokemon_entity.longitude,
                    request.build_absolute_uri(pokemon.image.url)
                )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        if pokemon.image:
            pokemon_image_url = request.build_absolute_uri(pokemon.image.url)
        else:
            pokemon_image_url = None
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
        pokemons = json.load(database)['pokemons']

    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(pokemon=requested_pokemon):
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(requested_pokemon.image.url)
        )

    pokemon = {'title_ru': requested_pokemon.title,
               'img_url': request.build_absolute_uri(requested_pokemon.image.url),
               'title_en': requested_pokemon.title_en,
               'title_jp': requested_pokemon.title_jp,
               'description': requested_pokemon.description
    }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
