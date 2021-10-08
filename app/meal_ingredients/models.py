from django.db import models
from common.choices import measurement_type_choices


class MealIngredient(models.Model):
    code_meal = models.ForeignKey('meals.Meal', verbose_name='Meal', on_delete=models.PROTECT,
                                    related_name='meal_item')
    code_ingredient = models.ForeignKey('ingredients.Ingredient', verbose_name='Ingredient', on_delete=models.PROTECT,
                                        related_name='meal_item')
    measurement_value = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    measurement_type = models.CharField(choices=measurement_type_choices, default='', max_length=5, blank=True,
                                        null=True)
    preparation = models.CharField(default='', max_length=40, blank=True, null=True)

    def __str__(self):
        return self.code_meal

    def save(self, *args, **kwargs):
        if self.preparation:
            self.preparation = self.preparation.title()
        return super(MealIngredient, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[
                'code_meal',
                'code_ingredient',
            ],
                name="ingredient_meal_unique"
            )
        ]

    def __str__(self):
        return self.code_ingredient.name
