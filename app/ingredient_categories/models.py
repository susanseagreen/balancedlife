from django.db import models


class IngredientCategory(models.Model):
    name = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=99)

    def __str__(self):
        return self.name
