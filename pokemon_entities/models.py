from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('Имя', max_length=200)
    title_en = models.CharField('Имя на английском', max_length=200,
                                blank=True)
    title_jp = models.CharField('Имя на японском', max_length=200, blank=True)
    image = models.ImageField('Картинка покемона', blank=True, null=True)
    description = models.TextField('Описание покемона', blank=True)
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL,
                                           null=True, blank=True,
                                           related_name="next_evolution",
                                           verbose_name='Прошлая эволюция')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
                                verbose_name='Покемон')
    latitude = models.FloatField('Долгота')
    longitude = models.FloatField('Широта')
    appeared_at = models.DateTimeField("Появляется в")
    disappeared_at = models.DateTimeField("Исчезает в")
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strenght = models.IntegerField("Сила", null=True, blank=True)
    defence = models.IntegerField("Защита", null=True, blank=True)
    stamina = models.IntegerField("Выносливость", null=True, blank=True)
