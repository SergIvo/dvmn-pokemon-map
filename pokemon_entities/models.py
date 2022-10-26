from django.db import models  # noqa F401
from django.utils import timezone


class Pokemon(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True)
    description = models.TextField(verbose_name='Описание',)
    title_en = models.CharField(verbose_name='Название на английском языке', max_length=200)
    title_jp = models.CharField(verbose_name='Название на японском языке', max_length=200)
    previous_form = models.ForeignKey(
        'Pokemon',
        verbose_name='Предыдущая ступень эволюции',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='next_form'
    )

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    latitude = models.FloatField(verbose_name='Широта', null=False)
    longitude = models.FloatField(verbose_name='Долгота', null=False)
    pokemon = models.ForeignKey(Pokemon, verbose_name='Покемон', on_delete=models.CASCADE)

    appeared_at = models.DateTimeField(verbose_name='Время появления', default=timezone.now)
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения', default=timezone.now)

    level = models.IntegerField(verbose_name='Уровень')
    health = models.IntegerField(verbose_name='Здоровье')
    strength = models.IntegerField(verbose_name='Сила')
    defence = models.IntegerField(verbose_name='Защита')
    stamina = models.IntegerField(verbose_name='Выносливость')
