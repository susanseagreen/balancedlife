# Generated by Django 3.2.7 on 2021-10-03 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredients', '0001_initial'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement_value', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('measurement_type', models.CharField(blank=True, choices=[('', ''), ('g', 'grams'), ('kg', 'kilograms'), ('dp', 'dash/pinch'), ('tsp', 'teaspoons'), ('tbsp', 'tablespoons'), ('c', 'cups'), ('ml', 'millilitres'), ('l', 'litres')], default='', max_length=5, null=True)),
                ('preparation', models.CharField(blank=True, default='', max_length=40, null=True)),
                ('code_ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipe_item', to='ingredients.ingredient', verbose_name='Ingredient')),
                ('code_recipe', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipe_item', to='recipes.recipe', verbose_name='Recipe')),
            ],
        ),
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('code_recipe', 'code_ingredient'), name='ingredient_recipe_unique'),
        ),
    ]
