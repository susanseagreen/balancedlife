# Generated by Django 3.2.7 on 2021-09-20 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_ingredients', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('code_recipe', 'code_ingredient'), name='ingredient_recipe'),
        ),
    ]
