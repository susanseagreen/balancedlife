from django.db import models


class ShoppingList(models.Model):
    name = models.CharField(max_length=50)
    date_shop = models.DateField(blank=True, null=True)
    done = models.BooleanField(default=False, blank=True)
    code_recipe = models.ManyToManyField('recipes.Recipe', verbose_name='Recipe', related_name='shopping_list')
    code_ingredient = models.ManyToManyField('ingredients.Ingredient', verbose_name='Ingredient', related_name='shopping_list')

    def __str__(self):
        return self.name
