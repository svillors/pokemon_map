from django.contrib import admin
from .models import Pokemon, PokemonEntity


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(PokemonEntity)
class PokemonEntityAdmin(admin.ModelAdmin):
    list_display = ('pokemon', 'appeared_at', 'disappeared_at',)
    ordering = ('appeared_at', 'pokemon')
