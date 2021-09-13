# Generated by Django 3.2.7 on 2021-09-13 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='code_ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipe_item', to='ingredients.ingredient', verbose_name='Ingredient'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='code_recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipe_item', to='recipes.recipe', verbose_name='Recipe'),
        ),
    ]
