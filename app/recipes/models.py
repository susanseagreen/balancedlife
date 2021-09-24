from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    code_category = models.ForeignKey(
        'ingredient_categories.IngredientCategory', verbose_name='Category', on_delete=models.PROTECT,
        related_name='recipe')
    description = models.TextField(max_length=1000, null=True, blank=True)
    steps = models.TextField('Cooking Instructions', max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.username = self.name.title()
        return super(Recipe, self).save(*args, **kwargs)
