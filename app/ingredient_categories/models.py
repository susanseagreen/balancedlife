from django.db import models


class IngredientCategory(models.Model):
    name = models.CharField(max_length=50)
    order = models.IntegerField(max_length=2, default=1)

    def __str__(self):
        return self.name
