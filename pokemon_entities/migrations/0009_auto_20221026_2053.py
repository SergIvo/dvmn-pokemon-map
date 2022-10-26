# Generated by Django 3.1.14 on 2022-10-26 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0008_pokemon_previous_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='previous_form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_form', to='pokemon_entities.pokemon'),
        ),
    ]
