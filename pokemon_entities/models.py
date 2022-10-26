from django.db import models  # noqa F401
from django.utils import timezone


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    title_en = models.CharField(max_length=200)
    title_jp = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    appeared_at = models.DateTimeField(default=timezone.now)
    disappeared_at = models.DateTimeField(default=timezone.now)

    level = models.IntegerField()
    health = models.IntegerField()
    strength = models.IntegerField()
    defence = models.IntegerField()
    stamina = models.IntegerField()
