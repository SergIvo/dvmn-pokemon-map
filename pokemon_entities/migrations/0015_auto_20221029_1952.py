# Generated by Django 3.1.14 on 2022-10-29 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0014_auto_20221029_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemonentity',
            name='pokemon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entities', to='pokemon_entities.pokemon', verbose_name='Покемон'),
        ),
    ]
