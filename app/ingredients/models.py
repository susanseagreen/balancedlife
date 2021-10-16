from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code_category = models.ForeignKey(
        'ingredient_categories.IngredientCategory', verbose_name='Category', on_delete=models.PROTECT,
        related_name='ingredient')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        return super(Ingredient, self).save(*args, **kwargs)
