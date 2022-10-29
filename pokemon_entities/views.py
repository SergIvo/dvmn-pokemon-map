import folium
import json

from django.http import HttpResponseNotFound, request
from django.shortcuts import render, get_object_or_404
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
    all_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_datetime,
        disappeared_at__gte=current_datetime
    )
    for pokemon_entity in all_entities:
        if pokemon_entity.pokemon.image:
            add_pokemon(
                folium_map, pokemon_entity.latitude,
                pokemon_entity.longitude,
                request.build_absolute_uri(pokemon_entity.pokemon.image.url)
            )
        else:
            add_pokemon(
                folium_map, pokemon_entity.latitude,
                pokemon_entity.longitude,
            )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        if pokemon.image:
            pokemon_image_uri = request.build_absolute_uri(pokemon.image.url)
        else:
            pokemon_image_uri = DEFAULT_IMAGE_URL
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_image_uri,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    current_datetime = timezone.localtime()
    entities = requested_pokemon.entities.filter(
        appeared_at__lte=current_datetime,
        disappeared_at__gte=current_datetime
    )
    for pokemon_entity in entities:
        if requested_pokemon.image:
            add_pokemon(
                folium_map, pokemon_entity.latitude,
                pokemon_entity.longitude,
                request.build_absolute_uri(requested_pokemon.image.url)
            )
        else:
            add_pokemon(
                folium_map, pokemon_entity.latitude,
                pokemon_entity.longitude,
            )

    pokemon = {
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
    }
    if requested_pokemon.image:
        pokemon['img_url'] = request.build_absolute_uri(requested_pokemon.image.url)
    else:
        pokemon['img_url'] = DEFAULT_IMAGE_URL
    if requested_pokemon.previous_form:
        pokemon['previous_evolution'] = {
            'pokemon_id': requested_pokemon.previous_form.id,
            'img_url': request.build_absolute_uri(requested_pokemon.previous_form.image.url),
            'title_ru': requested_pokemon.previous_form.title
        }
    next_form = requested_pokemon.next_forms.first()
    if next_form:
        pokemon['next_evolution'] = {
            'pokemon_id': next_form.id,
            'img_url': request.build_absolute_uri(next_form.image.url),
            'title_ru': next_form.title
        }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
