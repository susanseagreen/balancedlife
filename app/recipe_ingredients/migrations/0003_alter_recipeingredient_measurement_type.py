# Generated by Django 3.2.7 on 2021-09-18 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_ingredients', '0002_alter_recipeingredient_measurement_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='measurement_type',
            field=models.CharField(blank=True, choices=[('', ''), ('g', 'grams'), ('kg', 'kilograms'), ('dp', 'dash/pinch'), ('tsp', 'teaspoons'), ('tbsp', 'tablespoons'), ('c', 'cups'), ('l', 'litres')], default='', max_length=5, null=True),
        ),
    ]
