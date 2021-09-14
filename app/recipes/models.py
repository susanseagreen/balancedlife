from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, null=True, blank=True)
    steps = models.TextField('Cooking Instructions', max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    code_recipe = models.ForeignKey('recipes.Recipe', verbose_name='Recipe', on_delete=models.PROTECT, related_name='recipe_item')
    code_ingredient = models.ForeignKey('ingredients.Ingredient', verbose_name='Ingredient', on_delete=models.PROTECT, related_name='recipe_item')
    measurement_value = models.DecimalField(max_digits=5, decimal_places=2)
    measurement_type = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.code_recipe
