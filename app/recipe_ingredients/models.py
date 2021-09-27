from django.db import models
from common.choices import measurement_type_choices


class RecipeIngredient(models.Model):
    code_recipe = models.ForeignKey('recipes.Recipe', verbose_name='Recipe', on_delete=models.PROTECT,
                                    related_name='recipe_item')
    code_ingredient = models.ForeignKey('ingredients.Ingredient', verbose_name='Ingredient', on_delete=models.PROTECT,
                                        related_name='recipe_item')
    measurement_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    measurement_type = models.CharField(choices=measurement_type_choices, default='', max_length=5, blank=True,
                                        null=True)
    description = models.CharField(default='', max_length=40, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[
                'code_recipe',
                'code_ingredient',
            ],
                name="ingredient_recipe_unique"
            )
        ]

    def __str__(self):
        return self.code_ingredient.name
