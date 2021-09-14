from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    food_group = models.CharField(max_length=50)
    brand = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
