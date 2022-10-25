# Generated by Django 3.1.14 on 2022-10-25 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0004_auto_20221025_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonentity',
            name='defence',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pokemonentity',
            name='health',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pokemonentity',
            name='level',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pokemonentity',
            name='stamina',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pokemonentity',
            name='strength',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
