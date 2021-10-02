from django.db import models


class ShoppingListItem(models.Model):
    code_shopping_list = models.ForeignKey(
        'shopping_lists.ShoppingList', verbose_name='Shopping List', on_delete=models.PROTECT,
        related_name='shopping_list_item')

    added = models.BooleanField(default=True, blank=True)

    code_ingredient = models.ForeignKey(
        'ingredients.Ingredient', verbose_name='Ingredient', on_delete=models.PROTECT,
        related_name='shopping_list_item')
    code_recipe_ingredient = models.ForeignKey(
        'recipe_ingredients.RecipeIngredient', verbose_name='Recipe Ingredient', blank=True, null=True,
        on_delete=models.PROTECT, related_name='shopping_list_item')
    measurement_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    measurement_type = models.CharField(default='', max_length=5, blank=True, null=True)
    day_of_week = models.CharField(default='', max_length=15, blank=True, null=True)
    meal = models.CharField(default='', max_length=15, blank=True, null=True)

    def __str__(self):
        return self.code_ingredient.name
