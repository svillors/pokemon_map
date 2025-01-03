import folium
import os
import django
import sys

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import now

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pogomap.settings')
django.setup()

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
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lt=now(), disappeared_at__gt=now())
    for pokemon_entity in pokemon_entities:
        image_url = request.build_absolute_uri(
            pokemon_entity.pokemon.image.url)
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            image_url
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        if pokemon.image:
            image_url = request.build_absolute_uri(pokemon.image.url)
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'img_url': image_url,
                'title_ru': pokemon.title,
            })
        else:
            pokemons_on_page.append({
                'pokemon_id': pokemon.id,
                'title_ru': pokemon.title,
            })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.filter(id=int(pokemon_id)).first()

    if not requested_pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=requested_pokemon,
        appeared_at__lt=now(),
        disappeared_at__gt=now(),
    )
    image_url = request.build_absolute_uri(requested_pokemon.image.url)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longitude,
            image_url
        )

    pokemon = {
        'pokemon_id': requested_pokemon.id,
        'img_url': image_url,
        'title_ru': requested_pokemon.title,
        'description': requested_pokemon.description
    }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
