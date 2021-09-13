# Generated by Django 3.2.7 on 2021-09-13 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0002_alter_ingredient_name'),
        ('recipes', '0004_recipe_category'),
        ('shopping_list', '0002_alter_shoppinglist_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglist',
            name='code_ingredient',
            field=models.ManyToManyField(related_name='shopping_list', to='ingredients.Ingredient', verbose_name='Ingredient'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='code_recipe',
            field=models.ManyToManyField(related_name='shopping_list', to='recipes.Recipe', verbose_name='Recipe'),
        ),
    ]
