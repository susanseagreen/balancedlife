# Generated by Django 3.2.7 on 2021-09-26 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipe_ingredients', '0001_initial'),
        ('ingredients', '0001_initial'),
        ('shopping_lists', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.BooleanField(blank=True, default=True)),
                ('done', models.BooleanField(blank=True, default=False)),
                ('measurement_value', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('measurement_type', models.CharField(blank=True, default='', max_length=5, null=True)),
                ('day_of_week', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('meal', models.CharField(blank=True, default='', max_length=15, null=True)),
                ('code_ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shopping_list_item', to='ingredients.ingredient', verbose_name='Ingredient')),
                ('code_recipe_ingredient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shopping_list_item', to='recipe_ingredients.recipeingredient', verbose_name='Recipe Ingredient')),
                ('code_shopping_list', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shopping_list_item', to='shopping_lists.shoppinglist', verbose_name='Shopping List')),
            ],
        ),
    ]
