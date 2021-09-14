# Generated by Django 3.2.7 on 2021-09-14 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        ('ingredients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement_value', models.DecimalField(decimal_places=2, max_digits=5)),
                ('measurement_type', models.CharField(blank=True, max_length=50, null=True)),
                ('code_ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipe_item', to='ingredients.ingredient', verbose_name='Ingredient')),
                ('code_recipe', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipe_item', to='recipes.recipe', verbose_name='Recipe')),
            ],
        ),
    ]
