from django.db import models  # noqa F401
from django.utils import timezone


class Pokemon(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, default='описание отсутствует')
    title_en = models.CharField(
        verbose_name='Название на английском языке',
        max_length=200,
        blank=True,
        default='неизвестно'
    )
    title_jp = models.CharField(
        verbose_name='Название на японском языке',
        max_length=200,
        blank=True,
        default='неизвестно'
    )
    previous_form = models.ForeignKey(
        'Pokemon',
        verbose_name='Предыдущая ступень эволюции',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='next_forms'
    )

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Покемон',
        on_delete=models.CASCADE,
        related_name='entities'
    )

    appeared_at = models.DateTimeField(verbose_name='Время появления', default=timezone.now)
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения', default=timezone.now)

    level = models.IntegerField(verbose_name='Уровень', null=True, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', null=True, blank=True)
    strength = models.IntegerField(verbose_name='Сила', null=True, blank=True)
    defence = models.IntegerField(verbose_name='Защита', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', null=True, blank=True)
